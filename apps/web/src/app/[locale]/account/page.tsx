import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getTranslations } from "next-intl/server";

import { AccountForm } from "@/components/account/account-form";
import { defaultLocale, isLocale } from "@/i18n/locales";
import { requireUser } from "@/lib/server-api";

type AccountPageProps = {
  params: Promise<{ locale: string }>;
};

export async function generateMetadata({ params }: AccountPageProps): Promise<Metadata> {
  const { locale: rawLocale } = await params;
  const locale = isLocale(rawLocale) ? rawLocale : defaultLocale;
  const t = await getTranslations({ locale, namespace: "account" });
  return {
    title: t("title"),
    robots: { index: false, follow: false },
  };
}

export default async function AccountPage({ params }: AccountPageProps) {
  const { locale: rawLocale } = await params;
  if (!isLocale(rawLocale)) {
    notFound();
  }

  const user = await requireUser(rawLocale, `/${rawLocale}/account`);
  return <AccountForm initialUser={user} />;
}
