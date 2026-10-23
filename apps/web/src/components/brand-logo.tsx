import Image from "next/image";

import { Link } from "@/i18n/navigation";

export function BrandLogo({ label }: { label: string }) {
  return (
    <Link
      href="/"
      aria-label={label}
      className="inline-flex shrink-0 items-center rounded-xl outline-offset-4"
    >
      <Image
        src="/brand/tricolink-transparente-removebg.png"
        alt=""
        width={500}
        height={500}
        sizes="(min-width: 640px) 56px, 48px"
        loading="eager"
        className="tc-brand-logo h-12 w-auto sm:h-14"
      />
    </Link>
  );
}
