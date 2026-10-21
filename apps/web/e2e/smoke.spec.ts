import { expect, test } from "@playwright/test";

import { localeLabels, locales } from "../src/i18n/locales";

test.describe("i18n routing", () => {
  test("redirects / to the detected locale", async ({ request }) => {
    const response = await request.get("/", {
      maxRedirects: 0,
      headers: { "accept-language": "pt-BR,pt;q=0.9,en;q=0.8" },
    });

    expect([307, 308]).toContain(response.status());
    expect(response.headers()["location"]).toMatch(/\/pt-BR$/);
  });

  test("falls back to English for unknown Accept-Language values", async ({ request }) => {
    const response = await request.get("/", {
      maxRedirects: 0,
      headers: { "accept-language": "xx-YY,xx;q=0.9" },
    });

    expect([307, 308]).toContain(response.status());
    expect(response.headers()["location"]).toMatch(/\/en$/);
  });

  test("switches all 11 locales while preserving the route", async ({ page }) => {
    for (const locale of locales) {
      await page.goto("/en");
      await expect(page.locator("html")).toHaveAttribute("lang", "en");

      if (locale !== "en") {
        const navigation = page.getByRole("navigation", { name: "Main navigation" });
        await navigation.getByRole("button", { name: /Select language/ }).click();
        await page.getByRole("option", { name: localeLabels[locale], exact: true }).click();
        await expect.poll(() => new URL(page.url()).pathname).toBe(`/${locale}`);
      }

      await expect(page.locator("html")).toHaveAttribute("lang", locale);
    }
  });

  test("short-link paths are not captured by the i18n middleware", async ({ page }) => {
    await page.goto("/zzzzzz9");

    expect(new URL(page.url()).pathname).toBe("/zzzzzz9");
    expect(page.url()).not.toContain("/en/zzzzzz9");
  });

  test("mobile menu exposes the same navigation", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto("/en");

    await page.getByRole("button", { name: "Open menu" }).click();
    const dialog = page.getByRole("dialog");
    await expect(dialog).toBeVisible();
    await expect(dialog.getByRole("link", { name: "Links" })).toBeVisible();
    await expect(dialog.getByRole("button", { name: /Select language/ })).toBeVisible();

    await dialog.getByRole("button", { name: "Close menu" }).click();
    await expect(dialog).not.toBeVisible();
  });

  test("Arabic renders RTL and the nonce-based CSP has no violations", async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on("console", (message) => {
      if (message.type() === "error") {
        consoleErrors.push(message.text());
      }
    });

    const response = await page.goto("/ar");
    await expect(page.locator("html")).toHaveAttribute("dir", "rtl");
    await expect(page.locator("html")).toHaveAttribute("lang", "ar");

    const csp = response?.headers()["content-security-policy"] ?? "";
    expect(csp).toContain("nonce-");
    expect(csp).toContain("frame-ancestors 'none'");
    expect(await page.locator("script[nonce]").count()).toBeGreaterThan(0);

    const cspErrors = consoleErrors.filter(
      (message) => message.includes("Content Security Policy") || message.includes("Refused to"),
    );
    expect(cspErrors).toEqual([]);
  });
});
