import { expect, test } from "@playwright/test";

const password = "E2e-correct-horse-42";

function uniqueEmail(): string {
  const suffix = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  return `e2e-${suffix}@example.com`;
}

test.describe("authenticated pages", () => {
  test.beforeEach(async ({ context }) => {
    await context.route("**/api/v1/**", async (route) => {
      const response = await route.fetch({
        headers: {
          ...route.request().headers(),
          origin: "http://localhost:3001",
        },
      });
      await route.fulfill({ response });
    });
  });

  test("registers, creates, edits, copies and deletes a link, then logs out", async ({
    page,
    context,
  }) => {
    await context.grantPermissions(["clipboard-read", "clipboard-write"]);
    const email = uniqueEmail();
    const destination = `https://example.com/e2e-${Date.now()}`;
    const editedDestination = `https://example.org/edited-${Date.now()}`;

    await page.goto("/en/login");
    await page.getByRole("tab", { name: "Create account" }).click();
    await page.getByLabel("Email").fill(email);
    await page.getByLabel("Password", { exact: true }).fill(password);
    await page.evaluate(() => {
      (window as Window & { __tricolinkNoReload?: boolean }).__tricolinkNoReload = true;
    });
    await page.getByRole("button", { name: "Create account" }).click();

    await expect(page).toHaveURL(/\/en\/links$/, { timeout: 30_000 });
    await expect(page.getByRole("heading", { name: "Your links" })).toBeVisible();
    await expect(page.getByText("No links yet")).toBeVisible();
    expect(
      await page.evaluate(
        () => (window as Window & { __tricolinkNoReload?: boolean }).__tricolinkNoReload,
      ),
    ).toBe(true);
    await expect(
      page.getByRole("navigation", { name: "Main navigation" }).getByRole("link", {
        name: "Sign in",
      }),
    ).toHaveCount(0);

    await page.goto("/en");
    await page.getByLabel("Long URL").fill(destination);
    await page.getByRole("button", { name: "Shorten" }).click();
    await expect(page.getByText("Your short link is ready", { exact: true })).toBeVisible({
      timeout: 20_000,
    });

    const shortLink = page.locator('#shorten a[dir="ltr"]').first();
    const shortHref = await shortLink.getAttribute("href");
    expect(shortHref).toBeTruthy();
    const code = new URL(shortHref as string).pathname.replace(/^\//, "");
    expect(code.length).toBeGreaterThanOrEqual(7);

    await page.goto("/en/links");
    await expect(page.getByRole("link", { name: `Open details: ${code}` })).toBeVisible({
      timeout: 20_000,
    });
    await expect(page.getByTitle(destination)).toBeVisible();
    await expect(page.getByText("Clicks in the last 30 days")).toBeVisible();
    await expect(page.getByText("1 link", { exact: true })).toBeVisible();

    await page.getByRole("button", { name: `Edit: ${code}` }).click();
    const editDialog = page.getByRole("dialog");
    await expect(editDialog.getByLabel("Short code")).toHaveValue(code);
    await expect(editDialog.getByLabel("Short code")).toHaveAttribute("readonly", "");
    await editDialog.getByLabel("Destination URL").fill(editedDestination);
    await editDialog.getByRole("button", { name: "Save changes" }).click();

    await expect(page.getByTitle(editedDestination)).toBeVisible({ timeout: 20_000 });

    const xssTitle = '<img src=x onerror="window.__xss=1">';
    await page.getByRole("button", { name: `Edit: ${code}` }).click();
    await page.getByRole("dialog").getByLabel("Title").fill(xssTitle);
    await page.getByRole("dialog").getByRole("button", { name: "Save changes" }).click();
    await expect(page.getByText(xssTitle, { exact: true })).toBeVisible({ timeout: 20_000 });
    expect(await page.evaluate(() => (window as Window & { __xss?: number }).__xss)).toBeUndefined();
    await expect(page.locator('img[src="x"]')).toHaveCount(0);

    await page.getByRole("link", { name: `Open details: ${code}` }).click();
    await expect(page.getByRole("heading", { name: xssTitle })).toBeVisible({ timeout: 20_000 });
    expect(await page.evaluate(() => (window as Window & { __xss?: number }).__xss)).toBeUndefined();
    await expect(page.locator('img[src="x"]')).toHaveCount(0);

    const externalAnchors = page.locator('a[target="_blank"]');
    for (let index = 0; index < (await externalAnchors.count()); index += 1) {
      const anchor = externalAnchors.nth(index);
      expect(await anchor.getAttribute("href")).toMatch(/^https?:\/\//);
      expect(await anchor.getAttribute("rel")).toContain("noopener");
      expect(await anchor.getAttribute("rel")).toContain("noreferrer");
    }
    await page.goto("/en/links");

    await page.getByRole("button", { name: `Copy: ${code}` }).click();
    await expect.poll(() => page.evaluate(() => navigator.clipboard.readText())).toBe(shortHref);

    await test.step("shows clicks in the statistics after the flush", async () => {
      for (let index = 0; index < 5; index += 1) {
        const redirect = await page.request.get(`/${code}`, { maxRedirects: 0 });
        expect(redirect.status()).toBe(302);
      }

      await expect
        .poll(
          async () => {
            const response = await page.request.get(`/api/v1/links/${code}`);
            if (!response.ok()) {
              return -1;
            }
            const payload = (await response.json()) as { click_count?: number };
            return payload.click_count ?? -1;
          },
          { timeout: 20_000 },
        )
        .toBeGreaterThanOrEqual(5);

      await page.goto(`/en/links/${code}`);
      const stats = page.getByRole("region", { name: "Clicks over time" });
      await expect(stats.getByTestId("stats-total")).toHaveText("5");

      const chart = stats.getByRole("table", { name: /Clicks per day/ });
      await expect(chart.getByRole("cell", { name: "5", exact: true })).toHaveCount(1);

      const countries = stats.getByRole("table", { name: "Countries" });
      await expect(countries.getByRole("rowheader", { name: "Other" })).toBeVisible();
      await expect(countries.getByRole("cell", { name: "5", exact: true })).toBeVisible();

      const referrers = stats.getByRole("table", { name: "Sources" });
      await expect(referrers.getByRole("rowheader", { name: "Direct" })).toBeVisible();

      const devices = stats.getByRole("table", { name: "Devices" });
      await expect(devices.getByRole("cell", { name: "5", exact: true })).toBeVisible();

      await stats.getByRole("button", { name: "7 days" }).click();
      await expect(stats.getByRole("button", { name: "7 days" })).toHaveAttribute(
        "aria-pressed",
        "true",
      );
      await expect(stats.getByTestId("stats-total")).toHaveText("5");

      await page.goto("/en/links");
    });

    const storage = await page.evaluate(() => ({
      local: { ...window.localStorage },
      session: { ...window.sessionStorage },
    }));
    expect(JSON.stringify(storage)).not.toMatch(/eyJ|access_token|refresh_token/i);

    const cookies = await context.cookies();
    const sessionCookies = cookies.filter((cookie) => /tl_(access|refresh)$/.test(cookie.name));
    expect(sessionCookies).toHaveLength(2);
    expect(sessionCookies.every((cookie) => cookie.httpOnly)).toBe(true);

    await page.getByRole("button", { name: `Delete: ${code}` }).click();
    await page.getByRole("dialog").getByRole("button", { name: "Delete link" }).click();
    await expect(page.getByRole("link", { name: `Open details: ${code}` })).toHaveCount(0);
    await expect(page.getByText("No links yet")).toBeVisible();

    await page.goto("/en/account");
    await page.getByLabel("Display name").fill("E2E Tester");
    await page.getByRole("button", { name: "Save changes" }).click();
    await expect(page.getByRole("status")).toContainText("Changes saved.");

    await page.getByRole("button", { name: "Dark" }).click();
    await expect(page.locator("html")).toHaveClass(/dark/);
    await page.getByRole("button", { name: "Light" }).click();
    await expect(page.locator("html")).not.toHaveClass(/dark/);

    await page.locator("select").selectOption("pt-BR");
    await expect(page).toHaveURL(/\/pt-BR\/account$/, { timeout: 15_000 });
    await page.locator("select").selectOption("en");
    await expect(page).toHaveURL(/\/en\/account$/, { timeout: 15_000 });

    await page.evaluate(() => {
      (window as Window & { __tricolinkNoReload?: boolean }).__tricolinkNoReload = true;
    });
    await page.getByRole("button", { name: "Sign out" }).click();
    await expect(page).toHaveURL(/\/en$/, { timeout: 15_000 });
    expect(
      await page.evaluate(
        () => (window as Window & { __tricolinkNoReload?: boolean }).__tricolinkNoReload,
      ),
    ).toBe(true);
    await expect(
      page.getByRole("navigation", { name: "Main navigation" }).getByRole("link", {
        name: "Sign in",
      }),
    ).toBeVisible();

    const me = await page.request.get("/api/v1/auth/me");
    expect(me.status()).toBe(401);
  });

  test("guards private pages and ignores an external next target", async ({ page, context }) => {
    const email = uniqueEmail();
    const registered = await page.request.post("/api/v1/auth/register", {
      data: { email, password },
    });
    expect(registered.status()).toBe(202);

    await page.goto("/en/links");
    await expect(page).toHaveURL(/\/en\/login\?next=%2Fen%2Flinks$/, { timeout: 15_000 });

    await page.getByLabel("Email").fill(email);
    await page.getByLabel("Password", { exact: true }).fill(password);
    await page.getByRole("button", { name: "Sign in" }).click();
    await expect(page).toHaveURL(/\/en\/links$/, { timeout: 30_000 });

    await context.clearCookies();
    await page.goto("/en/login?next=https%3A%2F%2Fevil.com");
    await page.getByLabel("Email").fill(email);
    await page.getByLabel("Password", { exact: true }).fill(password);
    await page.getByRole("button", { name: "Sign in" }).click();

    await expect(page).toHaveURL(/\/en\/links$/, { timeout: 30_000 });
    await expect(page).not.toHaveURL(/evil\.com/);
  });

  test("shows the wait time when login is rate limited", async ({ page }) => {
    await page.route("**/api/v1/auth/login", async (route) => {
      await route.fulfill({
        status: 429,
        headers: {
          "content-type": "application/json",
          "retry-after": "30",
        },
        body: JSON.stringify({
          error: { code: "too_many_attempts", message: "Too many attempts" },
        }),
      });
    });

    await page.goto("/en/login");
    await page.getByLabel("Email").fill("rate-limited@example.com");
    await page.getByLabel("Password", { exact: true }).fill(password);
    await page.getByRole("button", { name: "Sign in" }).click();

    const alert = page.getByRole("alert").filter({ hasText: "Too many attempts" });
    await expect(alert).toBeVisible();
    await expect(alert).toContainText(/Try again in \d+ seconds/);
    await expect(page.getByRole("button", { name: "Sign in" })).toBeDisabled();
  });
});
