import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getTranslations } from "next-intl/server";

import { LinksView } from "@/components/links/links-view";
import { defaultLocale, isLocale } from "@/i18n/locales";
import { getServerLinks, requireUser } from "@/lib/server-api";

type LinksPageProps = {
  params: Promise<{ locale: string }>;
};

export async function generateMetadata({ params }: LinksPageProps): Promise<Metadata> {
  const { locale: rawLocale } = await params;
  const locale = isLocale(rawLocale) ? rawLocale : defaultLocale;
  const t = await getTranslations({ locale, namespace: "links" });
  return {
    title: t("title"),
    robots: { index: false, follow: false },
  };
}

export default async function LinksPage({ params }: LinksPageProps) {
  const { locale: rawLocale } = await params;
  if (!isLocale(rawLocale)) {
    notFound();
  }

  await requireUser(rawLocale, `/${rawLocale}/links`);
  const { page, summary } = await getServerLinks();

  return <LinksView initialPage={page} initialSummary={summary} />;
}
