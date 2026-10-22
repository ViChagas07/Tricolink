import Image from "next/image";

import { Link } from "@/i18n/navigation";

export function BrandLogo({ label }: { label: string }) {
  return (
    <Link
      href="/"
      aria-label={label}
      className="inline-flex shrink-0 items-center rounded-xl outline-offset-4"
    >
      <span className="inline-flex items-center justify-center rounded-xl dark:bg-white dark:p-1 dark:shadow-sm dark:ring-1 dark:ring-white/20">
        <Image
          src="/brand/tricolink-navbar.png"
          alt=""
          width={640}
          height={603}
          sizes="(min-width: 640px) 56px, 48px"
          loading="eager"
          className="h-12 w-auto sm:h-14"
        />
      </span>
    </Link>
  );
}
