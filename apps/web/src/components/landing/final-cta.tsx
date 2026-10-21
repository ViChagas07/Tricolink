import { ArrowRight } from "lucide-react";
import { getTranslations } from "next-intl/server";

import { buttonVariants } from "@/components/ui/button";
import { Link } from "@/i18n/navigation";
import { cn } from "@/lib/utils";

export async function FinalCta() {
  const t = await getTranslations("finalCta");

  return (
    <section className="tc-defer-render mx-auto w-full max-w-6xl px-4 pb-16 sm:px-6 sm:pb-24">
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-tc-blue-950 via-tc-blue-800 to-tc-blue-700 px-6 py-12 text-center text-tc-white shadow-[0_40px_100px_-50px_rgba(7,26,77,0.9)] sm:px-12 sm:py-16">
        <div aria-hidden="true" className="tc-tricolor-bar absolute inset-x-0 top-0 h-1" />
        <div aria-hidden="true" className="tc-cta-glow pointer-events-none absolute inset-0" />

        <h2 className="relative text-balance font-heading text-3xl font-bold tracking-tight sm:text-4xl">
          {t("title")}
        </h2>
        <p className="relative mx-auto mt-4 max-w-xl text-pretty text-sm leading-relaxed text-white/80 sm:text-base">
          {t("body")}
        </p>

        <div className="relative mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <Link
            href="/login"
            className={cn(
              buttonVariants({ variant: "brand" }),
              "h-12 w-full px-6 text-base sm:w-auto",
            )}
          >
            {t("button")}
            <ArrowRight aria-hidden="true" className="size-4 rtl:rotate-180" />
          </Link>
          <a
            href="#shorten"
            className="inline-flex h-12 w-full items-center justify-center rounded-lg border border-white/30 px-6 text-base font-semibold text-white transition-colors hover:bg-white/10 sm:w-auto"
          >
            {t("secondary")}
          </a>
        </div>
      </div>
    </section>
  );
}
