import type { AnchorHTMLAttributes, ReactNode } from "react";

import { safeExternalHref } from "@/lib/url";

type ExternalLinkProps = Omit<
  AnchorHTMLAttributes<HTMLAnchorElement>,
  "href" | "target" | "rel"
> & {
  href: string;
  children: ReactNode;
};

export function ExternalLink({ href, children, ...props }: ExternalLinkProps) {
  const safeHref = safeExternalHref(href);

  if (!safeHref) {
    return <span>{children}</span>;
  }

  return (
    <a href={safeHref} target="_blank" rel="noopener noreferrer nofollow ugc" {...props}>
      {children}
    </a>
  );
}
