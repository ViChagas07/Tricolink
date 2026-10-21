import { describe, expect, it } from "vitest";

import { safeExternalHref } from "./url";

describe("safeExternalHref", () => {
  it("accepts http and https URLs", () => {
    expect(safeExternalHref("https://example.com/path?q=1")).toBe("https://example.com/path?q=1");
    expect(safeExternalHref("http://example.com")).toBe("http://example.com/");
  });

  it("rejects dangerous or malformed targets", () => {
    for (const value of [
      "javascript:alert(1)",
      "data:text/html,<script>alert(1)</script>",
      "//evil.example",
      "/relative",
      "https://user:pass@example.com",
      "https://exa mple.com",
      "ftp://example.com/file",
      "",
    ]) {
      expect(safeExternalHref(value)).toBeNull();
    }
  });
});
