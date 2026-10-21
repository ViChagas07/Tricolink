import "@testing-library/jest-dom/vitest";

import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

afterEach(() => {
  cleanup();
  window.localStorage.clear();
  document.documentElement.classList.remove("dark", "light");
});

if (typeof window.matchMedia !== "function") {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: (query: string) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: () => undefined,
      removeListener: () => undefined,
      addEventListener: () => undefined,
      removeEventListener: () => undefined,
      dispatchEvent: () => false,
    }),
  });
}

if (typeof window.HTMLDialogElement !== "undefined") {
  window.HTMLDialogElement.prototype.showModal ??= function showModal() {
    this.open = true;
  };
  window.HTMLDialogElement.prototype.close ??= function close() {
    this.open = false;
    this.dispatchEvent(new Event("close"));
  };
}
