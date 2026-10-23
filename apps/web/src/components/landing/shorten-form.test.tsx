import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { NextIntlClientProvider, type AbstractIntlMessages } from "next-intl";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import arMessages from "../../../messages/ar.json";
import enMessages from "../../../messages/en.json";
import { ApiError, api } from "@/lib/api";

import { ShortenForm } from "./shorten-form";

vi.mock("@/i18n/navigation", () => ({
  Link: ({
    href,
    children,
    locale: _locale,
    prefetch: _prefetch,
    ...props
  }: Omit<React.AnchorHTMLAttributes<HTMLAnchorElement>, "href"> & {
    href: string | { pathname: string };
    locale?: string;
    prefetch?: boolean;
  }) => {
    void _locale;
    void _prefetch;
    return (
      <a href={typeof href === "string" ? href : href.pathname} {...props}>
        {children}
      </a>
    );
  },
}));

const authState = vi.hoisted(() => ({
  current: {
    user: null as { id: string; email: string; displayName: string | null } | null,
    status: "anonymous" as "anonymous" | "authenticated" | "idle" | "loading",
  },
}));

vi.mock("@/stores/auth-store", () => ({
  useAuthStore: (selector: (state: typeof authState.current) => unknown) =>
    selector(authState.current),
}));

function renderForm(locale: "en" | "ar" = "en", messages: unknown = enMessages) {
  return render(
    <NextIntlClientProvider
      locale={locale}
      messages={messages as AbstractIntlMessages}
      timeZone="UTC"
    >
      <ShortenForm />
    </NextIntlClientProvider>,
  );
}

function linkResponse() {
  return {
    code: "abc1234",
    short_url: "https://tricolink.test/abc1234",
    original_url: "https://example.com/",
    title: null,
    created_at: "2026-10-21T12:00:00Z",
    expires_at: "2026-11-20T12:00:00Z",
    is_active: true,
    click_count: 0,
  };
}

