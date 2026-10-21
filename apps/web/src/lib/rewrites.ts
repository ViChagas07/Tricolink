import { locales } from "../i18n/locales";

export type RewriteRule = {
  source: string;
  destination: string;
};

export type RewritesConfig = {
  beforeFiles: RewriteRule[];
  afterFiles: RewriteRule[];
  fallback: RewriteRule[];
};

const RESERVED_TOP_LEVEL = [
  ...locales,
  "api",
  "r",
  "login",
  "account",
  "links",
  "admin",
  "static",
  "_next",
  "favicon.ico",
  "robots.txt",
  "sitemap.xml",
  "llms.txt",
];

const RESERVED_PATTERN = RESERVED_TOP_LEVEL.map((value) =>
  value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
).join("|");

const CODE_PATTERN = "[A-Za-z0-9_-]{3,32}";

export const SHORT_CODE_SOURCE = `/:code((?!(?:${RESERVED_PATTERN})$)[A-Za-z0-9_-]{3,32})`;

export function isShortCodePath(pathname: string): boolean {
  if (!pathname.startsWith("/") || pathname.includes("?") || pathname.includes("#")) {
    return false;
  }

  const segment = pathname.slice(1);
  if (segment.includes("/") || !new RegExp(`^${CODE_PATTERN}$`).test(segment)) {
    return false;
  }

  return !RESERVED_TOP_LEVEL.includes(segment);
}

export function buildRewrites(apiInternalUrl: string): RewritesConfig {
  const base = apiInternalUrl.replace(/\/+$/, "");

  return {
    beforeFiles: [
      {
        source: "/api/v1/:path*",
        destination: `${base}/api/v1/:path*`,
      },
    ],
    afterFiles: [
      {
        source: SHORT_CODE_SOURCE,
        destination: `${base}/api/v1/r/:code`,
      },
    ],
    fallback: [
      {
        source: "/:code",
        destination: `${base}/api/v1/r/:code`,
      },
    ],
  };
}
