const MAX_URL_LENGTH = 2048;
const CONTROL_OR_SPACE = /[\u0000-\u0020\u007f]/;

export type ShortenUrlError = "required" | "invalid" | "too_long";

export function validateShortenUrl(value: string): ShortenUrlError | null {
  const trimmed = value.trim();
  if (!trimmed) {
    return "required";
  }
  if (trimmed.length > MAX_URL_LENGTH) {
    return "too_long";
  }
  if (CONTROL_OR_SPACE.test(trimmed)) {
    return "invalid";
  }

  let parsed: URL;
  try {
    parsed = new URL(trimmed);
  } catch {
    return "invalid";
  }

  if (parsed.protocol !== "http:" && parsed.protocol !== "https:") {
    return "invalid";
  }
  if (!parsed.hostname || parsed.username || parsed.password) {
    return "invalid";
  }
  if (parsed.href.length > MAX_URL_LENGTH) {
    return "too_long";
  }

  return null;
}

export function normalizeShortenUrl(value: string): string {
  return new URL(value.trim()).toString();
}
