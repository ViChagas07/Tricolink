"use client";

import {
  ArrowRight,
  Check,
  CheckCircle2,
  Copy,
  Link2,
  Loader2,
  ShieldCheck,
  Sparkles,
  TriangleAlert,
} from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useId, useRef, useState, type FormEvent } from "react";

import { Button } from "@/components/ui/button";
import { Link } from "@/i18n/navigation";
import { api, isApiError } from "@/lib/api";
import { normalizeShortenUrl, validateShortenUrl } from "@/lib/link-form";
import { useRetryCountdown } from "@/lib/use-retry-countdown";
import { safeExternalHref } from "@/lib/url";
import { cn } from "@/lib/utils";
import { useAuthStore } from "@/stores/auth-store";

type CreateLinkResponse = {
  code: string;
  short_url: string;
  original_url: string;
  created_at: string;
  expires_at: string | null;
};

type FormError =
  | { type: "required" | "invalid" | "too_long" | "own_host" | "network" | "generic" }
  | { type: "rate_limit"; retryAt: number };

type CopyState = "idle" | "copied" | "error";

const REQUEST_TIMEOUT_MS = 20_000;

function getOwnHosts(): string[] {
  const hosts = new Set<string>();
  if (typeof window !== "undefined" && window.location.hostname) {
    hosts.add(window.location.hostname.toLowerCase());
  }

  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL;
  if (siteUrl) {
    try {
      hosts.add(new URL(siteUrl).hostname.toLowerCase());
    } catch {
      // Ignore a malformed public URL; the current host still protects the app.
    }
  }

  return [...hosts];
}

const ERROR_KEYS = {
  required: "urlRequired",
  invalid: "invalidUrl",
  too_long: "urlTooLong",
  network: "network",
  generic: "generic",
} as const;

