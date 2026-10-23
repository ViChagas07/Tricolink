import { BarChart3, CalendarClock, Check, Copy, Link2, SlidersHorizontal } from "lucide-react";
import { getLocale, getTranslations } from "next-intl/server";

import { cn } from "@/lib/utils";

const WEEKDAY_BARS = [38, 56, 44, 72, 61, 84, 68];

function ShortLinkVisual({ title, copyLabel }: { title: string; copyLabel: string }) {
  return (
    <div className="relative overflow-hidden rounded-2xl border border-border bg-card p-4 shadow-lg sm:p-6">
      <div aria-hidden="true" className="flex gap-1.5">
        <span className="size-2 rounded-full bg-tc-red-600" />
        <span className="size-2 rounded-full bg-tc-blue-600" />
        <span className="size-2 rounded-full bg-tc-blue-100" />
      </div>

      <p className="mt-4 text-[0.65rem] font-semibold uppercase tracking-[0.18em] text-muted-foreground">
        {title}
      </p>

      <div className="mt-3 rounded-xl border border-border bg-background/70 p-3">
        <p dir="ltr" className="truncate text-xs text-muted-foreground line-through">
          https://www.esporte.example/noticia/tricolink-chega-ao-brasil
        </p>
      </div>

      <div className="mt-3 flex items-center justify-between gap-3 rounded-xl bg-tc-blue-700 p-3 text-tc-white shadow-md">
        <span className="flex min-w-0 items-center gap-2">
          <Link2 aria-hidden="true" className="size-4 shrink-0" />
          <span dir="ltr" className="truncate font-mono text-xs font-semibold sm:text-sm">
            tricolink.app/bahia24
          </span>
        </span>
        <span className="inline-flex shrink-0 items-center gap-1 rounded-lg bg-white/15 px-2 py-1 text-xs font-semibold">
          <Copy aria-hidden="true" className="size-3.5" />
          {copyLabel}
        </span>
      </div>
    </div>
  );
}

function StatsVisual({
  title,
  totalLabel,
  total,
}: {
  title: string;
  totalLabel: string;
  total: string;
}) {
  return (
    <div className="rounded-2xl border border-border bg-card p-4 shadow-lg sm:p-6">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-[0.65rem] font-semibold uppercase tracking-[0.18em] text-muted-foreground">
            {title}
          </p>
          <p className="mt-1 font-heading text-3xl font-bold tabular-nums text-tc-blue-950 dark:text-tc-white">
            {total}
          </p>
          <p className="text-xs text-muted-foreground">{totalLabel}</p>
        </div>
        <span className="grid size-10 place-items-center rounded-xl bg-tc-blue-100 text-tc-blue-700 dark:bg-tc-blue-600/20 dark:text-tc-blue-100">
          <BarChart3 aria-hidden="true" className="size-5" />
        </span>
      </div>

      <div aria-hidden="true" className="mt-5 flex h-32 items-end gap-2">
        {WEEKDAY_BARS.map((height, index) => (
          <span
            key={index}
            className={cn(
              "flex-1 rounded-t-lg",
              index === WEEKDAY_BARS.length - 2 ? "bg-tc-red-600" : "bg-tc-blue-600/75",
            )}
            style={{ height: `${height}%` }}
          />
        ))}
      </div>
    </div>
  );
}

function ControlVisual({
  title,
  expiryLabel,
  expiry,
  activeLabel,
}: {
  title: string;
  expiryLabel: string;
  expiry: string;
  activeLabel: string;
}) {
  return (
    <div className="rounded-2xl border border-border bg-card p-4 shadow-lg sm:p-6">
      <div className="flex items-center justify-between gap-3">
        <p className="inline-flex items-center gap-2 font-heading text-sm font-semibold text-card-foreground">
          <SlidersHorizontal aria-hidden="true" className="size-4 text-tc-blue-600" />
          {title}
        </p>
        <span className="inline-flex items-center gap-1.5 rounded-full bg-tc-blue-100 px-2.5 py-1 text-xs font-semibold text-tc-blue-800 dark:bg-tc-blue-600/20 dark:text-tc-blue-100">
          <Check aria-hidden="true" className="size-3.5" />
          {activeLabel}
        </span>
      </div>

      <div className="mt-4 flex items-center justify-between gap-3 rounded-xl border border-border bg-background/70 p-3">
        <span className="inline-flex items-center gap-2 text-sm text-muted-foreground">
          <CalendarClock aria-hidden="true" className="size-4" />
          {expiryLabel}
        </span>
        <span className="text-sm font-semibold text-card-foreground">{expiry}</span>
      </div>

      <div aria-hidden="true" className="mt-3 space-y-2">
        <span className="block h-2 w-full rounded-full bg-muted" />
        <span className="block h-2 w-4/5 rounded-full bg-muted" />
        <span className="block h-2 w-2/3 rounded-full bg-muted" />
      </div>
    </div>
  );
}

