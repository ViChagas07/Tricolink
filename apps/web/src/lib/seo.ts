import { defaultLocale, locales } from "@/i18n/locales";

const PRIVATE_SEGMENTS = new Set(["login", "account", "links"]);
const PROTECTED_SEGMENTS = new Set(["account", "links"]);

export const siteUrl = (process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000").replace(
  /\/+$/,
  "",
);

export function localizedUrl(locale: string, path = ""): string {
  const normalized = path === "/" ? "" : path;
  return `${siteUrl}/${locale}${normalized}`;
}

export function languageAlternates(path = ""): Record<string, string> {
  const normalized = path === "/" ? "" : path;

  return {
    ...Object.fromEntries(locales.map((locale) => [locale, localizedUrl(locale, normalized)])),
    "x-default": localizedUrl(defaultLocale, normalized),
  };
}

function pathSegments(pathname: string): string[] {
  const segments = pathname.split("/").filter(Boolean);
  if (segments.length > 0 && (locales as readonly string[]).includes(segments[0])) {
    segments.shift();
  }
  return segments;
}

export function isPrivatePath(pathname: string): boolean {
  const segments = pathSegments(pathname);
  return segments.length > 0 && PRIVATE_SEGMENTS.has(segments[0]);
}

export function isProtectedPath(pathname: string): boolean {
  const segments = pathSegments(pathname);
  return segments.length > 0 && PROTECTED_SEGMENTS.has(segments[0]);
}
