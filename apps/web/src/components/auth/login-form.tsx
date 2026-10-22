"use client";

import { ArrowLeft, Eye, EyeOff, Loader2, LogIn, TriangleAlert, UserPlus } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useId, useRef, useState, type FormEvent, type KeyboardEvent } from "react";

import { Button } from "@/components/ui/button";
import { Link, useRouter } from "@/i18n/navigation";
import { api, isApiError } from "@/lib/api";
import { toNavigationTarget } from "@/lib/next-path";
import { useRetryCountdown } from "@/lib/use-retry-countdown";
import { cn } from "@/lib/utils";
import { mapUserDto, useAuthStore } from "@/stores/auth-store";

type Mode = "login" | "register";

type FieldError = "required" | "invalid" | "short" | "long" | "weak";

type FieldErrors = {
  email?: FieldError;
  password?: FieldError;
};

type FormError =
  | { type: "invalid_credentials" | "account_conflict" | "network" | "generic" | "google" }
  | { type: "rate_limit"; retryAt: number };

const MAX_EMAIL_LENGTH = 254;
const MIN_PASSWORD_LENGTH = 10;
const MAX_PASSWORD_LENGTH = 128;
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

type LoginFormProps = {
  nextPath: string;
  initialError?: "google" | null;
};

function validate(mode: Mode, email: string, password: string): FieldErrors {
  const errors: FieldErrors = {};
  const trimmedEmail = email.trim();

  if (!trimmedEmail) {
    errors.email = "required";
  } else if (trimmedEmail.length > MAX_EMAIL_LENGTH || !EMAIL_PATTERN.test(trimmedEmail)) {
    errors.email = "invalid";
  }

  if (!password) {
    errors.password = "required";
  } else if (password.length > MAX_PASSWORD_LENGTH) {
    errors.password = "long";
  } else if (mode === "register" && password.length < MIN_PASSWORD_LENGTH) {
    errors.password = "short";
  }

  return errors;
}

