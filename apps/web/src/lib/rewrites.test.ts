import { describe, expect, it } from "vitest";

import { buildRewrites, isShortCodePath, SHORT_CODE_SOURCE } from "./rewrites";

describe("buildRewrites", () => {
  const rewrites = buildRewrites("http://api:8000/");

  it("proxies the public API through the frontend origin", () => {
    expect(rewrites.beforeFiles).toContainEqual({
      source: "/api/v1/:path*",
      destination: "http://api:8000/api/v1/:path*",
    });
  });

  it("keeps the short-link fallback required by CONTEXT §7", () => {
    expect(rewrites.fallback).toContainEqual({
      source: "/:code",
      destination: "http://api:8000/api/v1/r/:code",
    });
  });

  it("resolves short codes before the dynamic [locale] route", () => {
    expect(rewrites.afterFiles).toContainEqual({
      source: SHORT_CODE_SOURCE,
      destination: "http://api:8000/api/v1/r/:code",
    });
  });
});

describe("isShortCodePath", () => {
  it("accepts valid codes", () => {
    expect(isShortCodePath("/abc1234")).toBe(true);
    expect(isShortCodePath("/My_Alias-9")).toBe(true);
  });

  it("rejects locales and app routes", () => {
    for (const path of [
      "/en",
      "/pt-BR",
      "/zh-CN",
      "/login",
      "/account",
      "/links",
      "/api",
      "/r",
      "/robots.txt",
      "/sitemap.xml",
    ]) {
      expect(isShortCodePath(path)).toBe(false);
    }
  });

  it("rejects nested paths, short segments and invalid characters", () => {
    expect(isShortCodePath("/abc/def")).toBe(false);
    expect(isShortCodePath("/ab")).toBe(false);
    expect(isShortCodePath("/abc def")).toBe(false);
    expect(isShortCodePath("/abc?x=1")).toBe(false);
  });
});
