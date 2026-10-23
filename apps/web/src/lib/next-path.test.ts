import { describe, expect, it } from "vitest";

import {
  isSafeNextPath,
  sanitizeNextPath,
  toLocalizedServerPath,
  toNavigationTarget,
} from "./next-path";

describe("next path validation", () => {
  it("accepts internal paths", () => {
    expect(isSafeNextPath("/links")).toBe(true);
    expect(isSafeNextPath("/en/links/abc123?tab=1")).toBe(true);
    expect(sanitizeNextPath("/pt-BR/account")).toBe("/pt-BR/account");
  });

  it("rejects external and scheme-relative targets", () => {
    expect(isSafeNextPath("https://evil.com")).toBe(false);
    expect(isSafeNextPath("//evil.com")).toBe(false);
    expect(isSafeNextPath("/\\evil.com")).toBe(false);
    expect(isSafeNextPath("/%2F%2Fevil.com")).toBe(false);
    expect(isSafeNextPath("/%5Cevil.com")).toBe(false);
    expect(isSafeNextPath("javascript:alert(1)")).toBe(false);
    expect(isSafeNextPath("links")).toBe(false);
  });

  it("falls back to the home destination", () => {
    expect(sanitizeNextPath("https://evil.com")).toBe("/");
    expect(sanitizeNextPath(null)).toBe("/");
    expect(sanitizeNextPath("", "/account")).toBe("/account");
  });

  it("splits a locale prefix into a navigation target", () => {
    expect(toNavigationTarget("/en/links", "en")).toEqual({ path: "/links", locale: "en" });
    expect(toNavigationTarget("/links", "pt-BR")).toEqual({
      path: "/links",
      locale: "pt-BR",
    });
    expect(toNavigationTarget("/fr/account", "en")).toEqual({
      path: "/account",
      locale: "fr",
    });
  });

  it("localizes server redirects", () => {
    expect(toLocalizedServerPath("pt-BR", "/links")).toBe("/pt-BR/links");
    expect(toLocalizedServerPath("fr", "/en/links")).toBe("/en/links");
    expect(toLocalizedServerPath("en", "/")).toBe("/en");
  });
});
