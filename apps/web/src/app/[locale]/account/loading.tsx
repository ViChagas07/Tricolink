import { getTranslations } from "next-intl/server";

export default async function AccountLoading() {
  const t = await getTranslations("account");

  return (
    <div className="mx-auto w-full max-w-4xl px-4 py-10 sm:px-6 sm:py-14" aria-busy="true">
      <p className="sr-only" role="status">
        {t("loading")}
      </p>
      <div className="h-10 w-56 animate-pulse rounded-lg bg-muted" aria-hidden="true" />
      <div className="mt-3 h-4 w-80 max-w-full animate-pulse rounded bg-muted" aria-hidden="true" />
      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <div className="h-80 animate-pulse rounded-2xl bg-muted" aria-hidden="true" />
        <div className="h-80 animate-pulse rounded-2xl bg-muted" aria-hidden="true" />
      </div>
    </div>
  );
}
