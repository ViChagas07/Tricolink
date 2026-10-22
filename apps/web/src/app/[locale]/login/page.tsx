import type { Metadata } from "next";
import { notFound, redirect } from "next/navigation";
import { getTranslations } from "next-intl/server";

import { LoginForm } from "@/components/auth/login-form";
import { defaultLocale, isLocale } from "@/i18n/locales";
import { isLoginPath, sanitizeNextPath, toLocalizedServerPath } from "@/lib/next-path";
import { getServerUser } from "@/lib/server-api";

type LoginPageProps = {
  params: Promise<{ locale: string }>;
  searchParams: Promise<Record<string, string | string[] | undefined>>;
};

function first(value: string | string[] | undefined): string | null {
  if (Array.isArray(value)) {
    return value[0] ?? null;
  }
  return value ?? null;
}

export async function generateMetadata({ params }: LoginPageProps): Promise<Metadata> {
  const { locale: rawLocale } = await params;
  const locale = isLocale(rawLocale) ? rawLocale : defaultLocale;
  const t = await getTranslations({ locale, namespace: "auth" });
  return {
    title: t("loginTitle"),
    robots: { index: false, follow: false },
  };
}

export default async function LoginPage({ params, searchParams }: LoginPageProps) {
  const { locale: rawLocale } = await params;
  if (!isLocale(rawLocale)) {
    notFound();
  }

  const query = await searchParams;
  const safeNext = sanitizeNextPath(first(query.next), "/links");
  const nextPath = toLocalizedServerPath(rawLocale, isLoginPath(safeNext) ? "/links" : safeNext);

  const user = await getServerUser();
  if (user) {
    redirect(nextPath);
  }

  const googleError = first(query.error) === "google";

  return (
    <section className="relative overflow-hidden py-10 sm:py-16">
      <div aria-hidden="true" className="tc-hero-glow pointer-events-none absolute inset-0" />
      <div className="relative mx-auto w-full max-w-md px-4">
        <div className="rounded-3xl border border-border bg-card p-5 shadow-[0_30px_80px_-40px_rgba(7,26,77,0.55)] sm:p-8">
          <LoginForm nextPath={nextPath} initialError={googleError ? "google" : null} />
        </div>
      </div>
    </section>
  );
}
