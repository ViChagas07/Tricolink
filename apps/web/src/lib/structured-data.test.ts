import { describe, expect, it } from "vitest";

import enMessages from "../../messages/en.json";
import { buildLandingStructuredData, type FaqItem } from "./structured-data";

const faq: FaqItem[] = Array.from({ length: 8 }, (_, index) => ({
  question: enMessages.faq[`q${index + 1}` as keyof typeof enMessages.faq],
  answer: enMessages.faq[`a${index + 1}` as keyof typeof enMessages.faq],
}));

function landingData() {
  return buildLandingStructuredData({
    name: "Tricolink",
    description: enMessages.meta.homeDescription,
    url: "https://tricolink.example/en",
    locale: "en",
    faq,
    features: [
      enMessages.features.shortTitle,
      enMessages.features.statsTitle,
      enMessages.features.controlTitle,
    ],
  });
}

describe("buildLandingStructuredData", () => {
  it("produces JSON that round-trips and declares both schema types", () => {
    const data = landingData();
    expect(JSON.parse(JSON.stringify(data))).toEqual(data);

    const graph = data["@graph"] as Array<Record<string, unknown>>;
    expect(data["@context"]).toBe("https://schema.org");
    expect(graph.map((node) => node["@type"])).toEqual(["WebApplication", "FAQPage"]);
  });

  it("describes the free web application", () => {
    const graph = landingData()["@graph"] as Array<Record<string, unknown>>;
    const webApp = graph[0];

    expect(webApp.name).toBe("Tricolink");
    expect(webApp.url).toBe("https://tricolink.example/en");
    expect(webApp.applicationCategory).toBe("UtilitiesApplication");
    expect(webApp.isAccessibleForFree).toBe(true);
    expect(webApp.inLanguage).toBe("en");
    expect(webApp.offers).toEqual(
      expect.objectContaining({ "@type": "Offer", price: "0", priceCurrency: "USD" }),
    );
    expect(webApp.featureList).toHaveLength(3);
  });

  it("uses the same eight FAQ entries as the page", () => {
    const graph = landingData()["@graph"] as Array<Record<string, unknown>>;
    const faqPage = graph[1];
    const entities = faqPage.mainEntity as Array<Record<string, unknown>>;

    expect(faqPage["@type"]).toBe("FAQPage");
    expect(entities).toHaveLength(8);

    entities.forEach((entity, index) => {
      expect(entity["@type"]).toBe("Question");
      expect(entity.name).toBe(faq[index].question);
      expect(entity.acceptedAnswer).toEqual({
        "@type": "Answer",
        text: faq[index].answer,
      });
      expect(String(entity.name).length).toBeGreaterThan(0);
      expect(String((entity.acceptedAnswer as Record<string, string>).text).length).toBeGreaterThan(
        0,
      );
    });
  });
});
