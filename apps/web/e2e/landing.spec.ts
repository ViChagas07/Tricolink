import { expect, test } from "@playwright/test";

test.describe("landing page", () => {
  test("exposes localized SEO, structured data and the FAQ", async ({ page }) => {
    await page.goto("/en");

    await expect(page).toHaveTitle("Tricolink — Short links, clearly");
    await expect(
      page.getByRole("heading", { level: 1, name: "Short links, clearly." }),
    ).toBeVisible();
    await expect(page.getByRole("heading", { name: "Frequently asked questions" })).toBeVisible();
    await expect(page.locator("#faq details")).toHaveCount(8);
    await expect(page.getByText("Illustrative example")).toBeVisible();

    const canonical = await page.locator('link[rel="canonical"]').getAttribute("href");
    expect(canonical).toMatch(/\/en$/);

    await expect(page.locator('link[rel="alternate"][hreflang="pt-BR"]')).toHaveCount(1);
    await expect(page.locator('link[rel="alternate"][hreflang="x-default"]')).toHaveCount(1);
    const ogImage = await page.locator('meta[property="og:image"]').getAttribute("content");
    expect(ogImage).toContain("/opengraph-image");

    const raw = await page.locator('script[type="application/ld+json"]').textContent();
    expect(raw).toBeTruthy();
    const data = JSON.parse(raw as string) as {
      "@context": string;
      "@graph": Array<Record<string, unknown>>;
    };
    expect(data["@context"]).toBe("https://schema.org");
    expect(data["@graph"].map((node) => node["@type"])).toEqual(["WebApplication", "FAQPage"]);

    const faq = data["@graph"][1] as {
      mainEntity: Array<{ name: string; acceptedAnswer: { text: string } }>;
    };
    expect(faq.mainEntity).toHaveLength(8);
    expect(faq.mainEntity[0].name).toBe("What is Tricolink and how does it work?");
    expect(faq.mainEntity[0].acceptedAnswer.text.length).toBeGreaterThan(20);
  });

  test("loads the Recharts demo without layout shift when scrolled into view", async ({ page }) => {
    await page.goto("/en");
    const slot = page.locator("#demo-chart");
    await slot.scrollIntoViewIfNeeded();
    const chart = page.locator("#demo .recharts-surface");
    await expect(chart).toBeVisible({ timeout: 15_000 });

    const heightBefore = await slot.evaluate((node) => node.getBoundingClientRect().height);
    expect(heightBefore).toBeGreaterThan(200);
    await expect(page.locator("#demo-chart [aria-busy]")).toHaveAttribute("aria-busy", "false");
  });

  test("shortens a URL, copies it and opens the short link", async ({ page, context }) => {
    await context.grantPermissions(["clipboard-read", "clipboard-write"]);
    await page.goto("/en");

    await page.getByLabel("Long URL").fill("https://example.com/?from=tricolink-e2e");
    await page.getByRole("button", { name: "Shorten" }).click();

    await expect(page.getByText("Your short link is ready", { exact: true })).toBeVisible({
      timeout: 20_000,
    });
    const shortLink = page.locator('#shorten a[dir="ltr"]').first();
    await expect(shortLink).toHaveText(/^https?:\/\/.+\/.{7,}$/);
    const href = await shortLink.getAttribute("href");
    expect(href).toBeTruthy();

    await page.getByRole("button", { name: "Copy" }).click();
    await expect(page.getByRole("button", { name: "Copied!" })).toBeVisible();
    await expect.poll(() => page.evaluate(() => navigator.clipboard.readText())).toBe(href);

    const path = new URL(href as string).pathname;
    const redirect = await page.request.get(path, { maxRedirects: 0 });
    expect(redirect.status()).toBe(302);
    expect(redirect.headers()["location"]).toBe("https://example.com/?from=tricolink-e2e");
  });

  test("shows a translated inline error for an invalid URL", async ({ page }) => {
    await page.goto("/en");

    const input = page.getByLabel("Long URL");
    await input.fill("not-a-url");
    await page.getByRole("button", { name: "Shorten" }).click();

    await expect(page.locator("#shorten [role='alert']")).toHaveText(
      "Enter a valid http or https URL.",
    );
    await expect(input).toHaveAttribute("aria-invalid", "true");
    await expect(page.getByText("Your short link is ready", { exact: true })).toHaveCount(0);
  });

  test("serves llms.txt and the Open Graph image", async ({ request }) => {
    const llms = await request.get("/llms.txt");
    expect(llms.status()).toBe(200);
    expect(llms.headers()["content-type"]).toContain("text/plain");
    const body = await llms.text();
    expect(body).toContain("## Data policy");
    expect(body).toContain("HTTP 302");

    const image = await request.get("/opengraph-image");
    expect(image.status()).toBe(200);
    expect(image.headers()["content-type"]).toContain("image/png");
    expect((await image.body()).byteLength).toBeGreaterThan(10_000);
  });

  test("desktop layout fits a 1440px viewport", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto("/en");

    await expect(page.getByLabel("Long URL")).toBeVisible();
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    );
    expect(overflow).toBeLessThanOrEqual(1);
  });

  test("navigates the FAQ with the keyboard", async ({ page }) => {
    await page.goto("/en");

    const details = page.locator("#faq details");
    const second = details.nth(1);
    const third = details.nth(2);

    await expect(second).not.toHaveAttribute("open");
    await second.locator("summary").focus();
    await page.keyboard.press("Enter");
    await expect(second).toHaveAttribute("open");

    await page.keyboard.press("Tab");
    await expect(third.locator("summary")).toBeFocused();
    await page.keyboard.press("Enter");
    await expect(third).toHaveAttribute("open");
    await expect(second).not.toHaveAttribute("open");
  });

  test("Arabic RTL layout fits a 320px viewport", async ({ page }) => {
    await page.setViewportSize({ width: 320, height: 800 });
    await page.goto("/ar");

    await expect(page.locator("html")).toHaveAttribute("dir", "rtl");
    await expect(page).toHaveTitle("Tricolink — روابط قصيرة بوضوح");
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();

    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    );
    expect(overflow).toBeLessThanOrEqual(1);

    await page.getByRole("button", { name: "فتح القائمة" }).click();
    await expect(page.getByRole("dialog")).toBeVisible();
    await page.getByRole("button", { name: "إغلاق القائمة" }).click();
  });
});
