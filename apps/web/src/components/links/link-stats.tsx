"use client";

import { CalendarClock, MousePointerClick, TriangleAlert } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useRef, useState } from "react";

import { BreakdownTable, type BreakdownRow } from "@/components/dashboard/breakdown-table";
import { ClicksChart } from "@/components/dashboard/clicks-chart";
import { Button } from "@/components/ui/button";
import {
  STATS_RANGES,
  countryName,
  formatStatsDate,
  getLinkStats,
  type LinkStatsDto,
  type StatsBreakdownItem,
  type StatsRange,
} from "@/lib/stats";
import { cn } from "@/lib/utils";

const RANGE_LABEL_KEYS: Record<StatsRange, "range7d" | "range30d" | "range90d"> = {
  "7d": "range7d",
  "30d": "range30d",
  "90d": "range90d",
};

type LinkStatsPanelProps = {
  code: string;
  initialRange?: StatsRange;
  initialStats: LinkStatsDto | null;
};

function breakdownRows(
  items: StatsBreakdownItem[],
  prefix: string,
  labelFor: (item: StatsBreakdownItem) => string,
): BreakdownRow[] {
  return items.map((item) => ({
    id: `${prefix}-${item.code}`,
    label: labelFor(item),
    clicks: item.clicks,
    share: item.pct / 100,
  }));
}

