import { execFileSync } from "node:child_process";
import { join } from "node:path";

import { describe, expect, it } from "vitest";

import { defaultLocale, locales } from "./locales";

describe("i18n configuration", () => {
  it("ships the 11 locales from CONTEXT §8 with en as default", () => {
    expect(locales).toEqual([
      "pt-BR",
      "en",
      "es",
      "fr",
      "de",
      "it",
      "ja",
      "ko",
      "zh-CN",
      "ru",
      "ar",
    ]);
    expect(defaultLocale).toBe("en");
  });

  it("passes pnpm i18n:check", () => {
    const appRoot = process.cwd();
    const script = join(appRoot, "scripts", "i18n-check.mjs");

    const output = execFileSync(
      process.execPath,
      ["--disable-warning=MODULE_TYPELESS_PACKAGE_JSON", script],
      {
        cwd: appRoot,
        encoding: "utf8",
      },
    );

    expect(output).toContain("i18n:check ok");
  }, 15_000);
});
