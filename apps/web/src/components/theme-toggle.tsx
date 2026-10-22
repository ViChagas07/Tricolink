"use client";

import { Moon, Sun } from "lucide-react";
import { useTranslations } from "next-intl";

import { readTheme, storeTheme } from "@/lib/theme";

export function ThemeToggle() {
  const t = useTranslations("nav");

  function toggleTheme() {
    const next = readTheme() === "dark" ? "light" : "dark";
    storeTheme(next);
  }

  return (
    <button
      type="button"
      aria-label={t("theme")}
      title={t("theme")}
      onClick={toggleTheme}
      className="inline-flex size-9 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
    >
      <Moon className="size-4 dark:hidden" aria-hidden="true" />
      <Sun className="hidden size-4 dark:block" aria-hidden="true" />
    </button>
  );
}
