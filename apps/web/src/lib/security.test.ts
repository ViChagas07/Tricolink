import { describe, expect, it } from "vitest";

import { buildCspHeader, securityHeaders } from "./security";

describe("buildCspHeader", () => {
  it("locks down the production policy and includes the nonce", () => {
    const csp = buildCspHeader({ nonce: "abc123", isDev: false });

    expect(csp).toContain("default-src 'self'");
    expect(csp).toContain("script-src 'self' 'nonce-abc123' 'strict-dynamic'");
    expect(csp).toContain("style-src 'self' 'nonce-abc123'");
    expect(csp).toContain("img-src 'self' data:");
    expect(csp).toContain("connect-src 'self'");
    expect(csp).toContain("frame-ancestors 'none'");
    expect(csp).toContain("base-uri 'none'");
    expect(csp).toContain("form-action 'self'");
    expect(csp).toContain("object-src 'none'");
    expect(csp).not.toContain("'unsafe-eval'");
  });

  it("allows the React debugger only in development", () => {
    expect(buildCspHeader({ nonce: "dev", isDev: true })).toContain("'unsafe-eval'");
  });
});

describe("securityHeaders", () => {
  it("sets the required headers without HSTS outside production", () => {
    const headers = securityHeaders({ isProduction: false });

    expect(headers["X-Content-Type-Options"]).toBe("nosniff");
    expect(headers["Referrer-Policy"]).toBe("strict-origin-when-cross-origin");
    expect(headers["Cross-Origin-Opener-Policy"]).toBe("same-origin");
    expect(headers["X-Frame-Options"]).toBe("DENY");
    expect(headers["Permissions-Policy"]).toContain("camera=()");
    expect(headers["Strict-Transport-Security"]).toBeUndefined();
  });

  it("adds HSTS in production", () => {
    expect(securityHeaders({ isProduction: true })["Strict-Transport-Security"]).toBe(
      "max-age=63072000; includeSubDomains; preload",
    );
  });
});
