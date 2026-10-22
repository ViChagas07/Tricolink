import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { NextIntlClientProvider, type AbstractIntlMessages } from "next-intl";
import { beforeEach, describe, expect, it, vi } from "vitest";

import enMessages from "../../../messages/en.json";
import { formatStatsDate, getLinkStats, type LinkStatsDto } from "@/lib/stats";
import { LinkStatsPanel } from "./link-stats";

vi.mock("@/components/dashboard/clicks-chart", () => ({
  ClicksChart: ({ data }: { data: ReadonlyArray<{ label: string; clicks: number }> }) => (
    <div data-testid="clicks-chart">{data.map((point) => point.label).join(", ")}</div>
  ),
}));

vi.mock("@/lib/stats", async () => {
  const actual = await vi.importActual<typeof import("@/lib/stats")>("@/lib/stats");
  return {
    ...actual,
    getLinkStats: vi.fn(),
  };
});

const fullStats: LinkStatsDto = {
  total: 5,
  series: [
    { date: "2026-10-18", clicks: 2 },
    { date: "2026-10-19", clicks: 0 },
    { date: "2026-10-20", clicks: 3 },
  ],
  countries: [
    { code: "BR", clicks: 3, pct: 60 },
    { code: "other", clicks: 2, pct: 40 },
  ],
  devices: [
    { code: "mobile", clicks: 4, pct: 80 },
    { code: "desktop", clicks: 1, pct: 20 },
  ],
  referrers: [
    { code: "direct", clicks: 2, pct: 40 },
    { code: "google.com", clicks: 3, pct: 60 },
  ],
};

const emptyStats: LinkStatsDto = {
  total: 0,
  series: [
    { date: "2026-10-18", clicks: 0 },
    { date: "2026-10-19", clicks: 0 },
  ],
  countries: [],
  devices: [],
  referrers: [],
};

function renderPanel(stats: LinkStatsDto | null) {
  return render(
    <NextIntlClientProvider
      locale="en"
      messages={enMessages as AbstractIntlMessages}
      timeZone="UTC"
    >
      <LinkStatsPanel code="abc1234" initialStats={stats} />
    </NextIntlClientProvider>,
  );
}

describe("LinkStatsPanel", () => {
  beforeEach(() => {
    vi.mocked(getLinkStats).mockReset();
  });

  it("renders the total, chart series and breakdowns with localized names", () => {
    renderPanel(fullStats);

    expect(screen.getByText("Clicks in this period")).toBeInTheDocument();
    expect(screen.getByTestId("clicks-chart")).toHaveTextContent(
      fullStats.series.map((point) => formatStatsDate(point.date, "en")).join(", "),
    );

    const countries = screen.getByRole("table", { name: "Countries" });
    expect(within(countries).getByRole("rowheader", { name: "Brazil" })).toBeInTheDocument();
    expect(within(countries).getByRole("rowheader", { name: "Other" })).toBeInTheDocument();

    const referrers = screen.getByRole("table", { name: "Sources" });
    expect(within(referrers).getByRole("rowheader", { name: "Direct" })).toBeInTheDocument();
    expect(within(referrers).getByRole("rowheader", { name: "google.com" })).toBeInTheDocument();

    const devices = screen.getByRole("table", { name: "Devices" });
    expect(within(devices).getByRole("rowheader", { name: "Mobile" })).toBeInTheDocument();
    expect(within(devices).getByRole("rowheader", { name: "Desktop" })).toBeInTheDocument();
  });

  it("renders the empty state when there are no clicks", () => {
    renderPanel(emptyStats);

    expect(screen.getByText("No clicks in this period")).toBeInTheDocument();
    expect(screen.queryByRole("table")).not.toBeInTheDocument();
    expect(screen.queryByTestId("clicks-chart")).not.toBeInTheDocument();
  });

  it("shows an error with retry and reloads the selected period", async () => {
    vi.mocked(getLinkStats).mockResolvedValueOnce(fullStats);
    const browser = userEvent.setup();
    renderPanel(null);

    expect(screen.getByRole("alert")).toHaveTextContent("We couldn't load the statistics.");
    expect(getLinkStats).not.toHaveBeenCalled();

    await browser.click(screen.getByRole("button", { name: "Try again" }));

    await waitFor(() => expect(getLinkStats).toHaveBeenCalledWith("abc1234", "30d"));
    expect(await screen.findByText("Clicks in this period")).toBeInTheDocument();
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("switches the period and requests new statistics", async () => {
    vi.mocked(getLinkStats).mockResolvedValueOnce({ ...fullStats, total: 2 });
    const browser = userEvent.setup();
    renderPanel(fullStats);

    await browser.click(screen.getByRole("button", { name: "7 days" }));

    await waitFor(() => expect(getLinkStats).toHaveBeenCalledWith("abc1234", "7d"));
    expect(screen.getByRole("button", { name: "7 days" })).toHaveAttribute("aria-pressed", "true");
  });
});
