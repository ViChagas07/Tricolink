"use client";

import {
  CalendarDays,
  ExternalLink,
  Link2,
  Loader2,
  MousePointerClick,
  Pencil,
  Search,
  Trash2,
  TriangleAlert,
  X,
} from "lucide-react";
import { useFormatter, useTranslations } from "next-intl";
import { useCallback, useEffect, useRef, useState, type FormEvent } from "react";

import { CopyLinkButton } from "@/components/links/copy-link-button";
import { DeleteLinkDialog } from "@/components/links/delete-link-dialog";
import { EditLinkDialog } from "@/components/links/edit-link-dialog";
import { LinksSkeleton } from "@/components/links/links-skeleton";
import { Button } from "@/components/ui/button";
import { Link } from "@/i18n/navigation";
import { isApiError } from "@/lib/api";
import {
  deleteLink,
  linkStatus,
  listLinks,
  updateLink,
  type LinkDto,
  type ListLinksDto,
  type UpdateLinkInput,
} from "@/lib/links";
import { safeExternalHref } from "@/lib/url";
import { cn } from "@/lib/utils";

type LinksViewProps = {
  initialPage: ListLinksDto | null;
  initialSummary: { clicks: number; links: number } | null;
};

type Notice =
  "updated" | "deleted" | "save_error" | "delete_error" | "network" | "load_error" | null;

function sumClicks(items: LinkDto[]): { clicks: number; links: number } {
  return items.reduce(
    (total, item) => ({
      clicks: total.clicks + (Number.isFinite(item.click_count) ? item.click_count : 0),
      links: total.links + 1,
    }),
    { clicks: 0, links: 0 },
  );
}

function mergeItems(current: LinkDto[], incoming: LinkDto[]): LinkDto[] {
  const seen = new Set(current.map((item) => item.code));
  return [...current, ...incoming.filter((item) => !seen.has(item.code))];
}

function StatusBadge({ link }: { link: LinkDto }) {
  const t = useTranslations("links");
  const status = linkStatus(link);
  const label =
    status === "active"
      ? t("statusActive")
      : status === "inactive"
        ? t("statusInactive")
        : t("statusExpired");

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-2 py-0.5 text-[0.7rem] font-semibold",
        status === "active"
          ? "border-tc-blue-600/25 bg-tc-blue-100/60 text-tc-blue-800 dark:bg-tc-blue-600/15 dark:text-tc-blue-100"
          : status === "expired"
            ? "border-destructive/30 bg-destructive/5 text-destructive"
            : "border-border bg-muted text-muted-foreground",
      )}
    >
      {label}
    </span>
  );
}

function LinkCard({
  link,
  onEdit,
  onDelete,
}: {
  link: LinkDto;
  onEdit: (link: LinkDto) => void;
  onDelete: (link: LinkDto) => void;
}) {
  const t = useTranslations("links");
  const demo = useTranslations("demo");
  const format = useFormatter();
  const href = safeExternalHref(link.short_url);

  return (
    <li className="group relative rounded-2xl border border-border bg-card p-4 shadow-sm transition-colors hover:border-tc-blue-600/40 focus-within:border-tc-blue-600/60 sm:p-5">
      <div className="flex flex-col gap-3">
        <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
          <Link
            href={`/links/${encodeURIComponent(link.code)}`}
            prefetch={false}
            aria-label={`${t("openDetails")}: ${link.code}`}
            className="rounded-sm font-heading text-base font-semibold text-tc-blue-700 underline-offset-4 after:absolute after:inset-0 after:rounded-2xl focus-visible:outline-none focus-visible:after:ring-3 focus-visible:after:ring-ring/40 dark:text-tc-blue-100"
          >
            {link.code}
          </Link>
          <span
            dir="ltr"
            title={link.short_url}
            className="max-w-full truncate font-mono text-xs text-muted-foreground"
          >
            {link.short_url}
          </span>
          <StatusBadge link={link} />
        </div>

        <div className="min-w-0">
          {link.title ? (
            <p className="truncate text-sm font-semibold text-foreground">{link.title}</p>
          ) : null}
          <p
            dir="ltr"
            title={link.original_url}
            className="max-w-full truncate text-sm text-muted-foreground"
          >
            {link.original_url}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-muted-foreground">
          <span className="inline-flex items-center gap-1.5">
            <MousePointerClick aria-hidden="true" className="size-3.5" />
            {format.number(link.click_count)} {demo("clicks")}
          </span>
          <span className="inline-flex items-center gap-1.5">
            <CalendarDays aria-hidden="true" className="size-3.5" />
            {format.dateTime(new Date(link.created_at), { dateStyle: "medium" })}
          </span>
          {link.expires_at ? (
            <span className="inline-flex items-center gap-1.5">
              {t("expires")}: {format.dateTime(new Date(link.expires_at), { dateStyle: "medium" })}
            </span>
          ) : null}
        </div>

        <div className="relative z-10 flex flex-wrap items-center gap-1">
          <CopyLinkButton value={link.short_url} code={link.code} />
          {href ? (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer nofollow ugc"
              aria-label={`${t("open")}: ${link.code}`}
              title={t("open")}
              className="inline-flex size-9 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-muted hover:text-foreground focus-visible:ring-3 focus-visible:ring-ring/40"
            >
              <ExternalLink aria-hidden="true" className="size-4" />
            </a>
          ) : (
            <span
              aria-hidden="true"
              className="inline-flex size-9 items-center justify-center rounded-lg text-muted-foreground opacity-40"
            >
              <ExternalLink className="size-4" />
            </span>
          )}
          <button
            type="button"
            onClick={() => onEdit(link)}
            aria-label={`${t("edit")}: ${link.code}`}
            title={t("edit")}
            className="inline-flex size-9 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-muted hover:text-foreground focus-visible:ring-3 focus-visible:ring-ring/40"
          >
            <Pencil aria-hidden="true" className="size-4" />
          </button>
          <button
            type="button"
            onClick={() => onDelete(link)}
            aria-label={`${t("delete")}: ${link.code}`}
            title={t("delete")}
            className="inline-flex size-9 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-destructive/10 hover:text-destructive focus-visible:ring-3 focus-visible:ring-destructive/30"
          >
            <Trash2 aria-hidden="true" className="size-4" />
          </button>
        </div>
      </div>
    </li>
  );
}