describe("ShortenForm", () => {
  beforeEach(() => {
    authState.current.user = null;
    authState.current.status = "anonymous";
    vi.spyOn(api, "post").mockReset();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllEnvs();
  });

  it("shows a translated validation error without calling the API", async () => {
    const user = userEvent.setup();
    renderForm();

    await user.type(screen.getByLabelText("Long URL"), "not-a-url");
    await user.click(screen.getByRole("button", { name: "Shorten" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("Enter a valid http or https URL.");
    expect(screen.getByLabelText("Long URL")).toHaveAttribute("aria-invalid", "true");
    expect(api.post).not.toHaveBeenCalled();
  });

  it("creates a short link, copies it and announces the result", async () => {
    const user = userEvent.setup();
    vi.spyOn(api, "post").mockResolvedValue(linkResponse() as never);
    renderForm();

    await user.type(screen.getByLabelText("Long URL"), "https://example.com");
    await user.click(screen.getByRole("button", { name: "Shorten" }));

    expect(await screen.findByText("https://tricolink.test/abc1234")).toBeInTheDocument();
    expect(screen.getByText("Your short link is ready")).toBeInTheDocument();
    expect(api.post).toHaveBeenCalledWith(
      "/links",
      { url: "https://example.com/" },
      expect.objectContaining({ csrf: "skip", signal: expect.any(AbortSignal) }),
    );

    await user.click(screen.getByRole("button", { name: "Copy" }));

    expect(await screen.findByRole("button", { name: "Copied!" })).toBeInTheDocument();
    await expect(navigator.clipboard.readText()).resolves.toBe("https://tricolink.test/abc1234");
    expect(screen.getByRole("status")).toHaveTextContent("Copied!");
    expect(screen.queryByRole("link", { name: "View statistics" })).not.toBeInTheDocument();
  });

  it("warns immediately and disables submit for the app's own host", async () => {
    const user = userEvent.setup();
    renderForm();

    await user.type(screen.getByLabelText("Long URL"), "http://localhost/own");

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "For security reasons, you can't shorten a URL from Tricolink itself.",
    );
    expect(screen.getByRole("button", { name: "Shorten" })).toBeDisabled();
    expect(api.post).not.toHaveBeenCalled();
  });

  it("detects the configured public site host", async () => {
    vi.stubEnv("NEXT_PUBLIC_SITE_URL", "https://tricolink.vercel.app");
    const user = userEvent.setup();
    renderForm();

    await user.type(screen.getByLabelText("Long URL"), "https://tricolink.vercel.app/pt-BR");

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "For security reasons, you can't shorten a URL from Tricolink itself.",
    );
    expect(screen.getByRole("button", { name: "Shorten" })).toBeDisabled();
    expect(api.post).not.toHaveBeenCalled();
  });

  it("shows a cancel button while shortening and cancels the request", async () => {
    const user = userEvent.setup();
    let signal: AbortSignal | undefined;
    vi.spyOn(api, "post").mockImplementationOnce(
      (_path, _body, options) =>
        new Promise<never>((_, reject) => {
          signal = options?.signal ?? undefined;
          signal?.addEventListener("abort", () =>
            reject(new DOMException("Aborted", "AbortError")),
          );
        }),
    );
    renderForm();

    await user.type(screen.getByLabelText("Long URL"), "https://example.com");
    await user.click(screen.getByRole("button", { name: "Shorten" }));

    const cancel = await screen.findByRole("button", { name: "Cancel" });
    expect(screen.getByRole("button", { name: "Shortening…" })).toBeDisabled();
    await user.click(cancel);

    expect(await screen.findByText("Shortening cancelled.")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Shorten" })).toBeEnabled();
    expect(signal?.aborted).toBe(true);
  });

  it("offers the statistics page to signed-in users", async () => {
    const user = userEvent.setup();
    authState.current.user = { id: "1", email: "ada@example.com", displayName: "Ada" };
    authState.current.status = "authenticated";
    vi.spyOn(api, "post").mockResolvedValue(linkResponse() as never);
    renderForm();

    await user.type(screen.getByLabelText("Long URL"), "https://example.com");
    await user.click(screen.getByRole("button", { name: "Shorten" }));

    const stats = await screen.findByRole("link", { name: "View statistics" });
    expect(stats).toHaveAttribute("href", "/links/abc1234");
  });

  it("starts a countdown and invites the visitor to create an account on 429", async () => {
    const user = userEvent.setup();
    vi.spyOn(api, "post").mockRejectedValue(
      new ApiError({
        message: "Too many requests",
        status: 429,
        code: "rate_limited",
        retryAfter: 5,
      }),
    );
    renderForm();

    await user.type(screen.getByLabelText("Long URL"), "https://example.com");
    await user.click(screen.getByRole("button", { name: "Shorten" }));

    const alert = await screen.findByRole("alert");
    expect(alert).toHaveTextContent("Daily limit reached");
    expect(alert).toHaveTextContent("Try again in 5 seconds");
    expect(screen.getByRole("button", { name: "Shorten" })).toBeDisabled();
    expect(screen.getByRole("link", { name: "Create a free account" })).toHaveAttribute(
      "href",
      "/login",
    );
  });

  it("renders the Arabic form in RTL with translated labels", () => {
    renderForm("ar", arMessages);

    expect(screen.getByLabelText(arMessages.hero.inputLabel)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: arMessages.hero.submit })).toBeInTheDocument();
  });

  it("shows the generic translated error for unexpected failures", async () => {
    const user = userEvent.setup();
    vi.spyOn(api, "post").mockRejectedValue(
      new ApiError({ message: "Boom", status: 503, code: "unavailable" }),
    );
    renderForm();

    await user.type(screen.getByLabelText("Long URL"), "https://example.com");
    await user.click(screen.getByRole("button", { name: "Shorten" }));

    await waitFor(() =>
      expect(screen.getByRole("alert")).toHaveTextContent(
        "Something went wrong. Please try again.",
      ),
    );
  });
});
