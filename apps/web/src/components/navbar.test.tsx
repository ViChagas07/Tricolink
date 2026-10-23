import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { NextIntlClientProvider, type AbstractIntlMessages } from "next-intl";
import { beforeEach, describe, expect, it, vi } from "vitest";

import arMessages from "../../messages/ar.json";
import enMessages from "../../messages/en.json";
import { Navbar } from "./navbar";

const navigation = vi.hoisted(() => ({
  replace: vi.fn(),
  pathname: "/links",
}));

vi.mock("@/i18n/navigation", () => ({
  usePathname: () => navigation.pathname,
  useRouter: () => ({ replace: navigation.replace }),
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
    load: vi.fn(),
  },
}));

vi.mock("@/stores/auth-store", () => ({
  useAuthStore: (selector: (state: typeof authState.current) => unknown) =>
    selector(authState.current),
}));

function renderNavbar(locale: "en" | "ar", messages: unknown) {
  return render(
    <NextIntlClientProvider
      locale={locale}
      messages={messages as AbstractIntlMessages}
      timeZone="UTC"
    >
      <Navbar />
    </NextIntlClientProvider>,
  );
}

describe("Navbar", () => {
  beforeEach(() => {
    navigation.replace.mockReset();
    navigation.pathname = "/links";
    authState.current.user = null;
    authState.current.status = "anonymous";
  });

  it("renders the English navigation in LTR", () => {
    renderNavbar("en", enMessages);

    const header = screen.getByRole("banner");
    expect(header).toHaveAttribute("dir", "ltr");
    expect(screen.getByRole("link", { name: "Tricolink home" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Links" })).toHaveAttribute(
      "href",
      "/login?next=%2Fen%2Flinks",
    );
    expect(screen.getByRole("link", { name: "Sign in" })).toHaveAttribute("href", "/login");
    expect(screen.getByRole("button", { name: /Select language/ })).toBeInTheDocument();
  });

  it("hides the sign-in action on the login page", () => {
    navigation.pathname = "/login";
    renderNavbar("en", enMessages);

    expect(screen.queryByRole("link", { name: "Sign in" })).not.toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Links" })).toBeInTheDocument();
  });

  it("renders the Arabic navigation in RTL", () => {
    renderNavbar("ar", arMessages);

    expect(screen.getByRole("banner")).toHaveAttribute("dir", "rtl");
    expect(screen.getByRole("link", { name: arMessages.nav.links })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: arMessages.nav.login })).toHaveAttribute(
      "href",
      "/login",
    );
    expect(
      screen.getByRole("button", { name: new RegExp(arMessages.nav.selectLanguage) }),
    ).toBeInTheDocument();
  });

  it("switches locale while preserving the current route", async () => {
    const user = userEvent.setup();
    renderNavbar("en", enMessages);

    await user.click(screen.getByRole("button", { name: /Select language/ }));
    await user.click(screen.getByRole("option", { name: "العربية" }));

    expect(navigation.replace).toHaveBeenCalledWith("/links", { locale: "ar" });
  });

  it("shows the account menu when authenticated", () => {
    authState.current.user = { id: "1", email: "ada@example.com", displayName: "Ada" };
    authState.current.status = "authenticated";
    renderNavbar("en", enMessages);

    expect(screen.getByLabelText(/Account/)).toBeInTheDocument();
    expect(screen.getByText("Sign out")).toBeInTheDocument();
    expect(screen.queryByRole("link", { name: "Sign in" })).not.toBeInTheDocument();
  });

  it("keeps language and theme controls below Links in the mobile menu", async () => {
    const user = userEvent.setup();
    renderNavbar("en", enMessages);

    await user.click(screen.getByRole("button", { name: "Open menu" }));

    const dialog = screen.getByRole("dialog");
    expect(within(dialog).getByRole("button", { name: /Select language/ })).toBeInTheDocument();
    expect(within(dialog).getByRole("button", { name: "Toggle theme" })).toBeInTheDocument();
    expect(within(dialog).queryByRole("link", { name: "Sign in" })).not.toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Sign in" })).toBeInTheDocument();
  });
});
