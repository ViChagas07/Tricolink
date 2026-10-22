"use client";

import { Check, Copy } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";

import { cn } from "@/lib/utils";

type CopyLinkButtonProps = {
  value: string;
  code: string;
  className?: string;
};

export function CopyLinkButton({ value, code, className }: CopyLinkButtonProps) {
  const t = useTranslations("hero");
  const [state, setState] = useState<"idle" | "copied" | "error">("idle");

  useEffect(() => {
    if (state === "idle") {
      return;
    }
    const timer = window.setTimeout(() => setState("idle"), 2_000);
    return () => window.clearTimeout(timer);
  }, [state]);

  async function copy() {
    try {
      await navigator.clipboard.writeText(value);
      setState("copied");
    } catch {
      setState("error");
    }
  }

  return (
    <button
      type="button"
      onClick={() => void copy()}
      aria-label={`${t("copy")}: ${code}`}
      title={t("copy")}
      className={cn(
        "relative z-10 inline-flex size-9 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-muted hover:text-foreground focus-visible:ring-3 focus-visible:ring-ring/40",
        state === "copied" && "text-tc-blue-700 dark:text-tc-blue-100",
        state === "error" && "text-destructive",
        className,
      )}
    >
      {state === "copied" ? (
        <Check aria-hidden="true" className="size-4" />
      ) : (
        <Copy aria-hidden="true" className="size-4" />
      )}
      <span role="status" aria-live="polite" className="sr-only">
        {state === "copied" ? t("copied") : state === "error" ? t("copyFailed") : ""}
      </span>
    </button>
  );
}
