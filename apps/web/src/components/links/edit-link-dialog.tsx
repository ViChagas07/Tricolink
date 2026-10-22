"use client";

import { Loader2, X } from "lucide-react";
import { useTranslations } from "next-intl";
import { useId, useState, type FormEvent } from "react";

import { Button } from "@/components/ui/button";
import { Modal } from "@/components/ui/modal";
import {
  fromDateTimeLocal,
  toDateTimeLocal,
  type LinkDto,
  type UpdateLinkInput,
} from "@/lib/links";
import { normalizeShortenUrl, validateShortenUrl } from "@/lib/link-form";
import { cn } from "@/lib/utils";

type EditLinkDialogProps = {
  link: LinkDto;
  onClose: () => void;
  onSave: (input: UpdateLinkInput) => void;
};

type EditErrors = {
  destination?: "required" | "invalid" | "too_long";
  expiry?: "invalid";
};

export function EditLinkDialog({ link, onClose, onSave }: EditLinkDialogProps) {
  const t = useTranslations("links");
  const errorsText = useTranslations("errors");
  const titleId = useId();
  const headingId = useId();
  const destinationId = useId();
  const expiryId = useId();
  const codeId = useId();

  const [title, setTitle] = useState(link.title ?? "");
  const [destination, setDestination] = useState(link.original_url);
  const [expiry, setExpiry] = useState(() => toDateTimeLocal(link.expires_at));
  const [errors, setErrors] = useState<EditErrors>({});
  const [saving, setSaving] = useState(false);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (saving) {
      return;
    }

    const validation = validateShortenUrl(destination);
    const nextErrors: EditErrors = {};
    if (validation) {
      nextErrors.destination = validation;
    }
    if (expiry) {
      const parsed = Date.parse(expiry);
      if (Number.isNaN(parsed) || parsed <= Date.now()) {
        nextErrors.expiry = "invalid";
      }
    }

    setErrors(nextErrors);
    if (nextErrors.destination || nextErrors.expiry) {
      return;
    }

    setSaving(true);
    onSave({
      title: title.trim() ? title.trim() : null,
      original_url: normalizeShortenUrl(destination),
      expires_at: fromDateTimeLocal(expiry),
    });
  }

  const destinationError = errors.destination
    ? errors.destination === "required"
      ? errorsText("urlRequired")
      : errors.destination === "too_long"
        ? errorsText("urlTooLong")
        : errorsText("invalidUrl")
    : null;

  return (
    <Modal open onClose={onClose} labelledBy={headingId}>
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 id={headingId} className="font-heading text-xl font-semibold">
            {t("editTitle")}
          </h2>
          <p className="mt-1 text-sm text-muted-foreground">{t("editDescription")}</p>
        </div>
        <button
          type="button"
          onClick={onClose}
          aria-label={t("cancel")}
          className="inline-flex size-9 shrink-0 items-center justify-center rounded-lg text-muted-foreground hover:bg-muted hover:text-foreground"
        >
          <X aria-hidden="true" className="size-4" />
        </button>
      </div>

      <form noValidate onSubmit={handleSubmit} className="mt-5 space-y-4">
        <div>
          <label htmlFor={codeId} className="text-sm font-medium">
            {t("codeLabel")}
          </label>
          <input
            id={codeId}
            type="text"
            readOnly
            value={link.code}
            dir="ltr"
            className="mt-1.5 h-10 w-full cursor-not-allowed rounded-xl border border-border bg-muted px-3 font-mono text-sm text-muted-foreground"
          />
        </div>

        <div>
          <label htmlFor={titleId} className="text-sm font-medium">
            {t("titleLabel")}
          </label>
          <input
            id={titleId}
            type="text"
            maxLength={120}
            value={title}
            autoFocus
            onChange={(event) => setTitle(event.target.value)}
            placeholder={t("titlePlaceholder")}
            className="mt-1.5 h-10 w-full rounded-xl border border-input bg-background px-3 text-sm shadow-sm outline-none transition-colors placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/30"
          />
        </div>

        <div>
          <label htmlFor={destinationId} className="text-sm font-medium">
            {t("destinationLabel")}
          </label>
          <input
            id={destinationId}
            type="url"
            inputMode="url"
            dir="ltr"
            value={destination}
            aria-invalid={Boolean(errors.destination)}
            aria-describedby={destinationError ? `${destinationId}-error` : undefined}
            onChange={(event) => {
              setDestination(event.target.value);
              setErrors((current) => ({ ...current, destination: undefined }));
            }}
            className={cn(
              "mt-1.5 h-10 w-full rounded-xl border border-input bg-background px-3 text-sm shadow-sm outline-none transition-colors focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/30",
              "aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20",
            )}
          />
          {destinationError ? (
            <p id={`${destinationId}-error`} className="mt-1.5 text-xs text-destructive">
              {destinationError}
            </p>
          ) : null}
        </div>

        <div>
          <label htmlFor={expiryId} className="text-sm font-medium">
            {t("expiresLabel")}
          </label>
          <input
            id={expiryId}
            type="datetime-local"
            value={expiry}
            aria-invalid={Boolean(errors.expiry)}
            aria-describedby={errors.expiry ? `${expiryId}-error` : `${expiryId}-hint`}
            onChange={(event) => {
              setExpiry(event.target.value);
              setErrors((current) => ({ ...current, expiry: undefined }));
            }}
            className={cn(
              "mt-1.5 h-10 w-full rounded-xl border border-input bg-background px-3 text-sm shadow-sm outline-none transition-colors focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/30",
              "aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20",
            )}
          />
          {errors.expiry ? (
            <p id={`${expiryId}-error`} className="mt-1.5 text-xs text-destructive">
              {t("expiryInvalid")}
            </p>
          ) : (
            <p id={`${expiryId}-hint`} className="mt-1.5 text-xs text-muted-foreground">
              {t("expiresHint")}
            </p>
          )}
        </div>

        <div className="flex flex-col-reverse gap-2 pt-2 sm:flex-row sm:justify-end">
          <Button type="button" variant="outline" onClick={onClose} className="h-10 px-4">
            {t("cancel")}
          </Button>
          <Button type="submit" disabled={saving} className="h-10 px-4">
            {saving ? <Loader2 aria-hidden="true" className="size-4 animate-spin" /> : null}
            {t("save")}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
