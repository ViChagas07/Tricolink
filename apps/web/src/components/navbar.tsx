"use client";

import { Menu, X } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";

import { BrandLogo } from "@/components/brand-logo";
import { LanguageSwitcher } from "@/components/language-switcher";
import { ProfileAvatar, initialsFor } from "@/components/profile-avatar";
import { ThemeToggle } from "@/components/theme-toggle";
import { usePathname, useRouter, Link } from "@/i18n/navigation";
import { defaultLocale, getDirection, isLocale } from "@/i18n/locales";
import { buttonVariants } from "@/components/ui/button";
import type { AuthUser } from "@/stores/auth-store";
import { useAuthStore } from "@/stores/auth-store";
import { cn } from "@/lib/utils";

function AccountMenu({ user }: { user: AuthUser }) {
  const t = useTranslations("nav");
  const router = useRouter();
  const logout = useAuthStore((state) => state.logout);

  async function handleLogout() {
    await logout();
    router.replace("/");
    router.refresh();
  }

  return (
    <details className="group relative">
      <summary
        aria-label={`${t("account")} (${initialsFor(user.displayName, user.email)})`}
        className="flex size-9 cursor-pointer list-none items-center justify-center rounded-full transition-opacity hover:opacity-90 [&::-webkit-details-marker]:hidden"
      >
        <ProfileAvatar
          displayName={user.displayName}
          email={user.email}
          avatarUrl={user.avatarUrl}
          className="size-9"
        />
      </summary>
      <div className="absolute end-0 top-full z-50 mt-2 w-60 rounded-xl border border-border bg-popover p-1 text-popover-foreground shadow-lg">
        <div className="border-b border-border px-3 py-2.5">
          <p className="truncate text-sm font-semibold">{user.displayName ?? user.email}</p>
          {user.displayName ? (
            <p className="truncate text-xs text-muted-foreground">{user.email}</p>
          ) : null}
        </div>
        <Link
          href="/account"
          prefetch={false}
          className="mt-1 flex rounded-lg px-3 py-2 text-sm hover:bg-muted focus-visible:bg-muted"
        >
          {t("account")}
        </Link>
        <button
          type="button"
          onClick={(event) => {
            const details = event.currentTarget.closest("details");
            if (details) {
              details.open = false;
            }
            void handleLogout();
          }}
          className="flex w-full rounded-lg px-3 py-2 text-start text-sm text-destructive hover:bg-destructive/10 focus-visible:bg-destructive/10"
        >
          {t("logout")}
        </button>
      </div>
    </details>
  );
}

