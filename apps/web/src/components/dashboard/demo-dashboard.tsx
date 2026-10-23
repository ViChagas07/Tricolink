import { CalendarDays, Info, Link2, MousePointerClick } from "lucide-react";
import { getLocale, getTranslations } from "next-intl/server";

import { BreakdownTable, type BreakdownRow } from "@/components/dashboard/breakdown-table";
import { DeferredClicksChart } from "@/components/dashboard/deferred-clicks-chart";

const DAILY_CLICKS = [
  18, 22, 25, 31, 28, 24, 20, 26, 34, 38, 42, 35, 30, 27, 32, 39, 45, 48, 41, 36, 33, 37, 44, 52,
  47, 40, 35, 42, 49, 43,
];
const SERIES_START = Date.UTC(2026, 8, 21);
const DAY_MS = 86_400_000;
const TOTAL_CLICKS = DAILY_CLICKS.reduce((total, clicks) => total + clicks, 0);

const COUNTRIES = [
  { code: "BR", clicks: 486 },
  { code: "US", clicks: 302 },
  { code: "DE", clicks: 128 },
  { code: "JP", clicks: 84 },
];
const SOURCES = [
  { id: "instagram.com", label: "instagram.com", clicks: 298 },
  { id: "google.com", label: "google.com", clicks: 241 },
  { id: "news.example.com", label: "news.example.com", clicks: 167 },
];
const DEVICES = [
  { id: "mobile", clicks: 594 },
  { id: "desktop", clicks: 352 },
  { id: "tablet", clicks: 117 },
];

function regionName(locale: string, code: string): string {
  try {
    return new Intl.DisplayNames([locale], { type: "region" }).of(code) ?? code;
  } catch {
    return code;
  }
}

function rowsWithShare(rows: Array<{ id: string; label: string; clicks: number }>): BreakdownRow[] {
  return rows.map((row) => ({ ...row, share: row.clicks / TOTAL_CLICKS }));
}

