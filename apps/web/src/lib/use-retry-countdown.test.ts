import { act, renderHook } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { useRetryCountdown } from "./use-retry-countdown";

describe("useRetryCountdown", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2026-10-21T12:00:00Z"));
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("returns zero without a deadline", () => {
    const { result } = renderHook(() => useRetryCountdown(null));
    expect(result.current).toBe(0);
  });

  it("counts down once per second until the deadline", async () => {
    const retryAt = Date.now() + 3000;
    const { result } = renderHook(() => useRetryCountdown(retryAt));
    await act(async () => {});

    expect(result.current).toBe(3);

    act(() => {
      vi.advanceTimersByTime(1000);
    });
    expect(result.current).toBe(2);

    act(() => {
      vi.advanceTimersByTime(1000);
    });
    expect(result.current).toBe(1);

    act(() => {
      vi.advanceTimersByTime(1000);
    });
    expect(result.current).toBe(0);

    act(() => {
      vi.advanceTimersByTime(5000);
    });
    expect(result.current).toBe(0);
  });

  it("restarts when a new deadline is provided", async () => {
    const { result, rerender } = renderHook(
      ({ deadline }: { deadline: number | null }) => useRetryCountdown(deadline),
      { initialProps: { deadline: Date.now() + 1000 } },
    );
    await act(async () => {});

    expect(result.current).toBe(1);
    rerender({ deadline: Date.now() + 5000 });
    await act(async () => {});
    expect(result.current).toBe(5);
  });
});
