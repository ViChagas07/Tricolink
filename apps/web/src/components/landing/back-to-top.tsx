"use client";

import { ChevronUp } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";

const DEMO_TITLE_ID = "demo-title";

export function BackToTop() {
  const t = useTranslations("nav");
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const target = document.getElementById(DEMO_TITLE_ID);
    if (!target || typeof IntersectionObserver === "undefined") {
      return;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        setVisible(!entry.isIntersecting && entry.boundingClientRect.top < 0);
      },
      { threshold: 0 },
    );

    observer.observe(target);
    return () => observer.disconnect();
  }, []);

  function scrollToTop() {
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
  }

  if (!visible) {
    return null;
  }

  return (
    <button
      type="button"
      aria-label={t("backToTop")}
      onClick={scrollToTop}
      className="fixed right-4 bottom-4 z-40 inline-flex size-11 items-center justify-center rounded-full border border-border bg-background/95 text-foreground shadow-lg backdrop-blur transition-colors hover:bg-muted focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring sm:right-6 sm:bottom-6"
    >
      <ChevronUp aria-hidden="true" className="size-5" />
    </button>
  );
}
