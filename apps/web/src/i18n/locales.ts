export const locales = [
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
] as const;

export type Locale = (typeof locales)[number];

export const defaultLocale: Locale = "en";

export const localeLabels: Record<Locale, string> = {
  "pt-BR": "Português (Brasil)",
  en: "English",
  es: "Español",
  fr: "Français",
  de: "Deutsch",
  it: "Italiano",
  ja: "日本語",
  ko: "한국어",
  "zh-CN": "简体中文",
  ru: "Русский",
  ar: "العربية",
};

export function isLocale(value: string | undefined | null): value is Locale {
  return typeof value === "string" && (locales as readonly string[]).includes(value);
}

export function getDirection(locale: string): "ltr" | "rtl" {
  return locale === "ar" ? "rtl" : "ltr";
}
