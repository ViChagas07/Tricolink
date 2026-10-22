import { beforeEach, describe, expect, it, vi } from "vitest";

import { api, ApiError, parseRetryAfter, resetApiClientForTests } from "./api";

function jsonResponse(body: unknown, status = 200, headers: Record<string, string> = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", ...headers },
  });
}

const fetchMock = vi.fn<typeof fetch>();

describe("api client", () => {
  beforeEach(() => {
    fetchMock.mockReset();
    vi.stubGlobal("fetch", fetchMock);
    resetApiClientForTests();
    document.cookie = "tl_csrf=csrf-123; path=/";
    document.cookie = "tl_session_hint=1; path=/";
  });

  it("uses a same-origin path with credentials", async () => {
    fetchMock.mockResolvedValueOnce(jsonResponse({ items: [] }));

    await expect(api.get<{ items: unknown[] }>("/links")).resolves.toEqual({ items: [] });

    expect(fetchMock).toHaveBeenCalledWith(
      "/api/v1/links",
      expect.objectContaining({ credentials: "include", method: "GET" }),
    );
  });

  it("adds the CSRF header on mutations", async () => {
    fetchMock.mockResolvedValueOnce(jsonResponse({ code: "abc1234" }, 201));

    await api.post("/links", { url: "https://example.com" });

    const init = fetchMock.mock.calls[0]?.[1];
    expect(init?.method).toBe("POST");
    expect(new Headers(init?.headers).get("x-csrf-token")).toBe("csrf-123");
    expect(init?.body).toBe(JSON.stringify({ url: "https://example.com" }));
  });

  it("requests a CSRF token when the cookie is missing", async () => {
    document.cookie = "tl_csrf=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
    fetchMock
      .mockResolvedValueOnce(jsonResponse({ csrf_token: "fresh-token" }))
      .mockResolvedValueOnce(jsonResponse({ ok: true }, 201));

    await api.post("/links", { url: "https://example.com" });

    expect(fetchMock.mock.calls[0]?.[0]).toBe("/api/v1/auth/csrf");
    expect(new Headers(fetchMock.mock.calls[1]?.[1]?.headers).get("x-csrf-token")).toBe(
      "fresh-token",
    );
  });

  it("refreshes the session once on 401 and retries the request", async () => {
    fetchMock
      .mockResolvedValueOnce(
        jsonResponse({ error: { code: "unauthorized", message: "expired" } }, 401),
      )
      .mockResolvedValueOnce(jsonResponse({ user: { id: "1" } }))
      .mockResolvedValueOnce(jsonResponse({ items: ["ok"] }));

    await expect(api.get<{ items: string[] }>("/links")).resolves.toEqual({ items: ["ok"] });

    expect(fetchMock.mock.calls.map((call) => call[0])).toEqual([
      "/api/v1/links",
      "/api/v1/auth/refresh",
      "/api/v1/links",
    ]);
  });

  it("does not request a refresh without a session hint", async () => {
    document.cookie = "tl_session_hint=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
    fetchMock.mockResolvedValueOnce(
      jsonResponse({ error: { code: "unauthorized", message: "expired" } }, 401),
    );

    await expect(api.get("/links")).rejects.toMatchObject({ status: 401 });
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("does not refresh twice when the refresh fails", async () => {
    fetchMock
      .mockResolvedValueOnce(
        jsonResponse({ error: { code: "unauthorized", message: "expired" } }, 401),
      )
      .mockResolvedValueOnce(
        jsonResponse({ error: { code: "invalid_refresh", message: "no session" } }, 401),
      );

    await expect(api.get("/links")).rejects.toMatchObject({
      name: "ApiError",
      status: 401,
    });
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("exposes the standard error shape", async () => {
    fetchMock.mockResolvedValueOnce(
      jsonResponse({ error: { code: "invalid_url", message: "Invalid URL" } }, 400),
    );

    await expect(api.post("/links", { url: "nope" })).rejects.toMatchObject({
      code: "invalid_url",
      message: "Invalid URL",
      status: 400,
    });
  });

  it("reads Retry-After on 429", async () => {
    fetchMock.mockResolvedValueOnce(
      jsonResponse({ error: { code: "rate_limited", message: "slow down" } }, 429, {
        "retry-after": "7",
      }),
    );

    const error = await api.get("/links").catch((cause: unknown) => cause);

    expect(error).toBeInstanceOf(ApiError);
    expect(error).toMatchObject({ status: 429, code: "rate_limited", retryAfter: 7 });
  });

  it("handles non-JSON error responses", async () => {
    fetchMock.mockResolvedValueOnce(new Response("bad gateway", { status: 502 }));

    await expect(api.get("/links")).rejects.toMatchObject({
      status: 502,
      code: "request_failed",
    });
  });
});

describe("parseRetryAfter", () => {
  it("accepts delta seconds", () => {
    expect(parseRetryAfter("12")).toBe(12);
  });

  it("accepts an HTTP date", () => {
    const now = Date.parse("2026-01-01T00:00:00Z");
    const value = new Date(now + 5000).toUTCString();
    expect(parseRetryAfter(value, now)).toBe(5);
  });

  it("returns undefined for invalid values", () => {
    expect(parseRetryAfter(null)).toBeUndefined();
    expect(parseRetryAfter("soon")).toBeUndefined();
  });
});
