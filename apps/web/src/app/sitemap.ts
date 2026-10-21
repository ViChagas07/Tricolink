import type { MetadataRoute } from "next";

import { defaultLocale, locales } from "@/i18n/locales";
import { languageAlternates, localizedUrl } from "@/lib/seo";

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date();

  return locales.map((locale) => ({
    url: localizedUrl(locale),
    lastModified,
    changeFrequency: "weekly",
    priority: locale === defaultLocale ? 1 : 0.8,
    alternates: {
      languages: languageAlternates(),
    },
  }));
}
