const CONTROL_OR_SPACE = /[\u0000-\u0020\u007f]/;
const SCHEME = /^[a-zA-Z][a-zA-Z0-9+.-]*:/;

export function safeExternalHref(value: string): string | null {
  if (!value || CONTROL_OR_SPACE.test(value) || !SCHEME.test(value)) {
    return null;
  }

  let url: URL;
  try {
    url = new URL(value);
  } catch {
    return null;
  }

  if (url.protocol !== "http:" && url.protocol !== "https:") {
    return null;
  }
  if (url.username || url.password || !url.hostname) {
    return null;
  }

  return url.toString();
}
