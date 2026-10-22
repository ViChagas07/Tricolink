import createMiddleware from "next-intl/middleware";
import { NextRequest } from "next/server";

import { routing } from "@/i18n/routing";
import { buildCspHeader, securityHeaders } from "@/lib/security";
import { isPrivatePath } from "@/lib/seo";

const intlMiddleware = createMiddleware(routing);
const SESSION_HINT_COOKIE = "tl_session_hint";
const REFRESH_COOKIES = ["tl_refresh", "__Secure-tl_refresh"];

function createNonce(): string {
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);

  let binary = "";
  for (const byte of bytes) {
    binary += String.fromCharCode(byte);
  }
  return btoa(binary);
}

export default function proxy(request: NextRequest) {
  const nonce = createNonce();
  const isDev = process.env.NODE_ENV !== "production";
  const csp = buildCspHeader({ nonce, isDev });

  const requestHeaders = new Headers(request.headers);
  requestHeaders.set("x-nonce", nonce);
  requestHeaders.set("x-pathname", request.nextUrl.pathname);
  requestHeaders.set("Content-Security-Policy", csp);

  const localizedRequest = new NextRequest(request.url, {
    method: request.method,
    headers: requestHeaders,
  });

  const response = intlMiddleware(localizedRequest);
  response.headers.set("Content-Security-Policy", csp);

  const hasSession = REFRESH_COOKIES.some((name) => request.cookies.has(name));
  response.cookies.set(SESSION_HINT_COOKIE, hasSession ? "1" : "", {
    path: "/",
    httpOnly: false,
    sameSite: "lax",
    secure: !isDev,
    maxAge: hasSession ? 60 * 60 * 24 * 30 : 0,
  });

  for (const [name, value] of Object.entries(securityHeaders({ isProduction: !isDev }))) {
    response.headers.set(name, value);
  }

  if (isPrivatePath(request.nextUrl.pathname)) {
    response.headers.set("X-Robots-Tag", "noindex, nofollow");
  }

  return response;
}

export const config = {
  matcher: ["/", "/(pt-BR|en|es|fr|de|it|ja|ko|zh-CN|ru|ar)/:path*"],
};