export function ShortenForm() {
  const t = useTranslations("hero");
  const errors = useTranslations("errors");
  const user = useAuthStore((state) => state.user);
  const status = useAuthStore((state) => state.status);

  const inputId = useId();
  const errorId = `${inputId}-error`;
  const [url, setUrl] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<FormError | null>(null);
  const [result, setResult] = useState<CreateLinkResponse | null>(null);
  const [copyState, setCopyState] = useState<CopyState>("idle");
  const [cancelled, setCancelled] = useState(false);
  const requestRef = useRef<AbortController | null>(null);
  const timeoutRef = useRef<number | null>(null);

  const secondsLeft = useRetryCountdown(error?.type === "rate_limit" ? error.retryAt : null);
  const authenticated = status === "authenticated" && user !== null;
  const inputInvalid = error !== null && error.type !== "rate_limit";

  useEffect(() => {
    if (copyState === "idle") {
      return;
    }

    const timer = window.setTimeout(() => setCopyState("idle"), 2500);
    return () => window.clearTimeout(timer);
  }, [copyState]);

  useEffect(() => {
    return () => {
      requestRef.current?.abort("unmount");
      if (timeoutRef.current !== null) {
        window.clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  function cancelRequest() {
    requestRef.current?.abort("cancel");
  }

  function handleUrlChange(nextUrl: string) {
    setUrl(nextUrl);
    setCancelled(false);

    const isOwnHost = getOwnHosts().some(
      (host) => validateShortenUrl(nextUrl, host) === "own_host",
    );
    if (isOwnHost) {
      requestRef.current?.abort("own_host");
      setResult(null);
      setError({ type: "own_host" });
      return;
    }

    if (error?.type === "own_host") {
      setError(null);
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const validation = validateShortenUrl(url, getOwnHosts());
    if (validation) {
      if (validation === "own_host") {
        requestRef.current?.abort("own_host");
      }
      setError({ type: validation });
      setResult(null);
      setCancelled(false);
      return;
    }

    setSubmitting(true);
    setCancelled(false);
    setError(null);
    setResult(null);
    setCopyState("idle");

    const controller = new AbortController();
    requestRef.current = controller;
    timeoutRef.current = window.setTimeout(() => controller.abort("timeout"), REQUEST_TIMEOUT_MS);

    try {
      const response = await api.post<CreateLinkResponse>(
        "/links",
        { url: normalizeShortenUrl(url) },
        {
          csrf: status === "anonymous" ? "skip" : "auto",
          signal: controller.signal,
        },
      );
      setResult(response);
      setUrl("");
    } catch (requestError) {
      if (controller.signal.aborted) {
        if (controller.signal.reason === "cancel") {
          setCancelled(true);
        } else if (controller.signal.reason === "timeout") {
          setError({ type: "network" });
        }
        return;
      }

      if (isApiError(requestError)) {
        if (requestError.status === 429) {
          const retryAfter = Math.max(1, requestError.retryAfter ?? 60);
          setError({ type: "rate_limit", retryAt: Date.now() + retryAfter * 1000 });
        } else if (requestError.code === "invalid_url") {
          setError({ type: "invalid" });
        } else if (requestError.status === 0 || requestError.code === "network_error") {
          setError({ type: "network" });
        } else {
          setError({ type: "generic" });
        }
      } else {
        setError({ type: "generic" });
      }
    } finally {
      if (timeoutRef.current !== null) {
        window.clearTimeout(timeoutRef.current);
        timeoutRef.current = null;
      }
      requestRef.current = null;
      setSubmitting(false);
    }
  }

  async function copyShortLink() {
    if (!result) {
      return;
    }

    try {
      await navigator.clipboard.writeText(result.short_url);
      setCopyState("copied");
    } catch {
      setCopyState("error");
    }
  }

  const announcement =
    copyState === "copied"
      ? t("copied")
      : copyState === "error"
        ? t("copyFailed")
        : result
          ? `${t("resultTitle")} ${result.short_url}`
          : "";
  const shortHref = result ? safeExternalHref(result.short_url) : null;

  return (
    <div id="shorten" className="mx-auto w-full max-w-3xl scroll-mt-24">
      <form
        noValidate
        aria-busy={submitting}
        onSubmit={handleSubmit}
        className="rounded-2xl border border-border/80 bg-card p-2 shadow-[0_24px_60px_-32px_rgba(7,26,77,0.55)] sm:p-2.5"
      >
        <div className="flex flex-col gap-2 sm:flex-row sm:items-start">
          <div className="relative min-w-0 flex-1">
            <label htmlFor={inputId} className="sr-only">
              {t("inputLabel")}
            </label>
            <Link2
              aria-hidden="true"
              className="pointer-events-none absolute start-4 top-1/2 size-5 -translate-y-1/2 text-muted-foreground"
            />
            <input
              id={inputId}
              type="url"
              inputMode="url"
              dir="ltr"
              autoComplete="url"
              spellCheck={false}
              placeholder={t("placeholder")}
              value={url}
              aria-invalid={inputInvalid}
              aria-describedby={inputInvalid ? errorId : undefined}
              onChange={(event) => handleUrlChange(event.target.value)}
              className={cn(
                "h-12 w-full rounded-xl border border-transparent bg-transparent pe-4 ps-12 text-base text-foreground outline-none transition-colors",
                "placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/30",
                "aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20",
              )}
            />
          </div>
          <div className="flex shrink-0 flex-col gap-2">
            <Button
              type="submit"
              variant="brand"
              disabled={submitting || secondsLeft > 0 || error?.type === "own_host"}
              className="h-12 w-full rounded-xl px-7 text-base font-semibold"
            >
              {submitting ? <Loader2 aria-hidden="true" className="size-5 animate-spin" /> : null}
              {submitting ? t("submitting") : t("submit")}
            </Button>
            {submitting ? (
              <Button
                type="button"
                variant="secondary"
                onClick={cancelRequest}
                className="h-9 w-full rounded-xl"
              >
                {t("cancel")}
              </Button>
            ) : null}
          </div>
        </div>
      </form>

      {error ? (
        <div
          id={errorId}
          role="alert"
          className="mt-3 flex items-start gap-3 rounded-xl border border-destructive/30 bg-destructive/5 px-4 py-3 text-start text-sm text-destructive"
        >
          <TriangleAlert aria-hidden="true" className="mt-0.5 size-5 shrink-0" />
          <div className="min-w-0">
            {error.type === "rate_limit" ? (
              <>
                <p className="font-semibold">{t("limitTitle")}</p>
                <p className="mt-0.5">
                  {secondsLeft > 0 ? t("limitBody", { seconds: secondsLeft }) : t("limitReady")}
                </p>
                <Link
                  href="/login"
                  className="mt-2 inline-flex items-center gap-1 font-semibold underline underline-offset-4"
                >
                  {t("limitCta")}
                  <ArrowRight aria-hidden="true" className="size-4 rtl:rotate-180" />
                </Link>
              </>
            ) : error.type === "own_host" ? (
              <p className="font-semibold">{t("ownUrl")}</p>
            ) : (
              <p>{errors(ERROR_KEYS[error.type])}</p>
            )}
          </div>
        </div>
      ) : null}

      {cancelled ? (
        <p role="status" className="mt-3 text-center text-sm text-muted-foreground">
          {t("cancelled")}
        </p>
      ) : null}

      {result ? (
        <div className="mt-4 rounded-2xl border border-tc-blue-600/25 bg-card p-4 text-start shadow-sm">
          <p className="flex items-center gap-2 text-sm font-semibold text-tc-blue-700 dark:text-tc-blue-100">
            <CheckCircle2 aria-hidden="true" className="size-5" />
            {t("resultTitle")}
          </p>
          <div className="mt-3 flex flex-col gap-3 rounded-xl bg-muted/60 p-3 sm:flex-row sm:items-center sm:justify-between">
            {shortHref ? (
              <a
                href={shortHref}
                dir="ltr"
                target="_blank"
                rel="noopener noreferrer nofollow ugc"
                className="break-all font-mono text-sm font-semibold text-tc-blue-700 underline-offset-4 hover:underline dark:text-tc-blue-100"
              >
                {result.short_url}
              </a>
            ) : (
              <span dir="ltr" className="break-all font-mono text-sm font-semibold">
                {result.short_url}
              </span>
            )}

            <div className="flex flex-wrap items-center gap-2">
              <Button
                type="button"
                variant="outline"
                onClick={() => void copyShortLink()}
                className="h-9"
              >
                {copyState === "copied" ? (
                  <Check aria-hidden="true" className="size-4" />
                ) : (
                  <Copy aria-hidden="true" className="size-4" />
                )}
                {copyState === "copied" ? t("copied") : t("copy")}
              </Button>
              {authenticated ? (
                <Link
                  href={`/links/${result.code}`}
                  className="inline-flex h-9 items-center gap-1 rounded-lg px-2 text-sm font-semibold text-tc-blue-700 hover:underline dark:text-tc-blue-100"
                >
                  {t("stats")}
                  <ArrowRight aria-hidden="true" className="size-4 rtl:rotate-180" />
                </Link>
              ) : null}
            </div>
          </div>
        </div>
      ) : null}

      <span role="status" aria-live="polite" className="sr-only">
        {announcement}
      </span>

      <ul className="mt-4 flex flex-wrap items-center justify-center gap-x-5 gap-y-2 text-xs text-muted-foreground">
        <li className="inline-flex items-center gap-1.5">
          <ShieldCheck aria-hidden="true" className="size-4 text-tc-blue-600" />
          {t("secureNote")}
        </li>
        <li className="inline-flex items-center gap-1.5">
          <Sparkles aria-hidden="true" className="size-4 text-tc-red-600" />
          {t("anonymousNote")}
        </li>
      </ul>
    </div>
  );
}
