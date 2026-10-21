"use client";

import { Check, ChevronDown, Globe } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";

import { usePathname, useRouter } from "@/i18n/navigation";
import { defaultLocale, isLocale, localeLabels, locales, type Locale } from "@/i18n/locales";
import { cn } from "@/lib/utils";

export function LanguageSwitcher() {
  const t = useTranslations("nav");
  const locale = useLocale();
  const currentLocale: Locale = isLocale(locale) ? locale : defaultLocale;
  const pathname = usePathname();
  const router = useRouter();

  const [open, setOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(() => locales.indexOf(currentLocale));
  const buttonLabel = `${t("selectLanguage")}: ${localeLabels[currentLocale]}`;
  const containerRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const optionRefs = useRef<Array<HTMLButtonElement | null>>([]);

  useEffect(() => {
    if (!open) {
      return;
    }

    optionRefs.current[activeIndex]?.focus();

    const handlePointerDown = (event: PointerEvent) => {
      if (!containerRef.current?.contains(event.target as Node)) {
        setOpen(false);
      }
    };

    document.addEventListener("pointerdown", handlePointerDown);
    return () => document.removeEventListener("pointerdown", handlePointerDown);
  }, [open, activeIndex]);

  function selectLocale(nextLocale: Locale) {
    setOpen(false);
    buttonRef.current?.focus();
    if (nextLocale === currentLocale) {
      return;
    }
    router.replace(pathname, { locale: nextLocale });
  }

  function moveActive(delta: number) {
    setActiveIndex((index) => (index + delta + locales.length) % locales.length);
  }

  function handleListKeyDown(event: React.KeyboardEvent<HTMLUListElement>) {
    switch (event.key) {
      case "ArrowDown":
        event.preventDefault();
        moveActive(1);
        break;
      case "ArrowUp":
        event.preventDefault();
        moveActive(-1);
        break;
      case "Home":
        event.preventDefault();
        setActiveIndex(0);
        break;
      case "End":
        event.preventDefault();
        setActiveIndex(locales.length - 1);
        break;
      case "Escape":
        event.preventDefault();
        setOpen(false);
        buttonRef.current?.focus();
        break;
      default:
        break;
    }
  }

  return (
    <div ref={containerRef} className="relative">
      <button
        ref={buttonRef}
        type="button"
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-label={buttonLabel}
        onClick={() => {
          setActiveIndex(locales.indexOf(currentLocale));
          setOpen((value) => !value);
        }}
        onKeyDown={(event) => {
          if (event.key === "ArrowDown" || event.key === "ArrowUp") {
            event.preventDefault();
            setActiveIndex(locales.indexOf(currentLocale));
            setOpen(true);
          }
        }}
        className="inline-flex h-9 items-center gap-1.5 rounded-lg px-2.5 text-sm font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
      >
        <Globe className="size-4" aria-hidden="true" />
        <span className="max-w-36 truncate" dir="auto">
          {localeLabels[currentLocale]}
        </span>
        <ChevronDown className="size-3.5 opacity-70" aria-hidden="true" />
      </button>

      {open ? (
        <ul
          role="listbox"
          aria-label={t("selectLanguage")}
          onKeyDown={handleListKeyDown}
          className="absolute start-0 top-full z-50 mt-2 max-h-80 w-60 overflow-y-auto rounded-xl border border-border bg-popover p-1 text-popover-foreground shadow-lg"
        >
          {locales.map((code, index) => (
            <li key={code} role="presentation">
              <button
                ref={(element) => {
                  optionRefs.current[index] = element;
                }}
                type="button"
                role="option"
                aria-selected={code === currentLocale}
                tabIndex={index === activeIndex ? 0 : -1}
                dir="auto"
                onClick={() => selectLocale(code)}
                onFocus={() => setActiveIndex(index)}
                className={cn(
                  "flex w-full items-center justify-between gap-3 rounded-lg px-2.5 py-2 text-start text-sm",
                  code === currentLocale
                    ? "bg-accent font-semibold text-accent-foreground"
                    : "text-foreground hover:bg-muted",
                )}
              >
                <span lang={code}>{localeLabels[code]}</span>
                {code === currentLocale ? <Check className="size-4" aria-hidden="true" /> : null}
              </button>
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}
