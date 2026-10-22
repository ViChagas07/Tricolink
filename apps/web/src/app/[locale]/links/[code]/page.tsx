import type { Metadata } from "next";
import { ArrowLeft, ExternalLink, MousePointerClick } from "lucide-react";
import { notFound } from "next/navigation";
import { getTranslations } from "next-intl/server";

import { CopyLinkButton } from "@/components/links/copy-link-button";
import { Link } from "@/i18n/navigation";
import { defaultLocale, isLocale } from "@/i18n/locales";
import { linkStatus } from "@/lib/links";
import { requireUser, getServerLink } from "@/lib/server-api";
import { safeExternalHref } from "@/lib/url";
import { cn } from "@/lib/utils";

type LinkDetailPageProps = {
  params: Promise<{ locale: string; code: string }>;
};

export async function generateMetadata({ params }: LinkDetailPageProps): Promise<Metadata> {
  const { locale: rawLocale } = await params;
  const locale = isLocale(rawLocale) ? rawLocale : defaultLocale;
  const t = await getTranslations({ locale, namespace: "links" });
  return {
    title: t("detailTitle"),
    robots: { index: false, follow: false },
  };
}

export default async function LinkDetailPage({ params }: LinkDetailPageProps) {
  const { locale: rawLocale, code } = await params;
  if (!isLocale(rawLocale)) {
    notFound();
  }

  await requireUser(rawLocale, `/${rawLocale}/links/${encodeURIComponent(code)}`);
  const link = await getServerLink(code);
  if (!link) {
    notFound();
  }

  const t = await getTranslations({ locale: rawLocale, namespace: "links" });
  const demo = await getTranslations({ locale: rawLocale, namespace: "demo" });
  const number = new Intl.NumberFormat(rawLocale);
  const date = new Intl.DateTimeFormat(rawLocale, { dateStyle: "medium", timeZone: "UTC" });
  const status = linkStatus(link);
  const statusLabel =
    status === "active"
      ? t("statusActive")
      : status === "inactive"
        ? t("statusInactive")
        : t("statusExpired");
  const shortHref = safeExternalHref(link.short_url);
  const originalHref = safeExternalHref(link.original_url);

  return (
    <div className="mx-auto w-full max-w-3xl px-4 py-10 sm:px-6 sm:py-14">
      <Link
        href="/links"
        prefetch={false}
        className="inline-flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft aria-hidden="true" className="size-4 rtl:rotate-180" />
        {t("backToList")}
      </Link>

      <header className="mt-5 flex flex-wrap items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="font-mono text-sm font-semibold text-tc-blue-700 dark:text-tc-blue-100">
            {link.code}
          </p>
          <h1 className="mt-1 break-words font-heading text-3xl font-bold tracking-tight text-tc-blue-950 sm:text-4xl dark:text-tc-white">
            {link.title ?? t("detailTitle")}
          </h1>
          <p className="mt-2 max-w-xl text-muted-foreground">{t("detailSubtitle")}</p>
        </div>
        <span
          className={cn(
            "inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-semibold",
            status === "active"
              ? "border-tc-blue-600/25 bg-tc-blue-100/60 text-tc-blue-800 dark:bg-tc-blue-600/15 dark:text-tc-blue-100"
              : status === "expired"
                ? "border-destructive/30 bg-destructive/5 text-destructive"
                : "border-border bg-muted text-muted-foreground",
          )}
        >
          {statusLabel}
        </span>
      </header>

      <div className="mt-8 grid gap-4 sm:grid-cols-3">
        <div className="rounded-2xl border border-border bg-card p-4 shadow-sm sm:p-5">
          <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            {demo("clicks")}
          </p>
          <p className="mt-1 inline-flex items-center gap-2 font-heading text-2xl font-bold">
            <MousePointerClick aria-hidden="true" className="size-5 text-tc-blue-600" />
            {number.format(link.click_count)}
          </p>
        </div>
        <div className="rounded-2xl border border-border bg-card p-4 shadow-sm sm:p-5">
          <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            {demo("created")}
          </p>
          <p className="mt-1 text-sm font-medium">{date.format(new Date(link.created_at))}</p>
        </div>
        <div className="rounded-2xl border border-border bg-card p-4 shadow-sm sm:p-5">
          <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            {t("expires")}
          </p>
          <p className="mt-1 text-sm font-medium">
            {link.expires_at ? date.format(new Date(link.expires_at)) : t("never")}
          </p>
        </div>
      </div>

      <section
        aria-labelledby="link-destination-heading"
        className="mt-6 rounded-2xl border border-border bg-card p-5 shadow-sm sm:p-6"
      >
        <h2 id="link-destination-heading" className="font-heading text-lg font-semibold">
          {demo("destination")}
        </h2>

        <div className="mt-4 space-y-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              {demo("shortLink")}
            </p>
            <div className="mt-1 flex items-center gap-2">
              {shortHref ? (
                <a
                  href={shortHref}
                  target="_blank"
                  rel="noopener noreferrer nofollow ugc"
                  dir="ltr"
                  className="break-all font-mono text-sm font-semibold text-tc-blue-700 underline-offset-4 hover:underline dark:text-tc-blue-100"
                >
                  {link.short_url}
                </a>
              ) : (
                <span dir="ltr" className="break-all font-mono text-sm font-semibold">
                  {link.short_url}
                </span>
              )}
              <CopyLinkButton value={link.short_url} code={link.code} />
            </div>
          </div>

          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              {t("originalUrlLabel")}
            </p>
            <div className="mt-1 flex items-start gap-2">
              <p dir="ltr" className="break-all text-sm text-foreground">
                {link.original_url}
              </p>
              {originalHref ? (
                <a
                  href={originalHref}
                  target="_blank"
                  rel="noopener noreferrer nofollow ugc"
                  aria-label={t("openOriginal")}
                  title={t("openOriginal")}
                  className="inline-flex size-9 shrink-0 items-center justify-center rounded-lg text-muted-foreground hover:bg-muted hover:text-foreground"
                >
                  <ExternalLink aria-hidden="true" className="size-4" />
                </a>
              ) : null}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
