import { api } from "@/lib/api";

export const STATS_RANGES = ["7d", "30d", "90d"] as const;

export type StatsRange = (typeof STATS_RANGES)[number];

export type StatsSeriesPoint = {
  date: string;
  clicks: number;
};

export type StatsBreakdownItem = {
  code: string;
  clicks: number;
  pct: number;
};

export type LinkStatsDto = {
  total: number;
  series: StatsSeriesPoint[];
  countries: StatsBreakdownItem[];
  devices: StatsBreakdownItem[];
  referrers: StatsBreakdownItem[];
};

export function isStatsRange(value: string): value is StatsRange {
  return (STATS_RANGES as readonly string[]).includes(value);
}

export function getLinkStats(code: string, range: StatsRange): Promise<LinkStatsDto> {
  const search = new URLSearchParams({ range });
  return api.get<LinkStatsDto>(`/links/${encodeURIComponent(code)}/stats?${search.toString()}`);
}

export function parseStatsDate(value: string): Date | null {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (!match) {
    return null;
  }
  const [, year, month, day] = match;
  const date = new Date(Date.UTC(Number(year), Number(month) - 1, Number(day), 12));
  return Number.isNaN(date.getTime()) ? null : date;
}

export function formatStatsDate(value: string, locale: string): string {
  const date = parseStatsDate(value);
  if (!date) {
    return value;
  }
  return new Intl.DateTimeFormat(locale, { month: "short", day: "numeric" }).format(date);
}

export function countryName(locale: string, code: string): string {
  if (!/^[A-Za-z]{2}$/.test(code)) {
    return code;
  }
  try {
    return new Intl.DisplayNames([locale], { type: "region" }).of(code.toUpperCase()) ?? code;
  } catch {
    return code;
  }
}

export function emptyStats(range: StatsRange): LinkStatsDto {
  const days = range === "7d" ? 7 : range === "30d" ? 30 : 90;
  const today = new Date();
  return {
    total: 0,
    series: Array.from({ length: days }, (_, index) => {
      const date = new Date(
        Date.UTC(
          today.getUTCFullYear(),
          today.getUTCMonth(),
          today.getUTCDate() - (days - 1 - index),
        ),
      );
      return { date: date.toISOString().slice(0, 10), clicks: 0 };
    }),
    countries: [],
    devices: [],
    referrers: [],
  };
}
