import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getTranslations } from "next-intl/server";

import { buttonVariants } from "@/components/ui/button";
import { Link } from "@/i18n/navigation";
import { defaultLocale, isLocale } from "@/i18n/locales";
import { languageAlternates } from "@/lib/seo";
import { cn } from "@/lib/utils";

type HomePageProps = {
  params: Promise<{ locale: string }>;
};

export async function generateMetadata({ params }: HomePageProps): Promise<Metadata> {
  const { locale: rawLocale } = await params;
  const locale = isLocale(rawLocale) ? rawLocale : defaultLocale;
  const t = await getTranslations({ locale, namespace: "meta" });

  return {
    title: t("homeTitle"),
    description: t("homeDescription"),
    alternates: {
      canonical: `/${locale}`,
      languages: languageAlternates(),
    },
    openGraph: {
      url: `/${locale}`,
      title: t("homeTitle"),
      description: t("homeDescription"),
      locale: locale.replace("-", "_"),
    },
  };
}

export default async function HomePage({ params }: HomePageProps) {
  const { locale } = await params;
  if (!isLocale(locale)) {
    notFound();
  }

  const t = await getTranslations({ locale, namespace: "hero" });

  return (
    <section className="mx-auto flex w-full max-w-3xl flex-col items-center px-4 py-20 text-center sm:px-6 sm:py-28">
      <p className="text-xs font-semibold uppercase tracking-[0.28em] text-tc-blue-700 dark:text-tc-blue-100">
        Tricolink
      </p>
      <h1 className="mt-4 max-w-2xl text-balance font-heading text-4xl font-bold tracking-tight text-tc-blue-950 sm:text-5xl dark:text-tc-white">
        {t("title")}
      </h1>
      <p className="mt-5 max-w-xl text-pretty text-base leading-relaxed text-muted-foreground sm:text-lg">
        {t("subtitle")}
      </p>
      <Link
        href="/login"
        className={cn(buttonVariants({ variant: "brand", size: "lg" }), "mt-8 h-11 px-6 text-base")}
      >
        {t("cta")}
      </Link>
    </section>
  );
}
