import { expect, test } from "@playwright/test";

test.describe("security headers and untrusted input", () => {
  test("serves the production CSP and hardening headers", async ({ request }) => {
    const response = await request.get("/en");
    expect(response.status()).toBe(200);

    const headers = response.headers();
    const csp = headers["content-security-policy"];
    expect(csp).toBeTruthy();
    expect(csp).toContain("default-src 'self'");
    expect(csp).toContain("frame-ancestors 'none'");
    expect(csp).toContain("base-uri 'none'");
    expect(csp).toContain("form-action 'self'");
    expect(csp).toContain("object-src 'none'");
    expect(csp).toContain("style-src-attr 'unsafe-inline'");

    const scriptSrc = csp
      .split(";")
      .map((directive) => directive.trim())
      .find((directive) => directive.startsWith("script-src"));
    expect(scriptSrc).toBeTruthy();
    expect(scriptSrc).toContain("'nonce-");
    expect(scriptSrc).toContain("'strict-dynamic'");
    expect(scriptSrc).not.toContain("'unsafe-inline'");
    expect(scriptSrc).not.toContain("'unsafe-eval'");

    expect(headers["strict-transport-security"]).toContain("max-age=63072000");
    expect(headers["x-content-type-options"]).toBe("nosniff");
    expect(headers["x-frame-options"]).toBe("DENY");
    expect(headers["referrer-policy"]).toBe("strict-origin-when-cross-origin");
    expect(headers["cross-origin-opener-policy"]).toBe("same-origin");
    expect(headers["permissions-policy"]).toContain("camera=()");
    expect(headers["x-powered-by"]).toBeUndefined();
  });

  test("does not execute script payloads placed in the URL or query", async ({ page }) => {
    let dialogOpened = false;
    page.on("dialog", async (dialog) => {
      dialogOpened = true;
      await dialog.dismiss();
    });

    await page.goto("/en?q=%3Cscript%3Ewindow.__xss%3D1%3C%2Fscript%3E");
    expect(await page.evaluate(() => (window as Window & { __xss?: number }).__xss)).toBeUndefined();

    await page.goto(
      "/en/login?next=%3Cimg%20src%3Dx%20onerror%3D%22window.__xss%3D1%22%3E",
    );
    await expect(page).toHaveURL(/\/en\/login/);
    expect(await page.evaluate(() => (window as Window & { __xss?: number }).__xss)).toBeUndefined();
    expect(dialogOpened).toBe(false);
    await expect(page.locator('img[src="x"]')).toHaveCount(0);
    await expect(page.locator('img[onerror*="__xss"]')).toHaveCount(0);
  });

  test("rejects javascript: and data: destinations without executing them", async ({ page }) => {
    let dialogOpened = false;
    page.on("dialog", async (dialog) => {
      dialogOpened = true;
      await dialog.dismiss();
    });

    for (const value of [
      "javascript:alert(1)",
      "data:text/html,<script>alert(1)</script>",
    ]) {
      await page.goto("/en");
      await page.getByLabel("Long URL").fill(value);
      await page.getByRole("button", { name: "Shorten" }).click();

      await expect(page.locator('[role="alert"][id$="-error"]')).toBeVisible();
      await expect(page).toHaveURL(/\/en$/);
    }

    expect(dialogOpened).toBe(false);
    expect(await page.evaluate(() => (window as Window & { __xss?: number }).__xss)).toBeUndefined();
  });
});
