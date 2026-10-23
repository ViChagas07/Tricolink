import { render } from "@testing-library/react";
import { NextIntlClientProvider, type AbstractIntlMessages } from "next-intl";
import { beforeEach, describe, expect, it, vi } from "vitest";

import enMessages from "../../messages/en.json";
import { THEME_STORAGE_KEY } from "@/lib/theme";
import { ThemeSync } from "./theme-sync";

vi.mock("next/navigation", () => ({
  usePathname: () => "/en",
}));

function providers(locale: string) {
  return (
    <NextIntlClientProvider
      locale={locale}
      messages={enMessages as AbstractIntlMessages}
      timeZone="UTC"
    >
      <ThemeSync />
    </NextIntlClientProvider>
  );
}

describe("ThemeSync", () => {
  beforeEach(() => {
    window.localStorage.clear();
    document.documentElement.classList.remove("dark");
    document.documentElement.style.colorScheme = "";
  });

  it("reapplies the stored dark theme after the locale changes", () => {
    window.localStorage.setItem(THEME_STORAGE_KEY, "dark");
    const { rerender } = render(providers("en"));
    expect(document.documentElement).toHaveClass("dark");

    document.documentElement.classList.remove("dark");
    document.documentElement.style.colorScheme = "";
    rerender(providers("pt-BR"));

    expect(document.documentElement).toHaveClass("dark");
    expect(document.documentElement.style.colorScheme).toBe("dark");
    expect(window.localStorage.getItem(THEME_STORAGE_KEY)).toBe("dark");
  });

  it("keeps the light theme after the locale changes", () => {
    window.localStorage.setItem(THEME_STORAGE_KEY, "light");
    const { rerender } = render(providers("en"));
    expect(document.documentElement).not.toHaveClass("dark");

    rerender(providers("pt-BR"));

    expect(document.documentElement).not.toHaveClass("dark");
    expect(window.localStorage.getItem(THEME_STORAGE_KEY)).toBe("light");
  });
});
