"use client";

import dynamic from "next/dynamic";
import { useEffect, useRef, useState } from "react";

import type { ClicksChartProps } from "./clicks-chart";

const ClicksChart = dynamic(() => import("./clicks-chart").then((module) => module.ClicksChart), {
  ssr: false,
  loading: () => <ChartPlaceholder />,
});

const SKELETON_BARS = [42, 58, 48, 66, 54, 72, 62, 78, 58, 68, 84, 74, 88, 70, 92];

function ChartPlaceholder() {
  return (
    <div
      aria-hidden="true"
      className="flex h-64 w-full items-end gap-1.5 rounded-xl bg-muted/40 px-3 pt-6 pb-4"
    >
      {SKELETON_BARS.map((height, index) => (
        <span
          key={index}
          className="flex-1 rounded-t-md bg-muted"
          style={{ height: `${height}%` }}
        />
      ))}
    </div>
  );
}

export function DeferredClicksChart(props: ClicksChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (visible) {
      return;
    }

    const node = containerRef.current;
    if (!node) {
      return;
    }

    if (typeof IntersectionObserver === "undefined") {
      const timer = window.setTimeout(() => setVisible(true), 0);
      return () => window.clearTimeout(timer);
    }

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting)) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { rootMargin: "0px" },
    );
    observer.observe(node);

    return () => observer.disconnect();
  }, [visible]);

  return (
    <div ref={containerRef} className="h-64 w-full" aria-busy={!visible}>
      {visible ? <ClicksChart {...props} /> : <ChartPlaceholder />}
    </div>
  );
}
