import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { NextIntlClientProvider } from "next-intl";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import enMessages from "../../../messages/en.json";
import { BackToTop } from "./back-to-top";

const observers: MockIntersectionObserver[] = [];

class MockIntersectionObserver {
  readonly root = null;
  readonly rootMargin = "";
  readonly thresholds = [];
  observe = vi.fn();
  unobserve = vi.fn();
  disconnect = vi.fn();
  takeRecords = vi.fn(() => []);

  constructor(readonly callback: IntersectionObserverCallback) {
    observers.push(this);
  }
}

function notify(instance: MockIntersectionObserver, top: number, isIntersecting = false) {
  act(() => {
    instance.callback(
      [{ isIntersecting, boundingClientRect: { top } } as IntersectionObserverEntry],
      instance as unknown as IntersectionObserver,
    );
  });
}

function renderBackToTop() {
  return render(
    <NextIntlClientProvider locale="en" messages={enMessages} timeZone="UTC">
      <span id="demo-title">Your links in one place</span>
      <BackToTop />
    </NextIntlClientProvider>,
  );
}

describe("BackToTop", () => {
  beforeEach(() => {
    observers.length = 0;
    vi.stubGlobal("IntersectionObserver", MockIntersectionObserver);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("stays hidden until the hero title scrolls out of view", () => {
    renderBackToTop();

    expect(screen.queryByRole("button", { name: "Back to top" })).not.toBeInTheDocument();

    notify(observers[0], -200);
    expect(screen.getByRole("button", { name: "Back to top" })).toBeInTheDocument();

    notify(observers[0], 120, true);
    expect(screen.queryByRole("button", { name: "Back to top" })).not.toBeInTheDocument();
  });

  it("scrolls to the top when clicked", async () => {
    const scrollTo = vi.fn();
    vi.stubGlobal("scrollTo", scrollTo);
    renderBackToTop();

    notify(observers[0], -200);
    await userEvent.setup().click(screen.getByRole("button", { name: "Back to top" }));

    expect(scrollTo).toHaveBeenCalledWith({ top: 0, behavior: "smooth" });
  });
});
