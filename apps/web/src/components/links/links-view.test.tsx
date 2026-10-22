import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { NextIntlClientProvider, type AbstractIntlMessages } from "next-intl";
import { beforeEach, describe, expect, it, vi } from "vitest";

import enMessages from "../../../messages/en.json";
import { ApiError } from "@/lib/api";
import { deleteLink, listLinks, updateLink, type LinkDto, type ListLinksDto } from "@/lib/links";
import { LinksView } from "./links-view";

vi.mock("@/i18n/navigation", () => ({
  Link: ({
    href,
    children,
    ...props
  }: Omit<React.AnchorHTMLAttributes<HTMLAnchorElement>, "href"> & { href: string }) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
}));

vi.mock("@/lib/links", async () => {
  const actual = await vi.importActual<typeof import("@/lib/links")>("@/lib/links");
  return {
    ...actual,
    listLinks: vi.fn(),
    updateLink: vi.fn(),
    deleteLink: vi.fn(),
  };
});

const firstLink: LinkDto = {
  code: "abc1234",
  short_url: "http://localhost:3001/abc1234",
  original_url: "https://example.com/a-very-long-destination-path",
  title: "Launch page",
  created_at: "2026-01-02T10:00:00Z",
  expires_at: null,
  is_active: true,
  click_count: 7,
};

const secondLink: LinkDto = {
  code: "def5678",
  short_url: "http://localhost:3001/def5678",
  original_url: "https://example.org/inactive",
  title: null,
  created_at: "2026-01-03T10:00:00Z",
  expires_at: "2020-01-01T00:00:00Z",
  is_active: true,
  click_count: 2,
};

const initialPage: ListLinksDto = {
  items: [firstLink, secondLink],
  next_cursor: null,
};

function renderView(page: ListLinksDto | null = initialPage) {
  return render(
    <NextIntlClientProvider
      locale="en"
      messages={enMessages as AbstractIntlMessages}
      timeZone="UTC"
    >
      <LinksView initialPage={page} initialSummary={{ clicks: 9, links: 2 }} />
    </NextIntlClientProvider>,
  );
}

