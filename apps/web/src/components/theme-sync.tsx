"use client";

import { usePathname } from "next/navigation";
import { useLocale } from "next-intl";
import { useEffect, useLayoutEffect } from "react";

import { applyTheme, readTheme } from "@/lib/theme";

const useIsomorphicLayoutEffect =
  typeof window === "undefined" ? useEffect : useLayoutEffect;

export function ThemeSync() {
  const locale = useLocale();
  const pathname = usePathname();

  useIsomorphicLayoutEffect(() => {
    applyTheme(readTheme());
  }, [locale, pathname]);

  return null;
}
