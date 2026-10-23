import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { NextIntlClientProvider, type AbstractIntlMessages } from "next-intl";
import { beforeEach, describe, expect, it, vi } from "vitest";

import enMessages from "../../../messages/en.json";
import { ApiError, api, type UserDto } from "@/lib/api";
import { useAuthStore } from "@/stores/auth-store";
import { LoginForm } from "./login-form";

const navigation = vi.hoisted(() => ({ replace: vi.fn() }));

vi.mock("@/i18n/navigation", () => ({
  useRouter: () => ({ replace: navigation.replace }),
  Link: ({
    href,
    children,
    ...props
  }: Omit<React.AnchorHTMLAttributes<HTMLAnchorElement>, "href"> & { href: string }) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
}));

vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return {
    ...actual,
    api: {
      ...actual.api,
      register: vi.fn(),
      login: vi.fn(),
    },
  };
});

const user: UserDto = {
  id: "00000000-0000-4000-8000-000000000001",
  email: "ada@example.com",
  display_name: "Ada",
  locale: "en",
  is_active: true,
  created_at: "2026-01-01T00:00:00Z",
  avatar_url: null,
  avatar_source: null,
};

function renderForm(nextPath = "/en") {
  return render(
    <NextIntlClientProvider
      locale="en"
      messages={enMessages as AbstractIntlMessages}
      timeZone="UTC"
    >
      <LoginForm nextPath={nextPath} />
    </NextIntlClientProvider>,
  );
}

async function fillCredentials(email = "ada@example.com", password = "correct horse battery") {
  const browser = userEvent.setup();
  await browser.type(screen.getByLabelText("Email"), email);
  await browser.type(screen.getByLabelText("Password"), password);
  return browser;
}

describe("LoginForm", () => {
  beforeEach(() => {
    navigation.replace.mockReset();
    vi.mocked(api.login).mockReset();
    vi.mocked(api.register).mockReset();
    useAuthStore.getState().reset();
    window.localStorage.clear();
    window.sessionStorage.clear();
  });

  it("validates the registration fields inline", async () => {
    const browser = userEvent.setup();
    renderForm();

    await browser.click(screen.getByRole("tab", { name: "Create account" }));
    await browser.type(screen.getByLabelText("Email"), "not-an-email");
    await browser.type(screen.getByLabelText("Password"), "short");
    await browser.click(screen.getByRole("button", { name: "Create account" }));

    expect(screen.getByText("Enter a valid email address.")).toBeInTheDocument();
    expect(screen.getByText("Use at least 10 characters.")).toBeInTheDocument();
    expect(api.login).not.toHaveBeenCalled();
    expect(api.register).not.toHaveBeenCalled();
  });

  it("shows a generic message for invalid credentials", async () => {
    vi.mocked(api.login).mockRejectedValueOnce(
      new ApiError({ status: 401, code: "invalid_credentials", message: "invalid" }),
    );
    renderForm();
    const browser = await fillCredentials();

    await browser.click(screen.getByRole("button", { name: "Sign in" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("Invalid email or password.");
    expect(navigation.replace).not.toHaveBeenCalled();
  });

  it("shows the wait time on 429", async () => {
    vi.mocked(api.login).mockRejectedValueOnce(
      new ApiError({
        status: 429,
        code: "too_many_attempts",
        message: "slow down",
        retryAfter: 30,
      }),
    );
    renderForm();
    const browser = await fillCredentials();

    await browser.click(screen.getByRole("button", { name: "Sign in" }));

    const alert = await screen.findByRole("alert");
    expect(alert).toHaveTextContent("Too many attempts");
    expect(alert).toHaveTextContent(/Try again in \d+ seconds/);
    expect(screen.getByRole("button", { name: "Sign in" })).toBeDisabled();
  });

  it("toggles password visibility", async () => {
    renderForm();
    const browser = userEvent.setup();
    const password = screen.getByLabelText("Password");

    expect(password).toHaveAttribute("type", "password");
    await browser.click(screen.getByRole("button", { name: "Show password" }));
    expect(password).toHaveAttribute("type", "text");
    await browser.click(screen.getByRole("button", { name: "Hide password" }));
    expect(password).toHaveAttribute("type", "password");
  });

  it("sends registered users to the locale-aware next path without storing tokens", async () => {
    vi.mocked(api.login).mockResolvedValueOnce({ user });
    renderForm("/en/account");
    const browser = await fillCredentials();

    await browser.click(screen.getByRole("button", { name: "Sign in" }));

    await waitFor(() =>
      expect(navigation.replace).toHaveBeenCalledWith("/account", { locale: "en" }),
    );
    expect(useAuthStore.getState().user?.email).toBe("ada@example.com");
    expect(window.localStorage.length).toBe(0);
    expect(window.sessionStorage.length).toBe(0);
  });

  it("registers and signs in automatically", async () => {
    vi.mocked(api.register).mockResolvedValueOnce({ status: "registered" });
    vi.mocked(api.login).mockResolvedValueOnce({ user });
    renderForm();
    const browser = userEvent.setup();

    await browser.click(screen.getByRole("tab", { name: "Create account" }));
    await browser.type(screen.getByLabelText("Email"), "ada@example.com");
    await browser.type(screen.getByLabelText("Password"), "correct horse battery");
    await browser.click(screen.getByRole("button", { name: "Create account" }));

    await waitFor(() => expect(api.register).toHaveBeenCalledTimes(1));
    await waitFor(() => expect(api.login).toHaveBeenCalledTimes(1));
    expect(navigation.replace).toHaveBeenCalledWith("/", { locale: "en" });
  });

  it("builds the Google redirect with the validated next path", () => {
    renderForm("/en/links");

    expect(screen.getByRole("link", { name: "Continue with Google" })).toHaveAttribute(
      "href",
      "/api/v1/auth/google/login?next=%2Fen%2Flinks",
    );
  });
});