describe("LinksView", () => {
  beforeEach(() => {
    vi.mocked(listLinks).mockReset();
    vi.mocked(updateLink).mockReset();
    vi.mocked(deleteLink).mockReset();
  });

  it("renders the code, short link, destination, clicks and status", () => {
    renderView();

    expect(screen.getByRole("link", { name: "Open details: abc1234" })).toHaveAttribute(
      "href",
      "/links/abc1234",
    );
    expect(screen.getByText("http://localhost:3001/abc1234")).toBeInTheDocument();
    expect(screen.getByText("https://example.com/a-very-long-destination-path")).toHaveAttribute(
      "title",
      "https://example.com/a-very-long-destination-path",
    );
    expect(screen.getByText("Launch page")).toBeInTheDocument();
    expect(screen.getByText("Expired")).toBeInTheDocument();
    expect(screen.getAllByText("9").length).toBeGreaterThan(0);
  });

  it("renders user-controlled titles and URLs as inert text", () => {
    const malicious: LinkDto = {
      ...firstLink,
      title: '<img src=x onerror="window.__xss=1">',
      original_url: "javascript:alert(1)",
    };
    const { container } = renderView({ items: [malicious], next_cursor: null });

    expect(
      screen.getByText('<img src=x onerror="window.__xss=1">'),
    ).toBeInTheDocument();
    expect(container.querySelector("img")).toBeNull();
    expect(container.querySelector('script')).toBeNull();
    expect(container.querySelector('a[href^="javascript:"]')).toBeNull();
    expect(container.querySelector("iframe")).toBeNull();
  });

  it("copies the short link", async () => {
    const browser = userEvent.setup();
    renderView();

    await browser.click(screen.getByRole("button", { name: "Copy: abc1234" }));

    expect(await navigator.clipboard.readText()).toBe("http://localhost:3001/abc1234");
    expect(await screen.findByText("Copied!")).toBeInTheDocument();
  });

  it("edits the destination optimistically", async () => {
    vi.mocked(updateLink).mockResolvedValueOnce({
      ...firstLink,
      original_url: "https://example.org/new-destination",
    });
    const browser = userEvent.setup();
    renderView();

    await browser.click(screen.getByRole("button", { name: "Edit: abc1234" }));

    const dialog = screen.getByRole("dialog");
    expect(within(dialog).getByLabelText("Short code")).toHaveValue("abc1234");
    expect(within(dialog).getByLabelText("Short code")).toHaveAttribute("readonly");

    const title = within(dialog).getByLabelText("Title");
    await browser.clear(title);
    await browser.type(title, "New title");
    const destination = within(dialog).getByLabelText("Destination URL");
    await browser.clear(destination);
    await browser.type(destination, "https://example.org/new-destination");
    const expiry = within(dialog).getByLabelText("Expires at");
    fireEvent.change(expiry, { target: { value: "2030-01-01T12:00" } });
    await browser.click(within(dialog).getByRole("button", { name: "Save changes" }));

    await waitFor(() =>
      expect(updateLink).toHaveBeenCalledWith(
        "abc1234",
        expect.objectContaining({
          title: "New title",
          original_url: "https://example.org/new-destination",
          expires_at: expect.any(String),
        }),
      ),
    );
    expect(await screen.findByText("https://example.org/new-destination")).toBeInTheDocument();
    expect(await screen.findByText("Link updated.")).toBeInTheDocument();
  });

  it("rolls back an edit when the API fails", async () => {
    vi.mocked(updateLink).mockRejectedValueOnce(
      new ApiError({ status: 500, code: "server_error", message: "boom" }),
    );
    const browser = userEvent.setup();
    renderView();

    await browser.click(screen.getByRole("button", { name: "Edit: abc1234" }));
    const dialog = screen.getByRole("dialog");
    const destination = within(dialog).getByLabelText("Destination URL");
    await browser.clear(destination);
    await browser.type(destination, "https://example.org/never-saved");
    await browser.click(within(dialog).getByRole("button", { name: "Save changes" }));

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "We couldn't save your changes. The previous values were restored.",
    );
    expect(
      screen.getByText("https://example.com/a-very-long-destination-path"),
    ).toBeInTheDocument();
  });

  it("deletes a link after confirmation", async () => {
    vi.mocked(deleteLink).mockResolvedValueOnce(undefined);
    const browser = userEvent.setup();
    renderView();

    await browser.click(screen.getByRole("button", { name: "Delete: abc1234" }));
    const dialog = screen.getByRole("dialog");
    expect(dialog).toHaveTextContent("The short link abc1234 will stop working immediately.");
    await browser.click(within(dialog).getByRole("button", { name: "Delete link" }));

    await waitFor(() => expect(deleteLink).toHaveBeenCalledWith("abc1234"));
    expect(screen.queryByRole("link", { name: "Open details: abc1234" })).not.toBeInTheDocument();
    expect(await screen.findByText("Link deleted.")).toBeInTheDocument();
  });

  it("restores a link when deletion fails", async () => {
    vi.mocked(deleteLink).mockRejectedValueOnce(
      new ApiError({ status: 500, code: "server_error", message: "boom" }),
    );
    const browser = userEvent.setup();
    renderView();

    await browser.click(screen.getByRole("button", { name: "Delete: abc1234" }));
    await browser.click(
      within(screen.getByRole("dialog")).getByRole("button", { name: "Delete link" }),
    );

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "We couldn't delete the link. It was restored to the list.",
    );
    expect(screen.getByRole("link", { name: "Open details: abc1234" })).toBeInTheDocument();
  });

  it("loads the next cursor page and appends the results", async () => {
    vi.mocked(listLinks).mockResolvedValueOnce({
      items: [secondLink],
      next_cursor: null,
    });
    const browser = userEvent.setup();
    render(
      <NextIntlClientProvider
        locale="en"
        messages={enMessages as AbstractIntlMessages}
        timeZone="UTC"
      >
        <LinksView
          initialPage={{ items: [firstLink], next_cursor: "cursor-1" }}
          initialSummary={{ clicks: 9, links: 2 }}
        />
      </NextIntlClientProvider>,
    );

    await browser.click(screen.getByRole("button", { name: "Load more" }));

    await waitFor(() =>
      expect(listLinks).toHaveBeenCalledWith({ cursor: "cursor-1", limit: 20, q: "" }),
    );
    expect(await screen.findByRole("link", { name: "Open details: def5678" })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Load more" })).not.toBeInTheDocument();
  });

  it("searches with the q parameter after a short debounce", async () => {
    vi.mocked(listLinks).mockResolvedValueOnce({ items: [], next_cursor: null });
    const browser = userEvent.setup();
    renderView();

    await browser.type(screen.getByLabelText("Search links"), "launch");

    await waitFor(() => expect(listLinks).toHaveBeenCalledWith({ limit: 20, q: "launch" }), {
      timeout: 2_000,
    });
    expect(await screen.findByText("No links found")).toBeInTheDocument();
  });
});