export async function DemoDashboard() {
  const t = await getTranslations("demo");
  const locale = await getLocale();

  const dateFormat = new Intl.DateTimeFormat(locale, {
    month: "short",
    day: "numeric",
    timeZone: "UTC",
  });
  const createdFormat = new Intl.DateTimeFormat(locale, {
    dateStyle: "medium",
    timeZone: "UTC",
  });
  const numberFormat = new Intl.NumberFormat(locale);

  const series = DAILY_CLICKS.map((clicks, index) => ({
    label: dateFormat.format(new Date(SERIES_START + index * DAY_MS)),
    clicks,
  }));

  const countryRows = rowsWithShare([
    ...COUNTRIES.map((country) => ({
      id: country.code,
      label: regionName(locale, country.code),
      clicks: country.clicks,
    })),
    {
      id: "other",
      label: t("other"),
      clicks: TOTAL_CLICKS - COUNTRIES.reduce((total, country) => total + country.clicks, 0),
    },
  ]);

  const sourceRows = rowsWithShare([
    ...SOURCES,
    { id: "direct", label: t("sourceDirect"), clicks: 214 },
    {
      id: "other",
      label: t("other"),
      clicks: TOTAL_CLICKS - SOURCES.reduce((total, source) => total + source.clicks, 0) - 214,
    },
  ]).sort((left, right) => right.clicks - left.clicks);

  const deviceRows = rowsWithShare([
    { id: "mobile", label: t("deviceMobile"), clicks: DEVICES[0].clicks },
    { id: "desktop", label: t("deviceDesktop"), clicks: DEVICES[1].clicks },
    { id: "tablet", label: t("deviceTablet"), clicks: DEVICES[2].clicks },
  ]);

  return (
    <section
      id="demo"
      className="tc-defer-render scroll-mt-24 border-y border-border/70 bg-gradient-to-b from-background via-background to-tc-blue-100/40 py-16 sm:py-24 dark:to-tc-blue-950/40"
    >
      <div className="mx-auto w-full max-w-6xl px-4 sm:px-6">
        <div className="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-end">
          <div className="max-w-2xl">
            <h2
              id="demo-title"
              className="text-balance font-heading text-3xl font-bold tracking-tight text-tc-blue-950 sm:text-4xl dark:text-tc-white"
            >
              {t("title")}
            </h2>
            <p className="mt-3 text-pretty text-sm leading-relaxed text-muted-foreground sm:text-base">
              {t("description")}
            </p>
          </div>
          <span className="inline-flex shrink-0 items-center gap-1.5 rounded-full border border-tc-blue-600/25 bg-card px-3 py-1 text-xs font-semibold text-tc-blue-700 shadow-sm dark:text-tc-blue-100">
            <Info aria-hidden="true" className="size-3.5" />
            {t("label")}
          </span>
        </div>

        <div className="mt-8 rounded-3xl border border-border bg-card p-3 shadow-[0_40px_120px_-60px_rgba(7,26,77,0.65)] sm:mt-10 sm:p-5">
          <div className="flex flex-col gap-4 rounded-2xl bg-gradient-to-r from-tc-blue-950 to-tc-blue-700 p-4 text-tc-white sm:flex-row sm:items-center sm:justify-between sm:p-5">
            <div className="flex min-w-0 items-center gap-3">
              <span className="grid size-10 shrink-0 place-items-center rounded-xl bg-white/15">
                <Link2 aria-hidden="true" className="size-5" />
              </span>
              <div className="min-w-0">
                <p className="text-[0.65rem] font-semibold uppercase tracking-[0.18em] text-white/65">
                  {t("shortLink")}
                </p>
                <p dir="ltr" className="truncate font-mono text-sm font-semibold sm:text-base">
                  tricolink.app/bahia24
                </p>
              </div>
            </div>
            <span className="inline-flex w-fit items-center gap-1.5 rounded-full bg-white/15 px-2.5 py-1 text-xs font-semibold">
              <span aria-hidden="true" className="size-1.5 rounded-full bg-tc-red-400" />
              {t("active")}
            </span>
          </div>

          <div className="mt-4 grid grid-cols-1 gap-4 px-1 sm:grid-cols-2">
            <div className="min-w-0">
              <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                {t("destination")}
              </p>
              <p dir="ltr" className="mt-1 truncate text-sm font-medium text-card-foreground">
                https://www.esporte.example/noticia/tricolink-chega-ao-brasil
              </p>
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                {t("created")}
              </p>
              <p className="mt-1 inline-flex items-center gap-1.5 text-sm font-medium text-card-foreground">
                <CalendarDays aria-hidden="true" className="size-4 text-muted-foreground" />
                {createdFormat.format(new Date("2026-09-18T14:30:00Z"))}
              </p>
            </div>
          </div>

          <div className="mt-5 rounded-2xl border border-border bg-background/60 p-4 sm:p-5">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <h3 className="font-heading text-sm font-semibold text-card-foreground sm:text-base">
                  {t("chartTitle")}
                </h3>
                <p className="mt-0.5 text-xs text-muted-foreground">{t("chartCaption")}</p>
              </div>
              <div className="text-end">
                <p className="inline-flex items-center gap-1.5 font-heading text-2xl font-bold tabular-nums text-tc-blue-950 dark:text-tc-white">
                  <MousePointerClick
                    aria-hidden="true"
                    className="size-5 text-tc-red-600 dark:text-tc-red-400"
                  />
                  {numberFormat.format(TOTAL_CLICKS)}
                </p>
                <p className="text-xs text-muted-foreground">{t("totalClicks")}</p>
              </div>
            </div>

            <div id="demo-chart" className="mt-4">
              <DeferredClicksChart
                data={series}
                ariaLabel={`${t("chartTitle")}. ${t("chartCaption")}`}
                clicksLabel={t("clicks")}
                dateLabel={t("dateColumn")}
              />
            </div>
          </div>

          <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
            <BreakdownTable
              locale={locale}
              title={t("countries")}
              caption={`${t("countries")} — ${t("chartCaption")}`}
              columns={{
                label: t("countryColumn"),
                clicks: t("clicksColumn"),
                share: t("shareColumn"),
              }}
              items={countryRows}
              emptyLabel={t("chartCaption")}
            />
            <BreakdownTable
              locale={locale}
              title={t("referrers")}
              caption={`${t("referrers")} — ${t("chartCaption")}`}
              columns={{
                label: t("sourceColumn"),
                clicks: t("clicksColumn"),
                share: t("shareColumn"),
              }}
              items={sourceRows}
              emptyLabel={t("chartCaption")}
            />
            <BreakdownTable
              locale={locale}
              title={t("devices")}
              caption={`${t("devices")} — ${t("chartCaption")}`}
              columns={{
                label: t("deviceColumn"),
                clicks: t("clicksColumn"),
                share: t("shareColumn"),
              }}
              items={deviceRows}
              emptyLabel={t("chartCaption")}
            />
          </div>
        </div>
      </div>
    </section>
  );
}
