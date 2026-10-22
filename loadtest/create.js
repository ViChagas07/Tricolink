import http from "k6/http";
import { check } from "k6";
import { Counter, Trend } from "k6/metrics";

const BASE_URL = __ENV.BASE_URL || "http://api:8000";
const MODE = __ENV.MODE || "throughput";
const created = new Counter("created");
const rateLimited = new Counter("rate_limited");
const serverErrors = new Counter("server_errors");
const otherStatuses = new Counter("other_statuses");
const createDuration = new Trend("create_duration", true);

const uniqueIp = () => {
  const value = (__VU * 1000 + __ITER) % 65025;
  return `198.18.${Math.floor(value / 255)}.${(value % 255) + 1}`;
};

export const options = {
  summaryTrendStats: ["avg", "min", "med", "p(50)", "p(90)", "p(95)", "p(99)", "max"],
  scenarios:
    MODE === "ratelimit"
      ? {
          rate_limit: {
            executor: "ramping-arrival-rate",
            exec: "createWithSharedIp",
            startRate: 5,
            timeUnit: "1s",
            preAllocatedVUs: 20,
            maxVUs: 100,
            stages: [
              { target: 20, duration: "10s" },
              { target: 50, duration: "20s" },
              { target: 100, duration: "20s" },
              { target: 0, duration: "5s" },
            ],
          },
        }
      : {
          throughput: {
            executor: "ramping-arrival-rate",
            exec: "create",
            startRate: 10,
            timeUnit: "1s",
            preAllocatedVUs: 50,
            maxVUs: 150,
            stages: [
              { target: 50, duration: "10s" },
              { target: 100, duration: "20s" },
              { target: 100, duration: "20s" },
              { target: 0, duration: "5s" },
            ],
          },
        },
  thresholds: {
    http_req_duration: ["p(95)<1500"],
    ...(MODE === "ratelimit"
      ? { rate_limited: ["count>0"] }
      : { created: ["count>0"] }),
  },
};

function createLink(ip, suffix) {
  const response = http.post(
    `${BASE_URL}/api/v1/links`,
    JSON.stringify({ url: `https://93.184.216.34/loadtest/create-${suffix}` }),
    {
      headers: {
        "Content-Type": "application/json",
        "X-Forwarded-For": ip,
      },
    },
  );
  createDuration.add(response.timings.duration);
  if (response.status === 201) {
    created.add(1);
  } else if (response.status === 429) {
    rateLimited.add(1);
  } else if (response.status >= 500) {
    serverErrors.add(1);
  } else {
    otherStatuses.add(1);
  }
  check(response, {
    "create is 201 or rate limited": (item) =>
      item.status === 201 || item.status === 429,
  });
}

export function create() {
  createLink(uniqueIp(), `${__VU}-${__ITER}`);
}

export function createWithSharedIp() {
  createLink("203.0.113.202", `${__VU}-${__ITER}`);
}

export function handleSummary(data) {
  return {
    stdout: JSON.stringify({ mode: MODE, metrics: data.metrics }, null, 2),
  };
}
