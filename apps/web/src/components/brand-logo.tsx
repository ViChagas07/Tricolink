import { Link2 } from "lucide-react";

import { Link } from "@/i18n/navigation";

export function BrandLogo({ label }: { label: string }) {
  return (
    <Link
      href="/"
      aria-label={label}
      className="inline-flex items-center gap-2 rounded-xl outline-offset-4"
    >
      <span
        aria-hidden="true"
        className="relative grid size-9 shrink-0 place-items-center overflow-hidden rounded-xl bg-tc-blue-700 text-tc-white shadow-sm"
      >
        <span className="tc-tricolor-bar absolute inset-x-0 top-0 h-1" />
        <Link2 className="size-4" />
      </span>
      <span className="font-heading text-lg font-bold tracking-tight text-tc-blue-950 dark:text-tc-white">
        Trico<span className="text-tc-red-600 dark:text-tc-red-400">link</span>
      </span>
    </Link>
  );
}