export function Navbar() {
  const t = useTranslations("nav");
  const locale = useLocale();
  const currentLocale = isLocale(locale) ? locale : defaultLocale;
  const direction = getDirection(currentLocale);
  const pathname = usePathname();
  const router = useRouter();

  const user = useAuthStore((state) => state.user);
  const status = useAuthStore((state) => state.status);
  const load = useAuthStore((state) => state.load);
  const logout = useAuthStore((state) => state.logout);

  const [mobileOpen, setMobileOpen] = useState(false);
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    if (!mobileOpen) {
      return;
    }

    if (dialogRef.current && !dialogRef.current.open) {
      dialogRef.current.showModal();
    }

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = previousOverflow;
    };
  }, [mobileOpen]);

  function closeMobileMenu() {
    dialogRef.current?.close();
    setMobileOpen(false);
  }

  async function handleLogout() {
    closeMobileMenu();
    await logout();
    router.replace("/");
    router.refresh();
  }

  const linksActive = pathname === "/links" || pathname.startsWith("/links/");
  const linksHref = user
    ? "/links"
    : `/login?next=${encodeURIComponent(`/${currentLocale}/links`)}`;
  const isAuthenticated = status === "authenticated" && user !== null;
  const isLoginPage = pathname === "/login" || pathname.startsWith("/login/");

  return (
    <header
      dir={direction}
      className="sticky top-0 z-40 border-b border-border/70 bg-background/85 backdrop-blur supports-[backdrop-filter]:bg-background/70"
    >
      <nav
        aria-label={t("main")}
        className="mx-auto flex h-16 w-full max-w-6xl items-center gap-1 px-4 sm:h-[4.5rem] sm:px-6"
      >
        <BrandLogo label={t("home")} />
        <div className="ms-2 hidden sm:block">
          <LanguageSwitcher />
        </div>

        <div className="ms-auto hidden items-center gap-1 md:flex">
          <Link
            href={linksHref}
            prefetch={false}
            aria-current={linksActive ? "page" : undefined}
            className={cn(
              "rounded-lg px-3 py-2 text-sm font-medium transition-colors hover:bg-muted hover:text-foreground",
              linksActive ? "bg-accent text-accent-foreground" : "text-muted-foreground",
            )}
          >
            {t("links")}
          </Link>
          <ThemeToggle />
        </div>

        <div className="ms-auto flex items-center gap-1 md:ms-1">
          {isLoginPage ? null : isAuthenticated && user ? (
            <AccountMenu user={user} />
          ) : (
            <Link
              href="/login"
              prefetch={false}
              className={buttonVariants({ variant: "default", size: "lg" })}
            >
              {t("login")}
            </Link>
          )}

          <button
            type="button"
            aria-label={t("openMenu")}
            aria-expanded={mobileOpen}
            onClick={() => setMobileOpen(true)}
            className="inline-flex size-9 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-muted hover:text-foreground md:hidden"
          >
            <Menu className="size-5" aria-hidden="true" />
          </button>
        </div>
      </nav>

      {mobileOpen ? (
        <dialog
          ref={dialogRef}
          aria-labelledby="mobile-menu-title"
          onClose={() => setMobileOpen(false)}
          onClick={(event) => {
            if (event.target === event.currentTarget) {
              closeMobileMenu();
            }
          }}
          className="tc-sheet fixed inset-0 m-0 h-dvh max-h-dvh w-full max-w-none overflow-hidden border-0 bg-transparent p-0 md:hidden"
        >
          <div className="ms-auto flex h-full w-[min(20rem,85vw)] flex-col overflow-y-auto bg-background p-4 shadow-2xl">
            <div className="flex items-center justify-between gap-2">
              <h2 id="mobile-menu-title" className="font-heading text-lg font-semibold">
                {t("menuTitle")}
              </h2>
              <button
                type="button"
                aria-label={t("closeMenu")}
                onClick={closeMobileMenu}
                className="inline-flex size-9 items-center justify-center rounded-lg text-muted-foreground hover:bg-muted hover:text-foreground"
              >
                <X className="size-5" aria-hidden="true" />
              </button>
            </div>

            <nav aria-label={t("main")} className="mt-6 flex flex-col gap-1">
              <Link
                href={linksHref}
                prefetch={false}
                aria-current={linksActive ? "page" : undefined}
                onClick={closeMobileMenu}
                className={cn(
                  "rounded-lg px-3 py-2.5 text-sm font-medium",
                  linksActive
                    ? "bg-accent text-accent-foreground"
                    : "text-foreground hover:bg-muted",
                )}
              >
                {t("links")}
              </Link>
              <div className="mt-2 flex items-center justify-between gap-2 border-y border-border py-3">
                <LanguageSwitcher />
                <ThemeToggle />
              </div>
              {isAuthenticated && user ? (
                <>
                  <Link
                    href="/account"
                    prefetch={false}
                    onClick={closeMobileMenu}
                    className="rounded-lg px-3 py-2.5 text-sm font-medium text-foreground hover:bg-muted"
                  >
                    {t("account")}
                  </Link>
                  <button
                    type="button"
                    onClick={() => void handleLogout()}
                    className="rounded-lg px-3 py-2.5 text-start text-sm font-medium text-destructive hover:bg-destructive/10"
                  >
                    {t("logout")}
                  </button>
                </>
              ) : null}
            </nav>
          </div>
        </dialog>
      ) : null}
    </header>
  );
}