export function LinkStatsPanel({ code, initialRange = "30d", initialStats }: LinkStatsPanelProps) {
  const t = useTranslations("links");
  const demo = useTranslations("demo");
  const locale = useLocale();
  const requestId = useRef(0);
  const [range, setRange] = useState<StatsRange>(initialRange);
  const [stats, setStats] = useState<LinkStatsDto | null>(initialStats);
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(initialStats === null);

  async function load(nextRange: StatsRange) {
    const currentRequest = requestId.current + 1;
    requestId.current = currentRequest;
    setRange(nextRange);
    setLoading(true);
    setFailed(false);

    try {
      const nextStats = await getLinkStats(code, nextRange);
      if (requestId.current === currentRequest) {
        setStats(nextStats);
      }
    } catch {
      if (requestId.current === currentRequest) {
        setFailed(true);
      }
    } finally {
      if (requestId.current === currentRequest) {
        setLoading(false);
      }
    }
  }

  const countryLabel = (item: StatsBreakdownItem): string =>
    item.code === "other" ? demo("other") : countryName(locale, item.code);
  const referrerLabel = (item: StatsBreakdownItem): string =>
    item.code === "direct"
      ? demo("sourceDirect")
      : item.code === "other"
        ? demo("other")
        : item.code;
  const deviceLabel = (item: StatsBreakdownItem): string => {
    switch (item.code) {
      case "desktop":
        return demo("deviceDesktop");
      case "mobile":
        return demo("deviceMobile");
      case "tablet":
        return demo("deviceTablet");
      case "bot":
        return t("deviceBot");
      default:
        return t("deviceUnknown");
    }
  };

  const series =
    stats?.series.map((point) => ({
      label: formatStatsDate(point.date, locale),
      clicks: point.clicks,
    })) ?? [];
  const countries = stats ? breakdownRows(stats.countries, "country", countryLabel) : [];
  const referrers = stats ? breakdownRows(stats.referrers, "referrer", referrerLabel) : [];
  const devices = stats ? breakdownRows(stats.devices, "device", deviceLabel) : [];
  const isEmpty = stats !== null && stats.total === 0;

  return (
    <section
      aria-labelledby="link-stats-heading"
      aria-busy={loading}
      className="mt-6 rounded-2xl border border-border bg-card p-5 shadow-sm sm:p-6"
    >
      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div className="min-w-0">
          <h2 id="link-stats-heading" className="font-heading text-lg font-semibold">
            {t("statsTitle")}
          </h2>
          <p className="mt-1 text-sm text-muted-foreground">{t("statsSubtitle")}</p>
        </div>

        <div
          role="group"
          aria-label={t("periodLabel")}
          className="inline-flex w-fit shrink-0 rounded-xl border border-border bg-muted/40 p-1"
        >
          {STATS_RANGES.map((option) => (
            <button
              key={option}
              type="button"
              aria-pressed={range === option}
              disabled={loading}
              onClick={() => void load(option)}
              className={cn(
                "rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/50 disabled:cursor-not-allowed",
                range === option
                  ? "bg-card text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground",
              )}
            >
              {t(RANGE_LABEL_KEYS[option])}
            </button>
          ))}
        </div>
      </div>

      <div className="sr-only" role="status" aria-live="polite">
        {loading ? t("statsLoading") : null}
      </div>

      {failed ? (
        <div
          role="alert"
          className="mt-5 flex flex-col gap-3 rounded-xl border border-destructive/30 bg-destructive/5 p-4 text-sm text-destructive sm:flex-row sm:items-center sm:justify-between"
        >
          <span className="inline-flex items-center gap-2">
            <TriangleAlert aria-hidden="true" className="size-4 shrink-0" />
            {t("statsError")}
          </span>
          <Button
            type="button"
            size="sm"
            variant="outline"
            onClick={() => void load(range)}
            className="w-fit"
          >
            {t("retry")}
          </Button>
        </div>
      ) : null}

      {loading ? (
        <div aria-hidden="true" className="mt-5 space-y-4">
          <div className="h-16 animate-pulse rounded-xl bg-muted" />
          <div className="h-64 animate-pulse rounded-xl bg-muted" />
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            <div className="h-48 animate-pulse rounded-xl bg-muted" />
            <div className="h-48 animate-pulse rounded-xl bg-muted" />
            <div className="h-48 animate-pulse rounded-xl bg-muted" />
          </div>
        </div>
      ) : stats === null ? null : isEmpty ? (
        <div
          role="status"
          className="mt-5 flex flex-col items-center justify-center rounded-xl border border-dashed border-border bg-background/60 px-4 py-10 text-center"
        >
          <CalendarClock aria-hidden="true" className="size-8 text-muted-foreground" />
          <p className="mt-3 font-heading text-base font-semibold">{t("emptyStatsTitle")}</p>
          <p className="mt-1 max-w-sm text-sm text-muted-foreground">{t("emptyStatsBody")}</p>
        </div>
      ) : (
        <div className="mt-5 space-y-4">
          <div className="flex flex-wrap items-end justify-between gap-3 rounded-xl border border-border bg-background/60 p-4">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                {t("totalInPeriod")}
              </p>
              <p
                data-testid="stats-total"
                className="mt-1 inline-flex items-center gap-2 font-heading text-3xl font-bold tabular-nums text-tc-blue-950 dark:text-tc-white"
              >
                <MousePointerClick
                  aria-hidden="true"
                  className="size-6 text-tc-red-600 dark:text-tc-red-400"
                />
                {new Intl.NumberFormat(locale).format(stats.total)}
              </p>
            </div>
            <p className="text-xs font-medium text-muted-foreground">
              {t(RANGE_LABEL_KEYS[range])}
            </p>
          </div>

          <div className="rounded-xl border border-border bg-background/60 p-4">
            <div className="flex flex-wrap items-start justify-between gap-2">
              <div>
                <h3 className="font-heading text-sm font-semibold">{t("chartTitle")}</h3>
                <p className="mt-0.5 text-xs text-muted-foreground">{t("chartCaption")}</p>
              </div>
            </div>
            <div className="mt-4">
              <ClicksChart
                data={series}
                ariaLabel={`${t("chartTitle")}. ${t("chartCaption")}`}
                clicksLabel={demo("clicks")}
                dateLabel={demo("dateColumn")}
              />
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
            <BreakdownTable
              locale={locale}
              title={demo("countries")}
              columns={{
                label: demo("countryColumn"),
                clicks: demo("clicksColumn"),
                share: demo("shareColumn"),
              }}
              items={countries}
              emptyLabel={t("noData")}
            />
            <BreakdownTable
              locale={locale}
              title={demo("referrers")}
              columns={{
                label: demo("sourceColumn"),
                clicks: demo("clicksColumn"),
                share: demo("shareColumn"),
              }}
              items={referrers}
              emptyLabel={t("noData")}
            />
            <BreakdownTable
              locale={locale}
              title={demo("devices")}
              columns={{
                label: demo("deviceColumn"),
                clicks: demo("clicksColumn"),
                share: demo("shareColumn"),
              }}
              items={devices}
              emptyLabel={t("noData")}
            />
          </div>
        </div>
      )}
    </section>
  );
}
