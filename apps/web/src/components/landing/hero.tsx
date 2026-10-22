import Image from "next/image";
import { getTranslations } from "next-intl/server";

import { ShortenForm } from "@/components/landing/shorten-form";

export async function HeroSection() {
  const t = await getTranslations("hero");

  return (
    <section className="relative overflow-hidden border-b border-border/70">
      <div aria-hidden="true" className="tc-hero-glow pointer-events-none absolute inset-0" />

      <div className="relative mx-auto w-full max-w-6xl px-4 pt-14 pb-16 sm:px-6 sm:pt-20 sm:pb-20 lg:pt-24">
        <div className="mx-auto max-w-4xl text-center">
          <Image
            src="/brand/tricolink-hero.png"
            alt="Tricolink"
            width={640}
            height={640}
            priority
            sizes="(min-width: 640px) 208px, 160px"
            className="mx-auto size-40 rounded-[1.75rem] shadow-[0_30px_70px_-30px_rgba(7,26,77,0.65)] ring-1 ring-tc-blue-950/10 sm:size-52"
          />

          <h1 className="mt-6 text-balance font-heading text-4xl font-bold tracking-tight text-tc-blue-950 sm:mt-8 sm:text-6xl lg:text-7xl dark:text-tc-white">
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
