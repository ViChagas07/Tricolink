export type FaqItem = {
  question: string;
  answer: string;
};

export type LandingStructuredDataInput = {
  name: string;
  description: string;
  url: string;
  locale: string;
  faq: readonly FaqItem[];
  features?: readonly string[];
};

type WebApplicationNode = {
  "@type": "WebApplication";
  "@id": string;
  name: string;
  url: string;
  description: string;
  applicationCategory: string;
  operatingSystem: string;
  browserRequirements: string;
  isAccessibleForFree: boolean;
  inLanguage: string;
  offers: {
    "@type": "Offer";
    price: string;
    priceCurrency: string;
  };
  featureList?: string[];
};

type FaqPageNode = {
  "@type": "FAQPage";
  "@id": string;
  mainEntity: Array<{
    "@type": "Question";
    name: string;
    acceptedAnswer: {
      "@type": "Answer";
      text: string;
    };
  }>;
};

export type LandingStructuredData = {
  "@context": "https://schema.org";
  "@graph": [WebApplicationNode, FaqPageNode];
};

export function buildLandingStructuredData({
  name,
  description,
  url,
  locale,
  faq,
  features,
}: LandingStructuredDataInput): LandingStructuredData {
  const app: WebApplicationNode = {
    "@type": "WebApplication",
    "@id": `${url}#webapp`,
    name,
    url,
    description,
    applicationCategory: "UtilitiesApplication",
    operatingSystem: "Any",
    browserRequirements: "Requires JavaScript",
    isAccessibleForFree: true,
    inLanguage: locale,
    offers: {
      "@type": "Offer",
      price: "0",
      priceCurrency: "USD",
    },
  };

  if (features && features.length > 0) {
    app.featureList = [...features];
  }

  return {
    "@context": "https://schema.org",
    "@graph": [
      app,
      {
        "@type": "FAQPage",
        "@id": `${url}#faq`,
        mainEntity: faq.map((item) => ({
          "@type": "Question",
          name: item.question,
          acceptedAnswer: {
            "@type": "Answer",
            text: item.answer,
          },
        })),
      },
    ],
  };
}

export function serializeStructuredData(data: LandingStructuredData): string {
  return JSON.stringify(data).replace(/</g, "\\u003c");
}
