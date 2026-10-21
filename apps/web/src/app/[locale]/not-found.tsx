import { getTranslations } from "next-intl/server";

import { buttonVariants } from "@/components/ui/button";
import { Link } from "@/i18n/navigation";
import { cn } from "@/lib/utils";

export default async function LocaleNotFound() {
  const errors = await getTranslations("errors");
  const auth = await getTranslations("auth");

  return (
    <section className="mx-auto flex w-full max-w-xl flex-col items-center px-4 py-24 text-center sm:px-6">
      <p className="font-heading text-6xl font-bold text-tc-blue-700 dark:text-tc-blue-100">404</p>
      <h1 className="mt-4 text-2xl font-semibold text-foreground">{errors("notFound")}</h1>
      <Link href="/" className={cn(buttonVariants({ variant: "default", size: "lg" }), "mt-8")}>
        {auth("backHome")}
      </Link>
    </section>
  );
}
