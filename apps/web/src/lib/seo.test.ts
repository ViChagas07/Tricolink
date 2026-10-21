import { describe, expect, it } from "vitest";

import { isPrivatePath, languageAlternates } from "./seo";

describe("isPrivatePath", () => {
  it("marks login, account and links pages as private for every locale", () => {
    for (const path of [
      "/login",
      "/en/login",
      "/pt-BR/account",
      "/ar/links",
      "/zh-CN/links/abc1234",
      "/es/links/abc1234/stats",
    ]) {
      expect(isPrivatePath(path)).toBe(true);
    }
  });

  it("keeps the landing page and short links indexable", () => {
    for (const path of ["/", "/en", "/pt-BR/", "/abc1234", "/en/llms.txt", "/llms.txt"]) {
      expect(isPrivatePath(path)).toBe(false);
    }
  });
});

describe("languageAlternates", () => {
  it("includes every locale plus x-default", () => {
    const alternates = languageAlternates();
    expect(Object.keys(alternates)).toHaveLength(12);
    expect(alternates.en).toMatch(/\/en$/);
    expect(alternates["x-default"]).toMatch(/\/en$/);
  });
});