export function LinksView({ initialPage, initialSummary }: LinksViewProps) {
  const t = useTranslations("links");
  const errors = useTranslations("errors");
  const format = useFormatter();

  const [items, setItems] = useState<LinkDto[]>(initialPage?.items ?? []);
  const [nextCursor, setNextCursor] = useState<string | null>(initialPage?.next_cursor ?? null);
  const [query, setQuery] = useState("");
  const [appliedQuery, setAppliedQuery] = useState("");
  const [loading, setLoading] = useState(!initialPage);
  const [loadingMore, setLoadingMore] = useState(false);
  const [loadFailed, setLoadFailed] = useState(false);
  const [notice, setNotice] = useState<Notice>(null);
  const [editing, setEditing] = useState<LinkDto | null>(null);
  const [deleting, setDeleting] = useState<LinkDto | null>(null);
  const [deleteBusy, setDeleteBusy] = useState(false);
  const [summary, setSummary] = useState(initialSummary);
  const requestId = useRef(0);
  const didMount = useRef(false);

  const displaySummary = summary ?? sumClicks(items);

  const loadFirst = useCallback(async (term: string) => {
    const id = ++requestId.current;
    setLoading(true);
    setLoadFailed(false);
    setNotice(null);
    try {
      const page = await listLinks({ limit: 20, q: term });
      if (id !== requestId.current) {
        return;
      }
      setItems(page.items);
      setNextCursor(page.next_cursor);
    } catch (error) {
      if (id !== requestId.current) {
        return;
      }
      setItems([]);
      setNextCursor(null);
      setLoadFailed(true);
      if (isApiError(error) && (error.status === 0 || error.code === "network_error")) {
        setNotice("network");
      }
    } finally {
      if (id === requestId.current) {
        setLoading(false);
      }
    }
  }, []);

  useEffect(() => {
    if (initialPage || didMount.current) {
      didMount.current = true;
      return;
    }
    didMount.current = true;
    void loadFirst("");
  }, [initialPage, loadFirst]);

  useEffect(() => {
    const normalized = query.trim();
    if (normalized === appliedQuery) {
      return;
    }
    const timer = window.setTimeout(() => {
      setAppliedQuery(normalized);
      void loadFirst(normalized);
    }, 350);
    return () => window.clearTimeout(timer);
  }, [appliedQuery, loadFirst, query]);

  function handleSearchSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const normalized = query.trim();
    if (normalized === appliedQuery) {
      return;
    }
    setAppliedQuery(normalized);
    void loadFirst(normalized);
  }

  function clearSearch() {
    setQuery("");
    if (appliedQuery !== "") {
      setAppliedQuery("");
      void loadFirst("");
    }
  }

  async function loadMore() {
    if (!nextCursor || loadingMore) {
      return;
    }
    const id = requestId.current;
    setLoadingMore(true);
    try {
      const page = await listLinks({ cursor: nextCursor, limit: 20, q: appliedQuery });
      if (id !== requestId.current) {
        return;
      }
      setItems((current) => mergeItems(current, page.items));
      setNextCursor(page.next_cursor);
    } catch {
      if (id === requestId.current) {
        setNotice("load_error");
      }
    } finally {
      if (id === requestId.current) {
        setLoadingMore(false);
      }
    }
  }

  function handleSave(input: UpdateLinkInput) {
    if (!editing) {
      return;
    }
    const previous = editing;
    const optimistic: LinkDto = {
      ...previous,
      title: input.title ?? null,
      original_url: input.original_url ?? previous.original_url,
      expires_at: input.expires_at ?? null,
    };

    setItems((current) => current.map((item) => (item.code === previous.code ? optimistic : item)));
    setEditing(null);
    setNotice(null);

    void (async () => {
      try {
        const updated = await updateLink(previous.code, input);
        setItems((current) => current.map((item) => (item.code === updated.code ? updated : item)));
        setNotice("updated");
      } catch (error) {
        if (isApiError(error) && error.status === 404) {
          setItems((current) => current.filter((item) => item.code !== previous.code));
          setNotice("deleted");
          return;
        }
        setItems((current) =>
          current.map((item) => (item.code === previous.code ? previous : item)),
        );
        setNotice(
          isApiError(error) && (error.status === 0 || error.code === "network_error")
            ? "network"
            : "save_error",
        );
      }
    })();
  }

  async function confirmDelete() {
    const target = deleting;
    if (!target || deleteBusy) {
      return;
    }

    const index = items.findIndex((item) => item.code === target.code);
    setDeleteBusy(true);
    setItems((current) => current.filter((item) => item.code !== target.code));
    setDeleting(null);
    setNotice(null);

    try {
      await deleteLink(target.code);
      setSummary((current) =>
        current
          ? {
              clicks: Math.max(0, current.clicks - target.click_count),
              links: Math.max(0, current.links - 1),
            }
          : current,
      );
      setNotice("deleted");
    } catch (error) {
      if (isApiError(error) && error.status === 404) {
        setNotice("deleted");
        return;
      }
      setItems((current) => {
        if (current.some((item) => item.code === target.code)) {
          return current;
        }
        const restored = [...current];
        restored.splice(Math.max(0, Math.min(index, restored.length)), 0, target);
        return restored;
      });
      setNotice(
        isApiError(error) && (error.status === 0 || error.code === "network_error")
          ? "network"
          : "delete_error",
      );
    } finally {
      setDeleteBusy(false);
    }
  }

  const empty = !loading && !loadFailed && items.length === 0;

  return (
    <div className="mx-auto w-full max-w-5xl px-4 py-10 sm:px-6 sm:py-14">
      <header className="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="font-heading text-3xl font-bold tracking-tight text-tc-blue-950 sm:text-4xl dark:text-tc-white">
            {t("title")}
          </h1>
          <p className="mt-2 max-w-xl text-muted-foreground">{t("subtitle")}</p>
        </div>

        <div className="rounded-2xl border border-border bg-card px-5 py-4 shadow-sm">
          <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            {t("totalClicks")}
          </p>
          <p className="mt-1 font-heading text-3xl font-bold text-tc-blue-950 dark:text-tc-white">
            {format.number(displaySummary.clicks)}
          </p>
          <p className="mt-0.5 text-xs text-muted-foreground">
            {t("linkCount", { count: displaySummary.links })}
          </p>
        </div>
      </header>

      {notice ? (
        <div
          role={notice === "updated" || notice === "deleted" ? "status" : "alert"}
          className={cn(
            "mt-6 rounded-xl border px-4 py-3 text-sm",
            notice === "updated" || notice === "deleted"
              ? "border-tc-blue-600/30 bg-tc-blue-100/50 text-tc-blue-800 dark:bg-tc-blue-600/10 dark:text-tc-blue-100"
              : "border-destructive/30 bg-destructive/5 text-destructive",
          )}
        >
          {notice === "updated"
            ? t("updatedAnnouncement")
            : notice === "deleted"
              ? t("deletedAnnouncement")
              : notice === "save_error"
                ? t("saveError")
                : notice === "delete_error"
                  ? t("deleteError")
                  : notice === "network"
                    ? errors("network")
                    : t("loadError")}
        </div>
      ) : null}

      <form
        role="search"
        onSubmit={handleSearchSubmit}
        className="mt-6 flex items-center gap-2 rounded-2xl border border-border bg-card p-2 shadow-sm"
      >
        <label htmlFor="links-search" className="sr-only">
          {t("search")}
        </label>
        <Search aria-hidden="true" className="ms-2 size-4 shrink-0 text-muted-foreground" />
        <input
          id="links-search"
          type="search"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder={t("searchPlaceholder")}
          className="h-9 min-w-0 flex-1 bg-transparent px-1 text-sm outline-none placeholder:text-muted-foreground"
        />
        {query ? (
          <button
            type="button"
            onClick={clearSearch}
            aria-label={t("clearSearch")}
            title={t("clearSearch")}
            className="inline-flex size-8 items-center justify-center rounded-lg text-muted-foreground hover:bg-muted hover:text-foreground"
          >
            <X aria-hidden="true" className="size-4" />
          </button>
        ) : null}
        <Button type="submit" variant="outline" className="h-9 shrink-0 px-3">
          {t("search")}
        </Button>
      </form>

      <section aria-busy={loading} className="mt-6">
        <span className="sr-only" role="status" aria-live="polite">
          {loading ? t("loading") : ""}
        </span>

        {loading ? <LinksSkeleton rows={3} /> : null}

        {loadFailed && !loading ? (
          <div className="rounded-2xl border border-destructive/30 bg-destructive/5 p-6 text-center">
            <TriangleAlert aria-hidden="true" className="mx-auto size-8 text-destructive" />
            <h2 className="mt-3 font-heading text-lg font-semibold">{t("loadError")}</h2>
            <p className="mt-1 text-sm text-muted-foreground">{errors("generic")}</p>
            <Button
              type="button"
              variant="outline"
              onClick={() => void loadFirst(appliedQuery)}
              className="mt-4 h-10 px-4"
            >
              {t("retry")}
            </Button>
          </div>
        ) : null}

        {!loading && !loadFailed && items.length > 0 ? (
          <ul className="space-y-3">
            {items.map((link) => (
              <LinkCard key={link.code} link={link} onEdit={setEditing} onDelete={setDeleting} />
            ))}
          </ul>
        ) : null}

        {empty && appliedQuery ? (
          <div className="rounded-2xl border border-border bg-card p-8 text-center shadow-sm">
            <Search aria-hidden="true" className="mx-auto size-9 text-muted-foreground" />
            <h2 className="mt-3 font-heading text-xl font-semibold">{t("noResultsTitle")}</h2>
            <p className="mt-1 text-sm text-muted-foreground">{t("noResultsBody")}</p>
            <Button
              type="button"
              variant="outline"
              onClick={clearSearch}
              className="mt-4 h-10 px-4"
            >
              {t("clearSearch")}
            </Button>
          </div>
        ) : null}

        {empty && !appliedQuery ? (
          <div className="rounded-2xl border border-dashed border-border bg-card p-8 text-center shadow-sm sm:p-12">
            <span className="mx-auto grid size-14 place-items-center rounded-2xl bg-tc-blue-100 text-tc-blue-700 dark:bg-tc-blue-600/20 dark:text-tc-blue-100">
              <Link2 aria-hidden="true" className="size-7" />
            </span>
            <h2 className="mt-4 font-heading text-2xl font-semibold">{t("emptyTitle")}</h2>
            <p className="mx-auto mt-1 max-w-sm text-sm text-muted-foreground">{t("emptyBody")}</p>
            <Link
              href="/#shorten"
              className="mt-5 inline-flex h-11 items-center justify-center rounded-xl bg-tc-red-600 px-5 text-sm font-semibold text-tc-white transition-colors hover:bg-tc-red-700 focus-visible:border-tc-red-700 focus-visible:ring-3 focus-visible:ring-tc-red-600/40"
            >
              {t("create")}
            </Link>
          </div>
        ) : null}

        {nextCursor && !loading && !loadFailed ? (
          <div className="mt-6 flex justify-center">
            <Button
              type="button"
              variant="outline"
              disabled={loadingMore}
              onClick={() => void loadMore()}
              className="h-10 px-5"
            >
              {loadingMore ? <Loader2 aria-hidden="true" className="size-4 animate-spin" /> : null}
              {loadingMore ? t("loadingMore") : t("loadMore")}
            </Button>
          </div>
        ) : null}
      </section>

      {editing ? (
        <EditLinkDialog
          key={editing.code}
          link={editing}
          onClose={() => setEditing(null)}
          onSave={handleSave}
        />
      ) : null}
      <DeleteLinkDialog
        code={deleting?.code ?? null}
        open={deleting !== null}
        deleting={deleteBusy}
        onClose={() => {
          if (!deleteBusy) {
            setDeleting(null);
          }
        }}
        onConfirm={() => void confirmDelete()}
      />
    </div>
  );
}
