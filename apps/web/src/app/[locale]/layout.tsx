import type { Metadata } from "next";
import { headers } from "next/headers";
import { Inter, Plus_Jakarta_Sans } from "next/font/google";
import { NextIntlClientProvider } from "next-intl";
import { getMessages, getTranslations } from "next-intl/server";
import type { ReactNode } from "react";

import { Footer } from "@/components/footer";
import { Navbar } from "@/components/navbar";
import { defaultLocale, getDirection, isLocale } from "@/i18n/locales";
import { routing } from "@/i18n/routing";
import { siteUrl } from "@/lib/seo";
import { cn } from "@/lib/utils";

import "../globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const jakarta = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--font-jakarta",
  display: "swap",
});

export const dynamic = "force-dynamic";

const THEME_SCRIPT = `(function(){try{var key="tricolink-theme";var stored=localStorage.getItem(key);var dark=stored?stored==="dark":window.matchMedia("(prefers-color-scheme: dark)").matches;var root=document.documentElement;root.classList.toggle("dark",dark);root.style.colorScheme=dark?"dark":"light";}catch(e){}})();`;

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

type LocaleLayoutProps = {
  children: ReactNode;
  params: Promise<{ locale: string }>;
};

export async function generateMetadata({
  params,
}: Pick<LocaleLayoutProps, "params">): Promise<Metadata> {
  const { locale: rawLocale } = await params;
  const locale = isLocale(rawLocale) ? rawLocale : defaultLocale;
  const t = await getTranslations({ locale, namespace: "meta" });

  return {
    metadataBase: new URL(siteUrl),
    title: {
      default: t("title"),
      template: "%s · Tricolink",
    },
    description: t("description"),
    applicationName: "Tricolink",
    openGraph: {
      type: "website",
      siteName: "Tricolink",
      title: t("title"),
      description: t("description"),
      url: `/${locale}`,
      locale: locale.replace("-", "_"),
    },
    twitter: {
      card: "summary_large_image",
      title: t("title"),
      description: t("description"),
    },
    robots: { index: true, follow: true },
  };
}

export default async function LocaleLayout({ children, params }: LocaleLayoutProps) {
  const { locale: rawLocale } = await params;
  const locale = isLocale(rawLocale) ? rawLocale : defaultLocale;
  const direction = getDirection(locale);
  const messages = await getMessages({ locale });
  const nonce = (await headers()).get("x-nonce") ?? undefined;
  const nav = await getTranslations({ locale, namespace: "nav" });

  return (
    <html
      lang={locale}
      dir={direction}
      className={cn(inter.variable, jakarta.variable)}
      suppressHydrationWarning
    >
      <head>
        <script nonce={nonce}>{THEME_SCRIPT}</script>
      </head>
      <body className="min-h-screen bg-background font-sans text-foreground antialiased">
        <div aria-hidden="true" className="tc-tricolor-bar h-1 w-full" />
        <a
          href="#main"
          className="sr-only focus:not-sr-only focus:fixed focus:start-4 focus:top-4 focus:z-50 focus:rounded-lg focus:bg-primary focus:px-4 focus:py-2 focus:text-sm focus:font-semibold focus:text-primary-foreground"
        >
          {nav("skipToContent")}
        </a>
        <NextIntlClientProvider locale={locale} messages={messages} timeZone="UTC">
          <Navbar />
          <main id="main" tabIndex={-1}>
            {children}
          </main>
          <Footer />
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
