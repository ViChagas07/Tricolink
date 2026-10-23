"use client";

import { Check, ImageUp, Loader2, LogOut, Moon, Sun } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import {
  useEffect,
  useId,
  useRef,
  useState,
  type ChangeEvent,
  type FormEvent,
} from "react";

import { ProfileAvatar } from "@/components/profile-avatar";
import { Button } from "@/components/ui/button";
import { usePathname, useRouter } from "@/i18n/navigation";
import { isLocale, localeLabels, locales, type Locale } from "@/i18n/locales";
import { api, isApiError } from "@/lib/api";
import { AvatarError, prepareAvatar } from "@/lib/avatar";
import { readTheme, storeTheme, type Theme } from "@/lib/theme";
import { cn } from "@/lib/utils";
import { mapUserDto, useAuthStore, type AuthUser } from "@/stores/auth-store";

type AccountFormProps = {
  initialUser: AuthUser;
};

type Notice = "saved" | "error" | "network" | "avatar" | null;

export function AccountForm({ initialUser }: AccountFormProps) {
  const t = useTranslations("account");
  const errors = useTranslations("errors");
  const locale = useLocale();
  const router = useRouter();
  const pathname = usePathname();
  const setUser = useAuthStore((state) => state.setUser);
  const logout = useAuthStore((state) => state.logout);

  const nameId = useId();
  const emailId = useId();
  const languageId = useId();
  const avatarInputId = useId();
  const avatarInputRef = useRef<HTMLInputElement>(null);
  const [displayName, setDisplayName] = useState(initialUser.displayName ?? "");
  const [preferredLocale, setPreferredLocale] = useState<Locale>(() =>
    isLocale(initialUser.locale) ? initialUser.locale : isLocale(locale) ? locale : "en",
  );
  const [avatarUrl, setAvatarUrl] = useState(initialUser.avatarUrl);
  const [avatarSource, setAvatarSource] = useState(initialUser.avatarSource);
  const [theme, setTheme] = useState<Theme>("light");
  const [savingName, setSavingName] = useState(false);
  const [savingLocale, setSavingLocale] = useState(false);
  const [uploadingAvatar, setUploadingAvatar] = useState(false);
  const [signingOut, setSigningOut] = useState(false);
  const [notice, setNotice] = useState<Notice>(null);

  useEffect(() => {
    const timer = window.setTimeout(() => setTheme(readTheme()), 0);
    return () => window.clearTimeout(timer);
  }, []);

  function handleError(error: unknown) {
    if (isApiError(error) && (error.status === 0 || error.code === "network_error")) {
      setNotice("network");
      return;
    }
    setNotice("error");
  }

  async function handleProfileSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (savingName) {
      return;
    }

    setSavingName(true);
    setNotice(null);
    try {
      const updated = await api.updateMe({ display_name: displayName.trim() || null });
      setUser(mapUserDto(updated));
      setDisplayName(updated.display_name ?? "");
      setNotice("saved");
    } catch (error) {
      handleError(error);
    } finally {
      setSavingName(false);
    }
  }

  async function handleAvatarSelected(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file || uploadingAvatar) {
      return;
    }

    setUploadingAvatar(true);
    setNotice(null);
    try {
      const prepared = await prepareAvatar(file);
      const updated = await api.updateAvatar(prepared);
      setUser(mapUserDto(updated));
      setAvatarUrl(updated.avatar_url);
      setAvatarSource(updated.avatar_source);
      setNotice("saved");
    } catch (error) {
      if (error instanceof AvatarError) {
        setNotice("avatar");
      } else {
        handleError(error);
      }
    } finally {
      setUploadingAvatar(false);
    }
  }

  async function handleAvatarRemove() {
    if (uploadingAvatar || avatarSource !== "custom") {
      return;
    }

    setUploadingAvatar(true);
    setNotice(null);
    try {
      const updated = await api.deleteAvatar();
      setUser(mapUserDto(updated));
      setAvatarUrl(updated.avatar_url);
      setAvatarSource(updated.avatar_source);
      setNotice("saved");
    } catch (error) {
      handleError(error);
    } finally {
      setUploadingAvatar(false);
    }
  }

  async function handleLocaleChange(nextLocale: Locale) {
    if (nextLocale === preferredLocale || savingLocale) {
      return;
    }

    const previous = preferredLocale;
    setPreferredLocale(nextLocale);
    setSavingLocale(true);
    setNotice(null);
    try {
      const updated = await api.updateMe({ locale: nextLocale });
      setUser(mapUserDto(updated));
      router.replace(pathname, { locale: nextLocale });
    } catch (error) {
      setPreferredLocale(previous);
      handleError(error);
    } finally {
      setSavingLocale(false);
    }
  }

  function handleThemeChange(nextTheme: Theme) {
    storeTheme(nextTheme);
    setTheme(nextTheme);
  }

  async function handleSignOut() {
    if (signingOut) {
      return;
    }
    setSigningOut(true);
    await logout();
    router.replace("/");
    router.refresh();
  }

  return (
    <div className="mx-auto w-full max-w-4xl px-4 py-10 sm:px-6 sm:py-14">
      <header>
        <h1 className="font-heading text-3xl font-bold tracking-tight text-tc-blue-950 sm:text-4xl dark:text-tc-white">
          {t("title")}
        </h1>
        <p className="mt-2 max-w-xl text-muted-foreground">{t("subtitle")}</p>
      </header>

      {notice ? (
        <div
          role={notice === "saved" ? "status" : "alert"}
          className={cn(
            "mt-6 flex items-start gap-2.5 rounded-xl border px-4 py-3 text-sm",
            notice === "saved"
              ? "border-tc-blue-600/30 bg-tc-blue-100/50 text-tc-blue-800 dark:bg-tc-blue-600/10 dark:text-tc-blue-100"
              : "border-destructive/30 bg-destructive/5 text-destructive",
          )}
        >
          {notice === "saved" ? (
            <Check aria-hidden="true" className="mt-0.5 size-4 shrink-0" />
          ) : null}
          <p>
            {notice === "saved"
              ? t("saved")
              : notice === "avatar"
                ? t("avatarError")
                : notice === "network"
                  ? errors("network")
                  : errors("generic")}
          </p>
        </div>
      ) : null}

      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <section
          aria-labelledby="account-profile-heading"
          className="rounded-2xl border border-border bg-card p-5 shadow-sm sm:p-6"
        >
          <h2 id="account-profile-heading" className="font-heading text-lg font-semibold">
            {t("profile")}
          </h2>

          <div className="mt-5 flex items-center gap-4">
            <ProfileAvatar
              displayName={displayName || initialUser.displayName}
              email={initialUser.email}
              avatarUrl={avatarUrl}
              className="size-20 text-xl"
            />
            <div className="min-w-0">
              <p className="text-sm font-medium">{t("photo")}</p>
              <p className="mt-1 text-xs text-muted-foreground">{t("photoHint")}</p>
              <div className="mt-3 flex flex-wrap gap-2">
                <Button
                  type="button"
                  variant="outline"
                  disabled={uploadingAvatar}
                  onClick={() => avatarInputRef.current?.click()}
                  className="h-9 px-3"
                >
                  {uploadingAvatar ? (
                    <Loader2 aria-hidden="true" className="size-4 animate-spin" />
                  ) : (
                    <ImageUp aria-hidden="true" className="size-4" />
                  )}
                  {uploadingAvatar ? t("uploadingPhoto") : t("changePhoto")}
                </Button>
                {avatarSource === "custom" ? (
                  <Button
                    type="button"
                    variant="ghost"
                    disabled={uploadingAvatar}
                    onClick={() => void handleAvatarRemove()}
                    className="h-9 px-3"
                  >
                    {t("removePhoto")}
                  </Button>
                ) : null}
              </div>
              <input
                ref={avatarInputRef}
                id={avatarInputId}
                type="file"
                accept="image/jpeg,image/png,image/webp"
                className="sr-only"
                aria-label={t("changePhoto")}
                onChange={(event) => void handleAvatarSelected(event)}
              />
            </div>
          </div>

          <form onSubmit={handleProfileSubmit} className="mt-6 space-y-4">
            <div>
              <label htmlFor={nameId} className="text-sm font-medium">
                {t("displayName")}
              </label>
              <input
                id={nameId}
                type="text"
                autoComplete="name"
                maxLength={80}
                value={displayName}
                onChange={(event) => {
                  setDisplayName(event.target.value);
                  setNotice(null);
                }}
                placeholder={t("displayNamePlaceholder")}
                className="mt-1.5 h-11 w-full rounded-xl border border-input bg-background px-3.5 text-sm shadow-sm outline-none transition-colors placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/30"
              />
            </div>

            <div>
              <label htmlFor={emailId} className="text-sm font-medium">
                {t("email")}
              </label>
              <input
                id={emailId}
                type="email"
                dir="ltr"
                readOnly
                value={initialUser.email}
                aria-describedby={`${emailId}-hint`}
                className="mt-1.5 h-11 w-full cursor-not-allowed rounded-xl border border-border bg-muted px-3.5 text-sm text-muted-foreground"
              />
              <p id={`${emailId}-hint`} className="mt-1.5 text-xs text-muted-foreground">
                {t("emailHint")}
              </p>
            </div>

            <Button type="submit" disabled={savingName} className="h-10 px-4">
              {savingName ? <Loader2 aria-hidden="true" className="size-4 animate-spin" /> : null}
              {savingName ? t("saving") : t("save")}
            </Button>
          </form>
        </section>

        <section
          aria-labelledby="account-preferences-heading"
          className="rounded-2xl border border-border bg-card p-5 shadow-sm sm:p-6"
        >
          <h2 id="account-preferences-heading" className="font-heading text-lg font-semibold">
            {t("preferences")}
          </h2>

          <div className="mt-5 space-y-5">
            <div>
              <label htmlFor={languageId} className="text-sm font-medium">
                {t("language")}
              </label>
              <select
                id={languageId}
                value={preferredLocale}
                disabled={savingLocale}
                aria-describedby={`${languageId}-hint`}
                onChange={(event) => {
                  const next = event.target.value;
                  if (isLocale(next)) {
                    void handleLocaleChange(next);
                  }
                }}
                className="mt-1.5 h-11 w-full rounded-xl border border-input bg-background px-3 text-sm shadow-sm outline-none transition-colors focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/30 disabled:opacity-60"
              >
                {locales.map((code) => (
                  <option key={code} value={code} lang={code}>
                    {localeLabels[code]}
                  </option>
                ))}
              </select>
              <p id={`${languageId}-hint`} className="mt-1.5 text-xs text-muted-foreground">
                {t("languageHint")}
              </p>
            </div>

            <fieldset>
              <legend className="text-sm font-medium">{t("theme")}</legend>
              <div className="mt-1.5 grid grid-cols-2 gap-2">
                <button
                  type="button"
                  aria-pressed={theme === "light"}
                  onClick={() => handleThemeChange("light")}
                  className={cn(
                    "inline-flex h-11 items-center justify-center gap-2 rounded-xl border px-3 text-sm font-medium transition-colors",
                    theme === "light"
                      ? "border-tc-blue-600 bg-tc-blue-100 text-tc-blue-800 dark:bg-tc-blue-600/20 dark:text-tc-blue-100"
                      : "border-border bg-background text-muted-foreground hover:bg-muted",
                  )}
                >
                  <Sun aria-hidden="true" className="size-4" />
                  {t("themeLight")}
                </button>
                <button
                  type="button"
                  aria-pressed={theme === "dark"}
                  onClick={() => handleThemeChange("dark")}
                  className={cn(
                    "inline-flex h-11 items-center justify-center gap-2 rounded-xl border px-3 text-sm font-medium transition-colors",
                    theme === "dark"
                      ? "border-tc-blue-600 bg-tc-blue-100 text-tc-blue-800 dark:bg-tc-blue-600/20 dark:text-tc-blue-100"
                      : "border-border bg-background text-muted-foreground hover:bg-muted",
                  )}
                >
                  <Moon aria-hidden="true" className="size-4" />
                  {t("themeDark")}
                </button>
              </div>
            </fieldset>
          </div>
        </section>
      </div>

      <section
        aria-labelledby="account-session-heading"
        className="mt-6 flex flex-col gap-4 rounded-2xl border border-border bg-card p-5 shadow-sm sm:flex-row sm:items-center sm:justify-between sm:p-6"
      >
        <div>
          <h2 id="account-session-heading" className="font-heading text-lg font-semibold">
            {t("session")}
          </h2>
          <p className="mt-1 text-sm text-muted-foreground">{t("logoutHint")}</p>
        </div>
        <Button
          type="button"
          variant="destructive"
          disabled={signingOut}
          onClick={() => void handleSignOut()}
          className="h-10 shrink-0 px-4"
        >
          {signingOut ? (
            <Loader2 aria-hidden="true" className="size-4 animate-spin" />
          ) : (
            <LogOut aria-hidden="true" className="size-4 rtl:rotate-180" />
          )}
          {t("logout")}
        </Button>
      </section>
    </div>
  );
}
