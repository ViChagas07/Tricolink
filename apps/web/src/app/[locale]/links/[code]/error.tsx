"use client";

import { TriangleAlert } from "lucide-react";
import { useTranslations } from "next-intl";

import { Button } from "@/components/ui/button";
import { Link } from "@/i18n/navigation";

export default function LinkDetailError({ reset }: { error: Error; reset: () => void }) {
  const t = useTranslations("links");

  return (
    <div className="mx-auto w-full max-w-3xl px-4 py-16 sm:px-6">
      <div
        role="alert"
        className="rounded-2xl border border-destructive/30 bg-destructive/5 p-6 text-center"
      >
        <TriangleAlert aria-hidden="true" className="mx-auto size-8 text-destructive" />
        <h1 className="mt-3 font-heading text-lg font-semibold">{t("loadError")}</h1>
        <div className="mt-4 flex flex-wrap items-center justify-center gap-2">
          <Button type="button" onClick={reset}>
            {t("retry")}
          </Button>
          <Link
            href="/links"
            prefetch={false}
            className="inline-flex h-8 items-center rounded-lg border border-border bg-background px-3 text-sm font-medium hover:bg-muted"
          >
            {t("backToList")}
          </Link>
        </div>
      </div>
    </div>
  );
}
