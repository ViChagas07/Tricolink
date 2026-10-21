import { readdirSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const appRoot = resolve(scriptDir, "..");
const messagesDir = join(appRoot, "messages");

const { locales } = await import(pathToFileURL(join(appRoot, "src/i18n/locales.ts")).href);
const referenceLocale = "en";

function flattenKeys(value, prefix = "") {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    return [{ key: prefix, value }];
  }

  return Object.entries(value).flatMap(([key, child]) =>
    flattenKeys(child, prefix ? `${prefix}.${key}` : key),
  );
}

function placeholders(value) {
  if (typeof value !== "string") {
    return [];
  }
  return [...value.matchAll(/\{([a-zA-Z][a-zA-Z0-9_]*)/g)].map((match) => match[1]).sort();
}

const localeSet = new Set(locales);
const errors = [];
const catalogs = new Map();

const files = readdirSync(messagesDir).filter((file) => file.endsWith(".json"));
for (const file of files) {
  const locale = file.slice(0, -".json".length);
  if (!localeSet.has(locale)) {
    errors.push(`unexpected message file: messages/${file}`);
  }
}

for (const locale of locales) {
  const file = join(messagesDir, `${locale}.json`);
  let catalog;
  try {
    catalog = JSON.parse(readFileSync(file, "utf8"));
  } catch (error) {
    errors.push(`cannot read messages/${locale}.json: ${error.message}`);
    continue;
  }
  catalogs.set(locale, catalog);
}

const reference = catalogs.get(referenceLocale);
if (!reference) {
  errors.push(`missing reference catalog messages/${referenceLocale}.json`);
}

if (reference) {
  const referenceEntries = new Map(flattenKeys(reference).map((entry) => [entry.key, entry.value]));
  const referenceKeys = new Set(referenceEntries.keys());

  for (const [locale, catalog] of catalogs) {
    const entries = new Map(flattenKeys(catalog).map((entry) => [entry.key, entry.value]));

    for (const key of referenceKeys) {
      if (!entries.has(key)) {
        errors.push(`${locale}: missing key "${key}"`);
      }
    }

    for (const key of entries.keys()) {
      if (!referenceKeys.has(key)) {
        errors.push(`${locale}: extra key "${key}"`);
      }
    }

    for (const [key, value] of entries) {
      if (typeof value === "string" && value.trim() === "") {
        errors.push(`${locale}: empty value for "${key}"`);
        continue;
      }
      const expected = placeholders(referenceEntries.get(key));
      const actual = placeholders(value);
      if (expected.join(",") !== actual.join(",")) {
        errors.push(
          `${locale}: placeholders for "${key}" are {${actual.join(", ")}} but expected {${expected.join(", ")}}`,
        );
      }
    }
  }
}

if (errors.length > 0) {
  for (const error of errors) {
    console.error(`i18n:check: ${error}`);
  }
  process.exitCode = 1;
} else {
  const keyCount = reference ? flattenKeys(reference).length : 0;
  console.log(`i18n:check ok — ${locales.length} locales, ${keyCount} keys`);
}
