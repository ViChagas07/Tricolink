import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { NextIntlClientProvider, type AbstractIntlMessages } from "next-intl";
import { beforeEach, describe, expect, it, vi } from "vitest";

import enMessages from "../../../messages/en.json";
import type { UserDto } from "@/lib/api";
import type { AuthUser } from "@/stores/auth-store";
import { AccountForm } from "./account-form";

const updateAvatar = vi.hoisted(() => vi.fn());
const deleteAvatar = vi.hoisted(() => vi.fn());
const prepareAvatar = vi.hoisted(() => vi.fn());
const setUser = vi.hoisted(() => vi.fn());

vi.mock("@/i18n/navigation", () => ({
  usePathname: () => "/account",
  useRouter: () => ({ replace: vi.fn(), refresh: vi.fn() }),
}));

vi.mock("@/lib/api", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/lib/api")>();
  return {
    ...actual,
    api: {
      ...actual.api,
      updateAvatar,
      deleteAvatar,
    },
  };
});

vi.mock("@/lib/avatar", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/lib/avatar")>();
  return { ...actual, prepareAvatar };
});

vi.mock("@/stores/auth-store", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/stores/auth-store")>();
  return {
    ...actual,
    useAuthStore: (selector: (state: { setUser: typeof setUser; logout: () => void }) => unknown) =>
      selector({ setUser, logout: vi.fn() }),
  };
});

const googleAvatar = "https://lh3.googleusercontent.com/a/photo=s96-c";

const baseDto: UserDto = {
  id: "00000000-0000-4000-8000-000000000001",
  email: "ada@example.com",
  display_name: "Ada Lovelace",
  locale: "en",
  is_active: true,
  created_at: "2026-01-01T00:00:00Z",
  avatar_url: googleAvatar,
  avatar_source: "google",
};

const baseUser: AuthUser = {
  id: baseDto.id,
  email: baseDto.email,
  displayName: baseDto.display_name,
  locale: baseDto.locale,
  isActive: baseDto.is_active,
  createdAt: baseDto.created_at,
  avatarUrl: baseDto.avatar_url,
  avatarSource: baseDto.avatar_source,
};

function renderForm(user: AuthUser = baseUser) {
  return render(
    <NextIntlClientProvider
      locale="en"
      messages={enMessages as AbstractIntlMessages}
      timeZone="UTC"
    >
      <AccountForm initialUser={user} />
    </NextIntlClientProvider>,
  );
}

describe("AccountForm avatar", () => {
  beforeEach(() => {
    updateAvatar.mockReset();
    deleteAvatar.mockReset();
    prepareAvatar.mockReset();
    setUser.mockReset();
  });

  it("shows the Google picture without a remove action", () => {
    renderForm();

    expect(document.querySelector("img")).toHaveAttribute("src", googleAvatar);
    expect(screen.getByRole("button", { name: "Change photo" })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Remove photo" })).not.toBeInTheDocument();
  });

  it("uploads a cropped avatar and shows it", async () => {
    const user = userEvent.setup();
    prepareAvatar.mockResolvedValue({ content_type: "image/jpeg", data: "abc" });
    updateAvatar.mockResolvedValue({
      ...baseDto,
      avatar_url: "/api/v1/auth/me/avatar?v=2",
      avatar_source: "custom",
    });
    renderForm();

    await user.upload(
      screen.getByLabelText("Change photo"),
      new File(["x"], "avatar.png", { type: "image/png" }),
    );

    await waitFor(() =>
      expect(updateAvatar).toHaveBeenCalledWith({ content_type: "image/jpeg", data: "abc" }),
    );
    await waitFor(() =>
      expect(document.querySelector("img")).toHaveAttribute(
        "src",
        "/api/v1/auth/me/avatar?v=2",
      ),
    );
    expect(screen.getByRole("button", { name: "Remove photo" })).toBeInTheDocument();
    expect(setUser).toHaveBeenCalled();
  });

  it("removes a custom avatar and falls back to initials", async () => {
    const user = userEvent.setup();
    deleteAvatar.mockResolvedValue({
      ...baseDto,
      avatar_url: null,
      avatar_source: null,
    });
    renderForm({
      ...baseUser,
      avatarUrl: "/api/v1/auth/me/avatar?v=1",
      avatarSource: "custom",
    });

    await user.click(screen.getByRole("button", { name: "Remove photo" }));

    await waitFor(() => expect(document.querySelector("img")).toBeNull());
    expect(screen.getByText("AL")).toBeInTheDocument();
    expect(deleteAvatar).toHaveBeenCalledTimes(1);
  });
});