export async function FeatureBlocks() {
  const t = await getTranslations("features");
  const demo = await getTranslations("demo");
  const hero = await getTranslations("hero");
  const locale = await getLocale();
  const expiry = new Intl.DateTimeFormat(locale, {
    day: "numeric",
    month: "short",
    year: "numeric",
    timeZone: "UTC",
  }).format(new Date("2026-11-18T12:00:00Z"));
  const total = new Intl.NumberFormat(locale).format(1063);

  const features = [
    {
      icon: Link2,
      title: t("shortTitle"),
      body: t("shortBody"),
      visual: <ShortLinkVisual title={t("shortMockTitle")} copyLabel={hero("copy")} />,
    },
    {
      icon: BarChart3,
      title: t("statsTitle"),
      body: t("statsBody"),
      visual: (
        <StatsVisual title={t("statsMockTitle")} totalLabel={demo("totalClicks")} total={total} />
      ),
    },
    {
      icon: SlidersHorizontal,
      title: t("controlTitle"),
      body: t("controlBody"),
      visual: (
        <ControlVisual
          title={t("controlMockTitle")}
          expiryLabel={t("controlMockExpiry")}
          expiry={expiry}
          activeLabel={t("controlMockState")}
        />
      ),
    },
  ];

  return (
    <section
      id="features"
      className="tc-defer-render tc-defer-render-tall mx-auto w-full max-w-6xl scroll-mt-24 px-4 py-16 sm:px-6 sm:py-24"
    >
      <div className="max-w-2xl">
        <h2 className="text-balance font-heading text-3xl font-bold tracking-tight text-tc-blue-950 sm:text-4xl dark:text-tc-white">
          {t("title")}
        </h2>
        <p className="mt-3 text-pretty text-sm leading-relaxed text-muted-foreground sm:text-base">
          {t("subtitle")}
        </p>
      </div>

      <div className="mt-12 space-y-14 sm:mt-16 sm:space-y-20">
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <div
              key={feature.title}
              className="grid grid-cols-1 items-center gap-8 lg:grid-cols-2 lg:gap-16"
            >
              <div className={cn("min-w-0", index % 2 === 1 && "lg:order-2")}>
                <p className="text-xs font-semibold uppercase tracking-[0.22em] text-tc-red-600 dark:text-tc-red-400">
                  {String(index + 1).padStart(2, "0")}
                </p>
                <span className="mt-4 grid size-11 place-items-center rounded-xl bg-tc-blue-100 text-tc-blue-700 dark:bg-tc-blue-600/20 dark:text-tc-blue-100">
                  <Icon aria-hidden="true" className="size-5" />
                </span>
                <h3 className="mt-4 text-balance font-heading text-2xl font-bold tracking-tight text-tc-blue-950 sm:text-3xl dark:text-tc-white">
                  {feature.title}
                </h3>
                <p className="mt-3 max-w-md text-pretty text-sm leading-relaxed text-muted-foreground sm:text-base">
                  {feature.body}
                </p>
              </div>

              <div className={cn("min-w-0", index % 2 === 1 && "lg:order-1")}>
                <div className="relative">
                  <div
                    aria-hidden="true"
                    className="absolute -inset-3 -z-10 rounded-3xl bg-gradient-to-br from-tc-blue-600/10 to-tc-red-600/10"
                  />
                  {feature.visual}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
