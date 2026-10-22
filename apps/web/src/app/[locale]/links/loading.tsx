import { getTranslations } from "next-intl/server";

import { LinksSkeleton } from "@/components/links/links-skeleton";

export default async function LinksLoading() {
  const t = await getTranslations("links");

  return (
    <div className="mx-auto w-full max-w-5xl px-4 py-10 sm:px-6 sm:py-14" aria-busy="true">
      <p className="sr-only" role="status">
        {t("loading")}
      </p>
      <div className="h-9 w-48 animate-pulse rounded-lg bg-muted" aria-hidden="true" />
      <div className="mt-3 h-4 w-80 max-w-full animate-pulse rounded bg-muted" aria-hidden="true" />
      <div className="mt-8 h-40 animate-pulse rounded-2xl bg-muted" aria-hidden="true" />
      <LinksSkeleton className="mt-6" rows={3} />
    </div>
  );
}
