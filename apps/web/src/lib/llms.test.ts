import { describe, expect, it } from "vitest";

import { buildLlmsTxt } from "./llms";

describe("buildLlmsTxt", () => {
  const text = buildLlmsTxt("https://tricolink.example");

  it("describes the product and lists public routes", () => {
    expect(text).toContain("# Tricolink");
    expect(text).toContain("free URL shortener");
    expect(text).toContain("https://tricolink.example/en");
    expect(text).toContain("https://tricolink.example/pt-BR");
    expect(text).toContain("https://tricolink.example/sitemap.xml");
    expect(text).toContain("HTTP 302");
  });

  it("states the data policy honestly", () => {
    expect(text).toContain("IP addresses are not stored");
    expect(text).toContain("No advertising");
    expect(text).toContain("http and https");
    expect(text).toContain("noindex");
  });
});
