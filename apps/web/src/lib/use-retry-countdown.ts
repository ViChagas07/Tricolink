"use client";

import { useEffect, useState } from "react";

export function useRetryCountdown(retryAt: number | null): number {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    if (retryAt === null) {
      return;
    }

    let active = true;
    const update = () => {
      if (!active) {
        return;
      }
      setSeconds(Math.max(0, Math.ceil((retryAt - Date.now()) / 1000)));
    };

    void Promise.resolve().then(update);
    const timer = window.setInterval(update, 1000);
    return () => {
      active = false;
      window.clearInterval(timer);
    };
  }, [retryAt]);

  return retryAt === null ? 0 : seconds;
}
