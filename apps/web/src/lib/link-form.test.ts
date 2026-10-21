import { describe, expect, it } from "vitest";

import { normalizeShortenUrl, validateShortenUrl } from "./link-form";

describe("validateShortenUrl", () => {
  it("requires a value", () => {
    expect(validateShortenUrl("")).toBe("required");
    expect(validateShortenUrl("   ")).toBe("required");
  });

  it("accepts http and https URLs", () => {
    expect(validateShortenUrl("https://example.com/path?q=1")).toBeNull();
    expect(validateShortenUrl("http://example.com")).toBeNull();
    expect(validateShortenUrl("HTTPS://EXAMPLE.COM")).toBeNull();
    expect(validateShortenUrl("https://例子.测试/路径")).toBeNull();
  });

  it("rejects unsafe or malformed URLs", () => {
    for (const value of [
      "not a url",
      "example.com",
      "//evil.example",
      "/relative",
      "javascript:alert(1)",
      "data:text/html,<script>alert(1)</script>",
      "ftp://example.com/file",
      "https://user:pass@example.com",
      "https://exam\nple.com",
    ]) {
      expect(validateShortenUrl(value)).toBe("invalid");
    }
  });

  it("rejects URLs longer than 2048 characters", () => {
    const tooLong = `https://example.com/${"a".repeat(2048)}`;
    expect(validateShortenUrl(tooLong)).toBe("too_long");
  });

  it("normalizes whitespace and internationalized hosts", () => {
    expect(normalizeShortenUrl("  https://example.com/a  ")).toBe("https://example.com/a");
    expect(normalizeShortenUrl("https://例子.测试/路径")).toBe(
      "https://xn--fsqu00a.xn--0zwm56d/%E8%B7%AF%E5%BE%84",
    );
  });
});
