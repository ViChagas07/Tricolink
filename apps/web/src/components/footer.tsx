import { getTranslations } from "next-intl/server";

import { BrandLogo } from "@/components/brand-logo";
import { LanguageSwitcher } from "@/components/language-switcher";
import { Link } from "@/i18n/navigation";

export async function Footer() {
  const t = await getTranslations("footer");
  const nav = await getTranslations("nav");
  const auth = await getTranslations("auth");
  const year = new Date().getFullYear();

  return (
    <footer className="border-t border-border/70 bg-card">
      <div className="mx-auto grid w-full max-w-6xl gap-8 px-4 py-10 sm:px-6 md:grid-cols-[1.4fr_1fr_1fr]">
        <div>
          <BrandLogo label={nav("home")} />
          <p className="mt-3 max-w-xs text-sm text-muted-foreground">{t("tagline")}</p>
        </div>

        <nav aria-label={t("product")}>
          <h2 className="text-sm font-semibold text-foreground">{t("product")}</h2>
          <ul className="mt-3 space-y-2 text-sm">
            <li>
              <Link href="/" className="text-muted-foreground hover:text-foreground">
                {nav("home")}
              </Link>
            </li>
            <li>
              <Link
                href="/links"
                prefetch={false}
                className="text-muted-foreground hover:text-foreground"
              >
                {nav("links")}
              </Link>
            </li>
          </ul>
        </nav>

        <nav aria-label={t("account")}>
          <h2 className="text-sm font-semibold text-foreground">{t("account")}</h2>
          <ul className="mt-3 space-y-2 text-sm">
            <li>
              <Link
                href="/login"
                prefetch={false}
                className="text-muted-foreground hover:text-foreground"
              >
                {auth("login")}
              </Link>
            </li>
            <li>
              <Link
                href="/account"
                prefetch={false}
                className="text-muted-foreground hover:text-foreground"
              >
                {nav("account")}
              </Link>
            </li>
          </ul>
        </nav>

        <div className="flex flex-col gap-3 border-t border-border/70 pt-6 text-sm text-muted-foreground md:col-span-3 md:flex-row md:items-center md:justify-between">
          <p>{t("copyright", { year })}</p>
          <div className="flex items-center gap-2">
            <span className="text-xs font-medium uppercase tracking-wide">{t("language")}</span>
            <LanguageSwitcher />
          </div>
        </div>
      </div>
    </footer>
  );
}
