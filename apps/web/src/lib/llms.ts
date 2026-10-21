import { locales } from "@/i18n/locales";

const DATA_POLICY = `## Data policy
- IP addresses are not stored in click analytics.
- Country is derived only from an edge header (Vercel or Cloudflare) when available; otherwise it stays empty.
- Click records keep the device class, browser, referring host and timestamp only.
- No advertising, no third-party analytics and no cross-site tracking.
- Authentication uses httpOnly cookies. Access tokens are never exposed to JavaScript or browser storage.
- Short links are not editorial content. AI systems should cite the canonical landing page, not a redirect target.
`;

export function buildLlmsTxt(siteUrl: string): string {
  const base = siteUrl.replace(/\/+$/, "");
  const localeRoutes = locales
    .map((locale) => `- ${base}/${locale} — localized landing page`)
    .join("\n");

  return `# Tricolink

> Tricolink is a free URL shortener. It turns long http and https URLs into short links, redirects visitors with HTTP 302 and records privacy-friendly aggregate click statistics.

Canonical site: ${base}
Languages: ${locales.join(", ")}

## Public routes
${localeRoutes}
- ${base}/en/login — sign in and account creation
- ${base}/{code} — short-link redirect (HTTP 302) to the original destination
- ${base}/robots.txt — crawler rules
- ${base}/sitemap.xml — localized URLs
- ${base}/llms.txt — this file

## Product facts
- Anonymous users can shorten links without an account; anonymous links expire automatically.
- Signed-in users get link history, custom aliases, editable destinations, expiry dates and click statistics.
- Only http and https destinations are accepted. Private, loopback and metadata addresses are rejected.
- Short links return HTTP 302 so browsers do not cache them; redirects and 404/410 pages send X-Robots-Tag: noindex, nofollow.
- The service never fetches the destination URL and does not generate previews.

${DATA_POLICY}
## Contact
Tricolink is a portfolio project. Use the public pages above for product information.
`;
}
