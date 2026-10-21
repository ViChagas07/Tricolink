export type BreakdownRow = {
  id: string;
  label: string;
  clicks: number;
  share: number;
};

export type BreakdownColumns = {
  label: string;
  clicks: string;
  share: string;
};

type BreakdownTableProps = {
  locale: string;
  title: string;
  caption?: string;
  columns: BreakdownColumns;
  items: readonly BreakdownRow[];
  emptyLabel: string;
};

export function BreakdownTable({
  locale,
  title,
  caption,
  columns,
  items,
  emptyLabel,
}: BreakdownTableProps) {
  const numberFormat = new Intl.NumberFormat(locale);
  const percentFormat = new Intl.NumberFormat(locale, {
    style: "percent",
    maximumFractionDigits: 1,
  });

  return (
    <section className="rounded-2xl border border-border bg-card p-4 shadow-sm sm:p-5">
      <h3 className="font-heading text-sm font-semibold text-card-foreground">{title}</h3>

      {items.length === 0 ? (
        <p className="mt-4 text-sm text-muted-foreground">{emptyLabel}</p>
      ) : (
        <div className="mt-3 overflow-x-auto">
          <table className="w-full min-w-[16rem] text-sm">
            <caption className="sr-only">{caption ?? title}</caption>
            <thead>
              <tr className="border-b border-border text-xs uppercase tracking-wide text-muted-foreground">
                <th scope="col" className="py-2 pe-3 text-start font-medium">
                  {columns.label}
                </th>
                <th scope="col" className="py-2 pe-3 text-end font-medium">
                  {columns.clicks}
                </th>
                <th scope="col" className="py-2 text-end font-medium">
                  {columns.share}
                </th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id} className="border-b border-border/60 last:border-0">
                  <th scope="row" className="py-2.5 pe-3 text-start font-medium">
                    <span className="block max-w-44 truncate">{item.label}</span>
                  </th>
                  <td className="py-2.5 pe-3 text-end tabular-nums text-muted-foreground">
                    {numberFormat.format(item.clicks)}
                  </td>
                  <td className="py-2.5 text-end tabular-nums text-muted-foreground">
                    <span className="inline-flex items-center justify-end gap-2">
                      <span
                        aria-hidden="true"
                        className="hidden h-1.5 w-14 overflow-hidden rounded-full bg-muted sm:inline-block"
                      >
                        <span
                          className="block h-full rounded-full bg-tc-blue-600"
                          style={{ width: `${Math.max(4, item.share * 100)}%` }}
                        />
                      </span>
                      {percentFormat.format(item.share)}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
