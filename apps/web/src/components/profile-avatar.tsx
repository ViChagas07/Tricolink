"use client";

import { useState } from "react";

import { cn } from "@/lib/utils";

type ProfileAvatarProps = {
  displayName: string | null;
  email: string;
  avatarUrl: string | null;
  className?: string;
};

export function initialsFor(displayName: string | null, email: string): string {
  const source = displayName?.trim() || email;
  return source
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part.charAt(0).toUpperCase())
    .join("");
}

export function ProfileAvatar({
  displayName,
  email,
  avatarUrl,
  className,
}: ProfileAvatarProps) {
  const [failedUrl, setFailedUrl] = useState<string | null>(null);
  const failed = avatarUrl !== null && failedUrl === avatarUrl;

  return (
    <span
      className={cn(
        "inline-flex size-9 shrink-0 items-center justify-center overflow-hidden rounded-full bg-tc-blue-700 text-xs font-semibold text-tc-white",
        className,
      )}
    >
      {avatarUrl && !failed ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={avatarUrl}
          alt=""
          referrerPolicy="no-referrer"
          className="size-full object-cover"
          onError={() => setFailedUrl(avatarUrl)}
        />
      ) : (
        <span aria-hidden="true">{initialsFor(displayName, email)}</span>
      )}
    </span>
  );
}
