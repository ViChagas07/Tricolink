const API_BASE = "/api/v1";
const CSRF_HEADER = "x-csrf-token";
const CSRF_COOKIES = ["__Host-tl_csrf", "__Secure-tl_csrf", "tl_csrf"];
const SESSION_HINT_COOKIE = "tl_session_hint";
const SAFE_METHODS = new Set(["GET", "HEAD", "OPTIONS"]);
const NO_REFRESH_PATHS = [
  "/auth/csrf",
  "/auth/login",
  "/auth/register",
  "/auth/refresh",
  "/auth/logout",
];

export type ApiErrorPayload = {
  error: {
    code: string;
    message: string;
    details?: unknown;
  };
};

export type UserDto = {
  id: string;
  email: string;
  display_name: string | null;
  locale: string | null;
  is_active: boolean;
  created_at: string;
};

export type AuthResponseDto = {
  user: UserDto;
};

export type RegisterResponseDto = {
  status: "registered";
};

export type ApiRequestOptions = Omit<RequestInit, "body" | "credentials" | "method"> & {
  method?: string;
  body?: unknown;
  skipAuthRefresh?: boolean;
  csrf?: "auto" | "skip";
};

export class ApiError extends Error {
  readonly status: number;
  readonly code: string;
  readonly details?: unknown;
  readonly retryAfter?: number;

  constructor(options: {
    message: string;
    status: number;
    code: string;
    details?: unknown;
    retryAfter?: number;
  }) {
    super(options.message);
    this.name = "ApiError";
    this.status = options.status;
    this.code = options.code;
    this.details = options.details;
    this.retryAfter = options.retryAfter;
  }
}

export function isApiError(error: unknown): error is ApiError {
  return error instanceof ApiError;
}

export function parseRetryAfter(
  value: string | null | undefined,
  now = Date.now(),
): number | undefined {
  if (!value) {
    return undefined;
  }

  const trimmed = value.trim();
  if (/^\d+$/.test(trimmed)) {
    return Number.parseInt(trimmed, 10);
  }

  const date = Date.parse(trimmed);
  if (Number.isNaN(date)) {
    return undefined;
  }

  return Math.max(0, Math.ceil((date - now) / 1000));
}

let csrfCache: string | null = null;
let refreshInFlight: Promise<boolean> | null = null;

function readCookie(name: string): string | null {
  if (typeof document === "undefined") {
    return null;
  }

  const prefix = `${name}=`;
  for (const part of document.cookie.split(";")) {
    const entry = part.trim();
    if (entry.startsWith(prefix)) {
      const value = entry.slice(prefix.length);
      try {
        return decodeURIComponent(value);
      } catch {
        return value;
      }
    }
  }
  return null;
}

async function apiErrorFromResponse(response: Response): Promise<ApiError> {
  const retryAfter = parseRetryAfter(response.headers.get("retry-after"));
  let code = "request_failed";
  let message = response.statusText || "Request failed";
  let details: unknown;

  if (response.headers.get("content-type")?.includes("application/json")) {
    try {
      const payload = (await response.json()) as Partial<ApiErrorPayload>;
      const error = payload.error;
      if (error && typeof error.code === "string" && typeof error.message === "string") {
        code = error.code;
        message = error.message;
        details = error.details;
      }
    } catch {
      // Keep the fallback message when the body is not valid JSON.
    }
  }

  return new ApiError({ message, status: response.status, code, details, retryAfter });
}