export function LoginForm({ nextPath, initialError = null }: LoginFormProps) {
  const t = useTranslations("auth");
  const errors = useTranslations("errors");
  const locale = useLocale();
  const router = useRouter();
  const setUser = useAuthStore((state) => state.setUser);

  const fieldId = useId();
  const emailId = `${fieldId}-email`;
  const passwordId = `${fieldId}-password`;
  const emailErrorId = `${emailId}-error`;
  const passwordErrorId = `${passwordId}-error`;
  const errorId = `${fieldId}-form-error`;

  const tabLoginRef = useRef<HTMLButtonElement>(null);
  const tabRegisterRef = useRef<HTMLButtonElement>(null);

  const [mode, setMode] = useState<Mode>("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [formError, setFormError] = useState<FormError | null>(
    initialError === "google" ? { type: "google" } : null,
  );

  const secondsLeft = useRetryCountdown(
    formError?.type === "rate_limit" ? formError.retryAt : null,
  );
  const googleHref = `/api/v1/auth/google/login?next=${encodeURIComponent(nextPath)}`;

  function switchMode(nextMode: Mode) {
    if (nextMode === mode) {
      return;
    }
    setMode(nextMode);
    setPassword("");
    setShowPassword(false);
    setFieldErrors({});
    setFormError(null);
  }

  function handleTabKeyDown(event: KeyboardEvent<HTMLButtonElement>) {
    if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") {
      return;
    }
    event.preventDefault();
    const nextMode: Mode = mode === "login" ? "register" : "login";
    switchMode(nextMode);
    const nextTab = nextMode === "login" ? tabLoginRef.current : tabRegisterRef.current;
    nextTab?.focus();
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const validation = validate(mode, email, password);
    setFieldErrors(validation);
    setFormError(null);
    if (validation.email || validation.password) {
      return;
    }

    setSubmitting(true);
    try {
      if (mode === "register") {
        await api.register({ email: email.trim(), password });
      }

      const response = await api.login({ email: email.trim(), password });
      setUser(mapUserDto(response.user));

      const target = toNavigationTarget(nextPath, locale);
      router.replace(target.path, target.locale ? { locale: target.locale } : undefined);
    } catch (error) {
      if (isApiError(error)) {
        if (error.status === 429) {
          const retryAfter = Math.max(1, error.retryAfter ?? 60);
          setFormError({ type: "rate_limit", retryAt: Date.now() + retryAfter * 1000 });
        } else if (error.status === 401) {
          setFormError({ type: "invalid_credentials" });
        } else if (error.status === 409) {
          setFormError({ type: "account_conflict" });
        } else if (error.code === "weak_password") {
          setFieldErrors({ password: "weak" });
        } else if (error.code === "invalid_email") {
          setFieldErrors({ email: "invalid" });
        } else if (error.status === 0 || error.code === "network_error") {
          setFormError({ type: "network" });
        } else {
          setFormError({ type: "generic" });
        }
      } else {
        setFormError({ type: "generic" });
      }
    } finally {
      setSubmitting(false);
    }
  }

  const emailError = fieldErrors.email;
  const passwordError = fieldErrors.password;
  const emailErrorText = emailError
    ? emailError === "required"
      ? t("emailRequired")
      : t("emailInvalid")
    : null;
  const passwordErrorText = passwordError
    ? passwordError === "required"
      ? t("passwordRequired")
      : passwordError === "short"
        ? t("passwordTooShort")
        : passwordError === "long"
          ? t("passwordTooLong")
          : t("passwordWeak")
    : null;

  return (
    <div>
      <div
        role="tablist"
        aria-label={t("tabsLabel")}
        className="grid grid-cols-2 gap-1 rounded-xl bg-muted p-1"
      >
        <button
          ref={tabLoginRef}
          id={`${fieldId}-tab-login`}
          type="button"
          role="tab"
          aria-selected={mode === "login"}
          aria-controls={`${fieldId}-panel`}
          tabIndex={mode === "login" ? 0 : -1}
          onClick={() => switchMode("login")}
          onKeyDown={handleTabKeyDown}
          className={cn(
            "inline-flex h-10 items-center justify-center gap-2 rounded-lg px-3 text-sm font-semibold transition-colors",
            mode === "login"
              ? "bg-card text-foreground shadow-sm"
              : "text-muted-foreground hover:text-foreground",
          )}
        >
          <LogIn aria-hidden="true" className="size-4" />
          {t("login")}
        </button>
        <button
          ref={tabRegisterRef}
          id={`${fieldId}-tab-register`}
          type="button"
          role="tab"
          aria-selected={mode === "register"}
          aria-controls={`${fieldId}-panel`}
          tabIndex={mode === "register" ? 0 : -1}
          onClick={() => switchMode("register")}
          onKeyDown={handleTabKeyDown}
          className={cn(
            "inline-flex h-10 items-center justify-center gap-2 rounded-lg px-3 text-sm font-semibold transition-colors",
            mode === "register"
              ? "bg-card text-foreground shadow-sm"
              : "text-muted-foreground hover:text-foreground",
          )}
        >
          <UserPlus aria-hidden="true" className="size-4" />
          {t("register")}
        </button>
      </div>

      <div
        id={`${fieldId}-panel`}
        role="tabpanel"
        aria-labelledby={`${fieldId}-tab-${mode}`}
        className="mt-6"
      >
        <h1 className="font-heading text-2xl font-bold tracking-tight text-tc-blue-950 dark:text-tc-white">
          {mode === "login" ? t("loginTitle") : t("registerTitle")}
        </h1>
        <p className="mt-1.5 text-sm text-muted-foreground">
          {mode === "login" ? t("loginSubtitle") : t("registerSubtitle")}
        </p>

        <a
          href={googleHref}
          className={cn(
            "mt-6 inline-flex h-11 w-full items-center justify-center gap-2.5 rounded-xl border border-border bg-background px-4 text-sm font-semibold text-foreground shadow-sm transition-colors hover:bg-muted focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/40",
            submitting && "pointer-events-none opacity-50",
          )}
          aria-disabled={submitting}
        >
          <span
            aria-hidden="true"
            className="grid size-5 place-items-center rounded-full border border-border bg-card text-xs font-bold text-tc-blue-700 dark:text-tc-blue-100"
          >
            G
          </span>
          {t("google")}
        </a>

        <div className="my-5 flex items-center gap-3">
          <span className="h-px flex-1 bg-border" aria-hidden="true" />
          <span className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
            {t("or")}
          </span>
          <span className="h-px flex-1 bg-border" aria-hidden="true" />
        </div>

        {formError ? (
          <div
            id={errorId}
            role="alert"
            className="mb-4 flex items-start gap-2.5 rounded-xl border border-destructive/30 bg-destructive/5 px-3.5 py-3 text-sm text-destructive"
          >
            <TriangleAlert aria-hidden="true" className="mt-0.5 size-4 shrink-0" />
            <div>
              {formError.type === "rate_limit" ? (
                <>
                  <p className="font-semibold">{t("rateLimitedTitle")}</p>
                  <p className="mt-0.5">
                    {secondsLeft > 0
                      ? errors("rateLimited", { seconds: secondsLeft })
                      : t("rateLimitedReady")}
                  </p>
                </>
              ) : (
                <p>
                  {formError.type === "invalid_credentials"
                    ? t("invalidCredentials")
                    : formError.type === "account_conflict"
                      ? t("accountConflict")
                      : formError.type === "google"
                        ? t("googleError")
                        : formError.type === "network"
                          ? errors("network")
                          : errors("generic")}
                </p>
              )}
            </div>
          </div>
        ) : null}

        <form noValidate aria-busy={submitting} onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor={emailId} className="text-sm font-medium">
              {t("email")}
            </label>
            <input
              id={emailId}
              type="email"
              inputMode="email"
              dir="ltr"
              autoComplete="email"
              maxLength={MAX_EMAIL_LENGTH}
              value={email}
              aria-invalid={Boolean(emailError)}
              aria-describedby={emailErrorText ? emailErrorId : undefined}
              onChange={(event) => {
                setEmail(event.target.value);
                setFieldErrors((current) => ({ ...current, email: undefined }));
                setFormError(null);
              }}
              className={cn(
                "mt-1.5 h-11 w-full rounded-xl border border-input bg-background px-3.5 text-sm text-foreground shadow-sm outline-none transition-colors",
                "placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/30",
                "aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20",
              )}
            />
            {emailErrorText ? (
              <p id={emailErrorId} className="mt-1.5 text-xs text-destructive">
                {emailErrorText}
              </p>
            ) : null}
          </div>

          <div>
            <label htmlFor={passwordId} className="text-sm font-medium">
              {t("password")}
            </label>
            <div className="relative mt-1.5">
              <input
                id={passwordId}
                type={showPassword ? "text" : "password"}
                autoComplete={mode === "register" ? "new-password" : "current-password"}
                maxLength={MAX_PASSWORD_LENGTH}
                value={password}
                aria-invalid={Boolean(passwordError)}
                aria-describedby={
                  passwordErrorText
                    ? passwordErrorId
                    : mode === "register"
                      ? `${passwordId}-hint`
                      : undefined
                }
                onChange={(event) => {
                  setPassword(event.target.value);
                  setFieldErrors((current) => ({ ...current, password: undefined }));
                  setFormError(null);
                }}
                className={cn(
                  "h-11 w-full rounded-xl border border-input bg-background px-3.5 pe-11 text-sm text-foreground shadow-sm outline-none transition-colors",
                  "focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/30",
                  "aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20",
                )}
              />
              <button
                type="button"
                aria-label={showPassword ? t("hidePassword") : t("showPassword")}
                aria-pressed={showPassword}
                onClick={() => setShowPassword((value) => !value)}
                className="absolute end-1 top-1/2 inline-flex size-9 -translate-y-1/2 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
              >
                {showPassword ? (
                  <EyeOff aria-hidden="true" className="size-4" />
                ) : (
                  <Eye aria-hidden="true" className="size-4" />
                )}
              </button>
            </div>
            {passwordErrorText ? (
              <p id={passwordErrorId} className="mt-1.5 text-xs text-destructive">
                {passwordErrorText}
              </p>
            ) : mode === "register" ? (
              <p id={`${passwordId}-hint`} className="mt-1.5 text-xs text-muted-foreground">
                {t("passwordHint")}
              </p>
            ) : null}
          </div>

          <Button
            type="submit"
            variant="brand"
            size="lg"
            disabled={submitting || secondsLeft > 0}
            className="h-11 w-full rounded-xl text-base font-semibold"
          >
            {submitting ? <Loader2 aria-hidden="true" className="size-4 animate-spin" /> : null}
            {mode === "login" ? t("login") : t("register")}
          </Button>
        </form>

        <p className="mt-4 text-center text-sm text-muted-foreground">
          {mode === "login" ? t("noAccount") : t("hasAccount")}{" "}
          <button
            type="button"
            onClick={() => switchMode(mode === "login" ? "register" : "login")}
            className="font-semibold text-tc-blue-700 underline-offset-4 hover:underline dark:text-tc-blue-100"
          >
            {mode === "login" ? t("register") : t("login")}
          </button>
        </p>
      </div>

      <div className="mt-6 border-t border-border pt-4">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft aria-hidden="true" className="size-4 rtl:rotate-180" />
          {t("backHome")}
        </Link>
      </div>
    </div>
  );
}
