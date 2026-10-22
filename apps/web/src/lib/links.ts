import { api } from "@/lib/api";

export type LinkDto = {
  code: string;
  short_url: string;
  original_url: string;
  title: string | null;
  created_at: string;
  expires_at: string | null;
  is_active: boolean;
  click_count: number;
};

export type ListLinksDto = {
  items: LinkDto[];
  next_cursor: string | null;
};

export type ListLinksParams = {
  cursor?: string | null;
  limit?: number;
  q?: string;
};

export type UpdateLinkInput = {
  title?: string | null;
  original_url?: string;
  expires_at?: string | null;
  is_active?: boolean;
};

export type LinkStatus = "active" | "inactive" | "expired";

export function listLinks(params: ListLinksParams = {}): Promise<ListLinksDto> {
  const search = new URLSearchParams();
  if (params.cursor) {
    search.set("cursor", params.cursor);
  }
  if (params.limit) {
    search.set("limit", String(params.limit));
  }
  if (params.q?.trim()) {
    search.set("q", params.q.trim());
  }
  const suffix = search.size > 0 ? `?${search.toString()}` : "";
  return api.get<ListLinksDto>(`/links${suffix}`);
}

export function getLink(code: string): Promise<LinkDto> {
  return api.get<LinkDto>(`/links/${encodeURIComponent(code)}`);
}

export function updateLink(code: string, input: UpdateLinkInput): Promise<LinkDto> {
  return api.patch<LinkDto>(`/links/${encodeURIComponent(code)}`, input);
}

export function deleteLink(code: string): Promise<void> {
  return api.delete<void>(`/links/${encodeURIComponent(code)}`);
}

export function linkStatus(link: Pick<LinkDto, "is_active" | "expires_at">): LinkStatus {
  if (!link.is_active) {
    return "inactive";
  }
  if (link.expires_at) {
    const expires = Date.parse(link.expires_at);
    if (!Number.isNaN(expires) && expires <= Date.now()) {
      return "expired";
    }
  }
  return "active";
}

export function toDateTimeLocal(value: string | null): string {
  if (!value) {
    return "";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "";
  }
  const offset = date.getTimezoneOffset() * 60_000;
  return new Date(date.getTime() - offset).toISOString().slice(0, 16);
}

export function fromDateTimeLocal(value: string): string | null {
  if (!value) {
    return null;
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return null;
  }
  return date.toISOString();
}
