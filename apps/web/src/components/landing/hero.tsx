import { getTranslations } from "next-intl/server";

import { ShortenForm } from "@/components/landing/shorten-form";

export async function HeroSection() {
  const t = await getTranslations("hero");

  return (
    <section className="relative overflow-hidden border-b border-border/70">
      <div aria-hidden="true" className="tc-hero-glow pointer-events-none absolute inset-0" />

      <div className="relative mx-auto w-full max-w-6xl px-4 pt-14 pb-16 sm:px-6 sm:pt-20 sm:pb-20 lg:pt-24">
        <div className="mx-auto max-w-4xl text-center">
          <p className="inline-flex items-center gap-2 rounded-full border border-tc-blue-600/20 bg-tc-blue-100/60 px-3 py-1 text-[0.7rem] font-semibold uppercase tracking-[0.18em] text-tc-blue-800 dark:border-tc-blue-600/30 dark:bg-tc-blue-600/15 dark:text-tc-blue-100">
            <span aria-hidden="true" className="size-1.5 rounded-full bg-tc-red-600" />
            {t("eyebrow")}
          </p>

          <h1 className="mt-5 text-balance font-heading text-4xl font-bold tracking-tight text-tc-blue-950 sm:text-6xl lg:text-7xl dark:text-tc-white">
            {t("title")}
          </h1>
          <p className="mx-auto mt-5 max-w-2xl text-pretty text-base leading-relaxed text-muted-foreground sm:text-lg">
            {t("subtitle")}
          </p>

          <div className="mt-8 sm:mt-10">
            <ShortenForm />
          </div>
        </div>
      </div>
    </section>
  );
}
