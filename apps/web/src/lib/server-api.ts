import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { cache } from "react";

import { isLocale } from "@/i18n/locales";
import type { UserDto } from "@/lib/api";
import type { LinkDto, ListLinksDto } from "@/lib/links";
import type { LinkStatsDto, StatsRange } from "@/lib/stats";
import type { AuthUser } from "@/stores/auth-store";

const API_INTERNAL_URL = (process.env.API_INTERNAL_URL ?? "http://localhost:8000").replace(
  /\/+$/,
  "",
);
const REQUEST_TIMEOUT_MS = 5_000;

async function cookieHeader(): Promise<string> {
  const store = await cookies();
  return store
    .getAll()
    .map(({ name, value }) => `${name}=${value}`)
    .join("; ");
}

async function serverFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const headers = new Headers(init.headers);
  headers.set("Accept", "application/json");
  const cookie = await cookieHeader();
  if (cookie) {
    headers.set("Cookie", cookie);
  }

  return fetch(`${API_INTERNAL_URL}/api/v1${path}`, {
    ...init,
    headers,
    cache: "no-store",
    signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
  });
}

function toAuthUser(user: UserDto): AuthUser {
  return {
    id: user.id,
    email: user.email,
    displayName: user.display_name,
    locale: user.locale,
    isActive: user.is_active,
    createdAt: user.created_at,
  };
}

export const getServerUser = cache(async (): Promise<AuthUser | null> => {
  const cookie = await cookieHeader();
  if (!cookie) {
    return null;
  }

  try {
    const response = await serverFetch("/auth/me");
    if (!response.ok) {
      return null;
    }
    const user = (await response.json()) as UserDto;
    if (!user || typeof user.id !== "string") {
      return null;
    }
    return toAuthUser(user);
  } catch {
    return null;
  }
});

export async function requireUser(locale: string, nextPath: string): Promise<AuthUser> {
  const user = await getServerUser();
  if (user) {
    return user;
  }

  const safeLocale = isLocale(locale) ? locale : "en";
  redirect(`/${safeLocale}/login?next=${encodeURIComponent(nextPath)}`);
}

export type ServerLinksPage = {
  page: ListLinksDto | null;
  summary: { clicks: number; links: number } | null;
};

export async function getServerLinks(query = ""): Promise<ServerLinksPage> {
  const search = new URLSearchParams({ limit: "20" });
  if (query.trim()) {
    search.set("q", query.trim());
  }

  try {
    const response = await serverFetch(`/links?${search.toString()}`);
    if (!response.ok) {
      return { page: null, summary: null };
    }
    const page = (await response.json()) as ListLinksDto;
    if (!page || !Array.isArray(page.items)) {
      return { page: null, summary: null };
    }
    return { page, summary: await getServerLinksOverview() };
  } catch {
    return { page: null, summary: null };
  }
}

async function getServerLinksOverview(): Promise<{ clicks: number; links: number } | null> {
  try {
    const response = await serverFetch("/links/overview?range=30d");
    if (!response.ok) {
      return null;
    }
    const payload = (await response.json()) as {
      total_clicks?: unknown;
      total_links?: unknown;
    };
    if (typeof payload.total_clicks !== "number" || typeof payload.total_links !== "number") {
      return null;
    }
    return { clicks: payload.total_clicks, links: payload.total_links };
  } catch {
    return null;
  }
}

export async function getServerLink(code: string): Promise<LinkDto | null> {
  try {
    const response = await serverFetch(`/links/${encodeURIComponent(code)}`);
    if (!response.ok) {
      return null;
    }
    const link = (await response.json()) as LinkDto;
    if (!link || typeof link.code !== "string") {
      return null;
    }
    return link;
  } catch {
    return null;
  }
}

export async function getServerLinkStats(
  code: string,
  range: StatsRange = "30d",
): Promise<LinkStatsDto | null> {
  try {
    const search = new URLSearchParams({ range });
    const response = await serverFetch(
      `/links/${encodeURIComponent(code)}/stats?${search.toString()}`,
    );
    if (!response.ok) {
      return null;
    }
    const stats = (await response.json()) as LinkStatsDto;
    if (!stats || !Array.isArray(stats.series) || typeof stats.total !== "number") {
      return null;
    }
    return stats;
  } catch {
    return null;
  }
}