async function fetchCsrfToken(): Promise<string> {
  const response = await fetch(`${API_BASE}/auth/csrf`, {
    credentials: "include",
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw await apiErrorFromResponse(response);
  }

  const payload = (await response.json()) as { csrf_token?: unknown };
  if (typeof payload.csrf_token !== "string" || payload.csrf_token.length === 0) {
    throw new ApiError({
      message: "The server did not return a CSRF token",
      status: response.status,
      code: "invalid_csrf_response",
    });
  }

  return payload.csrf_token;
}

export async function ensureCsrfToken(force = false): Promise<string> {
  if (!force) {
    for (const name of CSRF_COOKIES) {
      const cookie = readCookie(name);
      if (cookie) {
        csrfCache = cookie;
        return cookie;
      }
    }
    if (csrfCache) {
      return csrfCache;
    }
  }

  csrfCache = await fetchCsrfToken();
  return csrfCache;
}

async function perform<T>(
  path: string,
  options: ApiRequestOptions,
  csrfToken?: string,
): Promise<T> {
  const { body, skipAuthRefresh, csrf, ...init } = options;
  void skipAuthRefresh;
  void csrf;
  const method = (init.method ?? "GET").toUpperCase();
  const headers = new Headers(init.headers);
  headers.set("Accept", "application/json");

  if (body !== undefined) {
    headers.set("Content-Type", "application/json");
  }
  if (!SAFE_METHODS.has(method) && csrfToken) {
    headers.set(CSRF_HEADER, csrfToken);
  }

  const response = await fetch(`${API_BASE}${path.startsWith("/") ? path : `/${path}`}`, {
    ...init,
    method,
    headers,
    credentials: "include",
    body: body === undefined ? undefined : JSON.stringify(body),
  });

  if (!response.ok) {
    throw await apiErrorFromResponse(response);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  if (response.headers.get("content-type")?.includes("application/json")) {
    return (await response.json()) as T;
  }

  return (await response.text()) as T;
}

function shouldAttemptRefresh(path: string): boolean {
  return !NO_REFRESH_PATHS.some(
    (candidate) => path === candidate || path.startsWith(`${candidate}?`),
  );
}

function hasSessionHint(): boolean {
  return readCookie(SESSION_HINT_COOKIE) === "1";
}

async function refreshSession(): Promise<boolean> {
  if (!hasSessionHint()) {
    return false;
  }

  if (!refreshInFlight) {
    refreshInFlight = (async () => {
      try {
        const csrfToken = await ensureCsrfToken();
        const response = await fetch(`${API_BASE}/auth/refresh`, {
          method: "POST",
          credentials: "include",
          headers: {
            Accept: "application/json",
            [CSRF_HEADER]: csrfToken,
          },
        });
        return response.ok;
      } catch {
        return false;
      }
    })().finally(() => {
      refreshInFlight = null;
    });
  }

  return refreshInFlight;
}

export async function request<T>(path: string, options: ApiRequestOptions = {}): Promise<T> {
  const method = (options.method ?? "GET").toUpperCase();
  const mutation = !SAFE_METHODS.has(method);

  try {
    const csrfToken = mutation && options.csrf !== "skip" ? await ensureCsrfToken() : undefined;
    return await perform<T>(path, options, csrfToken);
  } catch (error) {
    if (
      isApiError(error) &&
      error.status === 401 &&
      !options.skipAuthRefresh &&
      shouldAttemptRefresh(path)
    ) {
      const refreshed = await refreshSession();
      if (refreshed) {
        const csrfToken = mutation && options.csrf !== "skip" ? await ensureCsrfToken() : undefined;
        return perform<T>(path, options, csrfToken);
      }
    }

    if (isApiError(error)) {
      throw error;
    }

    throw new ApiError({
      message: error instanceof Error ? error.message : "Network request failed",
      status: 0,
      code: "network_error",
    });
  }
}

export const api = {
  request,
  get<T>(path: string, options: Omit<ApiRequestOptions, "method" | "body"> = {}) {
    return request<T>(path, { ...options, method: "GET" });
  },
  post<T>(path: string, body?: unknown, options: Omit<ApiRequestOptions, "method" | "body"> = {}) {
    return request<T>(path, { ...options, method: "POST", body });
  },
  patch<T>(path: string, body?: unknown, options: Omit<ApiRequestOptions, "method" | "body"> = {}) {
    return request<T>(path, { ...options, method: "PATCH", body });
  },
  delete<T>(path: string, options: Omit<ApiRequestOptions, "method" | "body"> = {}) {
    return request<T>(path, { ...options, method: "DELETE" });
  },
  getMe() {
    return request<UserDto>("/auth/me");
  },
  register(body: { email: string; password: string }) {
    return request<RegisterResponseDto>("/auth/register", {
      method: "POST",
      body,
      skipAuthRefresh: true,
      csrf: "skip",
    });
  },
  login(body: { email: string; password: string }) {
    return request<AuthResponseDto>("/auth/login", {
      method: "POST",
      body,
      skipAuthRefresh: true,
      csrf: "skip",
    });
  },
  updateMe(body: { display_name?: string | null; locale?: string | null }) {
    return request<UserDto>("/auth/me", { method: "PATCH", body });
  },
  logout() {
    return request<void>("/auth/logout", { method: "POST", skipAuthRefresh: true });
  },
  refresh() {
    return request<AuthResponseDto>("/auth/refresh", {
      method: "POST",
      skipAuthRefresh: true,
    });
  },
};

export function resetApiClientForTests(): void {
  csrfCache = null;
  refreshInFlight = null;
}
