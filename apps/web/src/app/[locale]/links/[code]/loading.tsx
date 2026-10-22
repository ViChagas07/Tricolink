import { getTranslations } from "next-intl/server";

export default async function LinkDetailLoading() {
  const t = await getTranslations("links");

  return (
    <div className="mx-auto w-full max-w-3xl px-4 py-10 sm:px-6 sm:py-14" aria-busy="true">
      <p className="sr-only" role="status">
        {t("statsLoading")}
      </p>
      <div className="h-5 w-28 animate-pulse rounded bg-muted" aria-hidden="true" />
      <div className="mt-5 h-9 w-64 max-w-full animate-pulse rounded-lg bg-muted" aria-hidden />
      <div className="mt-3 h-4 w-80 max-w-full animate-pulse rounded bg-muted" aria-hidden="true" />
      <div className="mt-8 grid gap-4 sm:grid-cols-3" aria-hidden="true">
        <div className="h-24 animate-pulse rounded-2xl bg-muted" />
        <div className="h-24 animate-pulse rounded-2xl bg-muted" />
        <div className="h-24 animate-pulse rounded-2xl bg-muted" />
      </div>
      <div className="mt-6 h-48 animate-pulse rounded-2xl bg-muted" aria-hidden="true" />
      <div className="mt-6 space-y-4" aria-hidden="true">
        <div className="h-16 animate-pulse rounded-2xl bg-muted" />
        <div className="h-64 animate-pulse rounded-2xl bg-muted" />
      </div>
    </div>
  );
}
