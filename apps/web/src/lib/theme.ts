export type Theme = "light" | "dark";

export const THEME_STORAGE_KEY = "tricolink-theme";

export function readTheme(): Theme {
  if (typeof document === "undefined") {
    return "light";
  }

  if (document.documentElement.classList.contains("dark")) {
    return "dark";
  }

  const stored = window.localStorage.getItem(THEME_STORAGE_KEY);
  if (stored === "dark" || stored === "light") {
    return stored;
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

export function applyTheme(theme: Theme): void {
  const root = document.documentElement;
  root.classList.toggle("dark", theme === "dark");
  root.style.colorScheme = theme;
}

export function storeTheme(theme: Theme): void {
  applyTheme(theme);
  window.localStorage.setItem(THEME_STORAGE_KEY, theme);
}
