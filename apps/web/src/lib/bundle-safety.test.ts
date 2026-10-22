import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative } from "node:path";

import { describe, expect, it } from "vitest";

const ROOT = join(process.cwd(), "src");
const FORBIDDEN = [
  /dangerouslySetInnerHTML/,
  /\bnew Function\s*\(/,
  /\beval\s*\(/,
];
const SECRET_PUBLIC_NAMES = /NEXT_PUBLIC_[A-Z0-9_]*(SECRET|TOKEN|PASSWORD|PRIVATE|DATABASE|REDIS)/;

function sourceFiles(directory: string): string[] {
  const files: string[] = [];
  for (const entry of readdirSync(directory)) {
    const path = join(directory, entry);
    const info = statSync(path);
    if (info.isDirectory()) {
      files.push(...sourceFiles(path));
      continue;
    }
    if (!/\.(ts|tsx)$/.test(entry)) {
      continue;
    }
    if (/\.test\.(ts|tsx)$/.test(entry)) {
      continue;
    }
    files.push(path);
  }
  return files;
}

describe("client source safety", () => {
  it("does not contain raw HTML injection or dynamic code execution", () => {
    const offenders = sourceFiles(ROOT).flatMap((path) => {
      const source = readFileSync(path, "utf8");
      return FORBIDDEN.filter((pattern) => pattern.test(source)).map(
        (pattern) => `${relative(process.cwd(), path)}: ${pattern}`,
      );
    });

    expect(offenders).toEqual([]);
  });

  it("does not expose secret-like values through NEXT_PUBLIC_*", () => {
    const offenders = sourceFiles(ROOT).filter((path) =>
      SECRET_PUBLIC_NAMES.test(readFileSync(path, "utf8")),
    );

    expect(offenders.map((path) => relative(process.cwd(), path))).toEqual([]);
  });

  it("keeps tokens out of the API client and auth store", () => {
    for (const file of ["lib/api.ts", "stores/auth-store.ts"]) {
      const source = readFileSync(join(ROOT, file), "utf8");
      expect(source).not.toMatch(/localStorage|sessionStorage/);
    }
  });
});
