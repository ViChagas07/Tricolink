import { beforeEach, describe, expect, it, vi } from "vitest";

const getMe = vi.hoisted(() => vi.fn());
const logout = vi.hoisted(() => vi.fn());

vi.mock("@/lib/api", () => ({
  api: { getMe, logout },
}));

import { useAuthStore } from "./auth-store";

const dto = {
  id: "11111111-1111-1111-1111-111111111111",
  email: "ada@example.com",
  display_name: "Ada",
  locale: "pt-BR",
  is_active: true,
  created_at: "2026-01-01T00:00:00Z",
};

describe("useAuthStore", () => {
  beforeEach(() => {
    useAuthStore.getState().reset();
    getMe.mockReset();
    logout.mockReset();
  });

  it("loads the current user from /auth/me", async () => {
    getMe.mockResolvedValueOnce(dto);

    await useAuthStore.getState().load();

    expect(getMe).toHaveBeenCalledTimes(1);
    expect(useAuthStore.getState()).toMatchObject({
      status: "authenticated",
      user: {
        id: dto.id,
        email: dto.email,
        displayName: "Ada",
        locale: "pt-BR",
        isActive: true,
      },
    });
  });

  it("treats a failed session as anonymous", async () => {
    getMe.mockRejectedValueOnce(new Error("unauthorized"));

    await useAuthStore.getState().load();

    expect(useAuthStore.getState()).toMatchObject({ status: "anonymous", user: null });
  });

  it("does not call /auth/me again once resolved", async () => {
    getMe.mockResolvedValueOnce(dto);
    await useAuthStore.getState().load();
    await useAuthStore.getState().load();

    expect(getMe).toHaveBeenCalledTimes(1);
  });

  it("clears the user on logout even when the request fails", async () => {
    useAuthStore.setState({ status: "authenticated", user: { id: "1" } as never });
    logout.mockRejectedValueOnce(new Error("network"));

    await useAuthStore.getState().logout();

    expect(useAuthStore.getState()).toMatchObject({ status: "anonymous", user: null });
    expect(logout).toHaveBeenCalledTimes(1);
  });
});
