import { defaultLocale, isLocale, locales, type Locale } from "@/i18n/locales";

const CONTROL_CHARACTERS = /[\u0000-\u001f\u007f]/;
const DEFAULT_NEXT = "/links";

function decodePath(value: string): string | null {
  try {
    return decodeURIComponent(value);
  } catch {
    return null;
  }
}

export function isSafeNextPath(value: string | null | undefined): value is string {
  if (!value || !value.startsWith("/") || value.startsWith("//")) {
    return false;
  }
  if (value.includes("\\") || CONTROL_CHARACTERS.test(value)) {
    return false;
  }

  const decoded = decodePath(value);
  if (!decoded || decoded.startsWith("//") || decoded.includes("\\")) {
    return false;
  }
  if (CONTROL_CHARACTERS.test(decoded)) {
    return false;
  }

  try {
    const parsed = new URL(decoded, "http://tricolink.invalid");
    return parsed.origin === "http://tricolink.invalid" && !parsed.username && !parsed.password;
  } catch {
    return false;
  }
}

export function sanitizeNextPath(
  value: string | null | undefined,
  fallback = DEFAULT_NEXT,
): string {
  return isSafeNextPath(value) ? value : fallback;
}

export type LocalizedTarget = {
  path: string;
  locale?: Locale;
};

export function toNavigationTarget(next: string, currentLocale: string): LocalizedTarget {
  const safeNext = sanitizeNextPath(next);
  const current = isLocale(currentLocale) ? currentLocale : defaultLocale;

  for (const locale of locales) {
    if (
      safeNext === `/${locale}` ||
      safeNext.startsWith(`/${locale}/`) ||
      safeNext.startsWith(`/${locale}?`) ||
      safeNext.startsWith(`/${locale}#`)
    ) {
      const rest = safeNext.slice(locale.length + 1);
      if (!rest) {
        return { path: "/", locale };
      }
      return {
        path: rest.startsWith("?") || rest.startsWith("#") ? `/${rest}` : rest,
        locale,
      };
    }
  }

  return { path: safeNext, locale: current };
}

export function toLocalizedServerPath(locale: string, next: string): string {
  const target = toNavigationTarget(next, locale);
  const targetLocale = target.locale ?? (isLocale(locale) ? locale : defaultLocale);
  if (target.path === "/") {
    return `/${targetLocale}`;
  }
  return `/${targetLocale}${target.path.startsWith("/") ? target.path : `/${target.path}`}`;
}

export function isLoginPath(value: string): boolean {
  const target = toNavigationTarget(value, defaultLocale);
  return target.path === "/login" || target.path.startsWith("/login/");
}
