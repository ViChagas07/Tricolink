"use client";

import { Loader2, Trash2 } from "lucide-react";
import { useTranslations } from "next-intl";
import { useId } from "react";

import { Button } from "@/components/ui/button";
import { Modal } from "@/components/ui/modal";

type DeleteLinkDialogProps = {
  code: string | null;
  open: boolean;
  deleting: boolean;
  onClose: () => void;
  onConfirm: () => void;
};

export function DeleteLinkDialog({
  code,
  open,
  deleting,
  onClose,
  onConfirm,
}: DeleteLinkDialogProps) {
  const t = useTranslations("links");
  const headingId = useId();

  return (
    <Modal open={open} onClose={onClose} labelledBy={headingId}>
      <div className="flex items-start gap-3">
        <span className="grid size-10 shrink-0 place-items-center rounded-full bg-destructive/10 text-destructive">
          <Trash2 aria-hidden="true" className="size-5" />
        </span>
        <div>
          <h2 id={headingId} className="font-heading text-xl font-semibold">
            {t("deleteTitle")}
          </h2>
          <p className="mt-2 text-sm text-muted-foreground">
            {t("deleteBody", { code: code ?? "" })}
          </p>
        </div>
      </div>

      <div className="mt-6 flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
        <Button
          type="button"
          variant="outline"
          onClick={onClose}
          disabled={deleting}
          className="h-10 px-4"
        >
          {t("cancel")}
        </Button>
        <Button
          type="button"
          variant="destructive"
          onClick={onConfirm}
          disabled={deleting}
          className="h-10 px-4"
        >
          {deleting ? <Loader2 aria-hidden="true" className="size-4 animate-spin" /> : null}
          {deleting ? t("deleting") : t("deleteConfirm")}
        </Button>
      </div>
    </Modal>
  );
}
