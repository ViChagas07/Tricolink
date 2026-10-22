import { create } from "zustand";

import { api, type UserDto } from "@/lib/api";

export type AuthUser = {
  id: string;
  email: string;
  displayName: string | null;
  locale: string | null;
  isActive: boolean;
  createdAt: string;
};

export type AuthStatus = "idle" | "loading" | "authenticated" | "anonymous";

type AuthState = {
  user: AuthUser | null;
  status: AuthStatus;
  load: () => Promise<void>;
  setUser: (user: AuthUser | null) => void;
  logout: () => Promise<void>;
  reset: () => void;
};

export function mapUserDto(dto: UserDto): AuthUser {
  return {
    id: dto.id,
    email: dto.email,
    displayName: dto.display_name,
    locale: dto.locale,
    isActive: dto.is_active,
    createdAt: dto.created_at,
  };
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  status: "idle",

  async load() {
    const status = get().status;
    if (status === "loading" || status === "authenticated") {
      return;
    }

    set({ status: "loading" });
    try {
      const user = await api.getMe();
      set({ user: mapUserDto(user), status: "authenticated" });
    } catch {
      set({ user: null, status: "anonymous" });
    }
  },

  setUser(user) {
    set({ user, status: user ? "authenticated" : "anonymous" });
  },

  async logout() {
    try {
      await api.logout();
    } catch {
      // The local session is cleared even when the API is unreachable.
    } finally {
      set({ user: null, status: "anonymous" });
    }
  },

  reset() {
    set({ user: null, status: "idle" });
  },
}));
