import { defaultLocale, locales } from "@/i18n/locales";

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
