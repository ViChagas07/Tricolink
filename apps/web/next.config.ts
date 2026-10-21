import type { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";

import { buildRewrites } from "./src/lib/rewrites";
import { securityHeaders } from "./src/lib/security";

const withNextIntl = createNextIntlPlugin("./src/i18n/request.ts");

const apiInternalUrl = process.env.API_INTERNAL_URL ?? "http://localhost:8000";
const isProduction = process.env.NODE_ENV === "production";

const nextConfig: NextConfig = {
  output: "standalone",
  reactStrictMode: true,
  poweredByHeader: false,
  async rewrites() {
    return buildRewrites(apiInternalUrl);
  },
  async headers() {
    return [
      {
        source: "/:path*",
        headers: Object.entries(securityHeaders({ isProduction })).map(([key, value]) => ({
          key,
          value,
        })),
      },
    ];
  },
};

export default withNextIntl(nextConfig);
