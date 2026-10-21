import type { Metadata } from "next";
import { headers } from "next/headers";
import { notFound } from "next/navigation";
import { getTranslations } from "next-intl/server";

import { DemoDashboard } from "@/components/dashboard/demo-dashboard";
import { Faq, type FaqEntry } from "@/components/landing/faq";
import { FeatureBlocks } from "@/components/landing/feature-blocks";
import { FinalCta } from "@/components/landing/final-cta";
import { HeroSection } from "@/components/landing/hero";
import { defaultLocale, isLocale } from "@/i18n/locales";
import { languageAlternates, localizedUrl, siteUrl } from "@/lib/seo";
import { buildLandingStructuredData, serializeStructuredData } from "@/lib/structured-data";

type HomePageProps = {
  params: Promise<{ locale: string }>;
};

export async function generateMetadata({ params }: HomePageProps): Promise<Metadata> {
  const { locale: rawLocale } = await params;
  const locale = isLocale(rawLocale) ? rawLocale : defaultLocale;
  const t = await getTranslations({ locale, namespace: "meta" });
  const title = t("homeTitle");
  const description = t("homeDescription");
  const ogAlt = t("ogAlt");

  return {
    metadataBase: new URL(siteUrl),
    title: { absolute: title },
    description,
    alternates: {
      canonical: `/${locale}`,
      languages: languageAlternates(),
    },
    openGraph: {
      type: "website",
      siteName: "Tricolink",
      url: `/${locale}`,
      title,
      description,
      locale: locale.replace("-", "_"),
      images: [
        {
          url: "/opengraph-image",
          width: 1200,
          height: 630,
          alt: ogAlt,
        },
      ],
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [{ url: "/opengraph-image", alt: ogAlt }],
    },
    robots: { index: true, follow: true },
  };
}

export default async function HomePage({ params }: HomePageProps) {
  const { locale } = await params;
  if (!isLocale(locale)) {
    notFound();
  }

  const [meta, faq, features] = await Promise.all([
    getTranslations({ locale, namespace: "meta" }),
    getTranslations({ locale, namespace: "faq" }),
    getTranslations({ locale, namespace: "features" }),
  ]);

  const faqItems: FaqEntry[] = Array.from({ length: 8 }, (_, index) => ({
    question: faq(`q${index + 1}`),
    answer: faq(`a${index + 1}`),
  }));

  const structuredData = buildLandingStructuredData({
    name: "Tricolink",
    description: meta("homeDescription"),
    url: localizedUrl(locale),
    locale,
    faq: faqItems,
    features: [features("shortTitle"), features("statsTitle"), features("controlTitle")],
  });
  const nonce = (await headers()).get("x-nonce") ?? undefined;

  return (
    <>
      <script type="application/ld+json" nonce={nonce}>
        {serializeStructuredData(structuredData)}
      </script>
      <HeroSection />
      <DemoDashboard />
      <FeatureBlocks />
      <Faq title={faq("title")} subtitle={faq("subtitle")} items={faqItems} />
      <FinalCta />
    </>
  );
}
