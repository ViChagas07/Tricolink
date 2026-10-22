import { cn } from "@/lib/utils";

type LinksSkeletonProps = {
  rows?: number;
  className?: string;
};

export function LinksSkeleton({ rows = 4, className }: LinksSkeletonProps) {
  return (
    <div aria-hidden="true" className={cn("space-y-3", className)}>
      {Array.from({ length: rows }, (_, index) => (
        <div key={index} className="rounded-2xl border border-border bg-card p-4 shadow-sm sm:p-5">
          <div className="flex flex-col gap-3">
            <div className="flex flex-wrap items-center gap-3">
              <span className="h-4 w-24 animate-pulse rounded bg-muted" />
              <span className="h-3 w-40 animate-pulse rounded bg-muted" />
            </div>
            <span className="h-3.5 w-full max-w-xl animate-pulse rounded bg-muted" />
            <div className="flex items-center gap-4">
              <span className="h-3 w-20 animate-pulse rounded bg-muted" />
              <span className="h-3 w-28 animate-pulse rounded bg-muted" />
            </div>
            <div className="flex items-center gap-2">
              <span className="size-9 animate-pulse rounded-lg bg-muted" />
              <span className="size-9 animate-pulse rounded-lg bg-muted" />
              <span className="size-9 animate-pulse rounded-lg bg-muted" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
