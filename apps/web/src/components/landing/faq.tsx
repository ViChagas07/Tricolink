import { ChevronDown } from "lucide-react";

export type FaqEntry = {
  question: string;
  answer: string;
};

type FaqProps = {
  title: string;
  subtitle: string;
  items: readonly FaqEntry[];
};

export function Faq({ title, subtitle, items }: FaqProps) {
  return (
    <section
      id="faq"
      className="tc-defer-render mx-auto w-full max-w-3xl scroll-mt-24 px-4 py-16 sm:px-6 sm:py-24"
    >
      <div className="text-center">
        <h2 className="text-balance font-heading text-3xl font-bold tracking-tight text-tc-blue-950 sm:text-4xl dark:text-tc-white">
          {title}
        </h2>
        <p className="mx-auto mt-3 max-w-xl text-pretty text-sm leading-relaxed text-muted-foreground sm:text-base">
          {subtitle}
        </p>
      </div>

      <div className="mt-10 space-y-3">
        {items.map((item, index) => (
          <details
            key={item.question}
            name="tricolink-faq"
            open={index === 0}
            className="group rounded-xl border border-border bg-card shadow-sm transition-shadow open:shadow-md"
          >
            <summary className="flex cursor-pointer list-none items-center justify-between gap-4 px-5 py-4 font-heading text-sm font-semibold text-card-foreground marker:content-none sm:text-base [&::-webkit-details-marker]:hidden">
              <span>{item.question}</span>
              <ChevronDown
                aria-hidden="true"
                className="size-5 shrink-0 text-muted-foreground transition-transform duration-200 group-open:rotate-180"
              />
            </summary>
            <div className="px-5 pb-5 text-sm leading-relaxed text-muted-foreground">
              <p className="text-pretty">{item.answer}</p>
            </div>
          </details>
        ))}
      </div>
    </section>
  );
}
