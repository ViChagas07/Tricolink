import { buildLlmsTxt } from "@/lib/llms";
import { siteUrl } from "@/lib/seo";

export const dynamic = "force-static";

export function GET() {
  return new Response(buildLlmsTxt(siteUrl), {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "public, max-age=3600, s-maxage=86400",
    },
  });
}
