import exec from "k6/execution";
import http from "k6/http";
import { check } from "k6";
import { Counter, Trend } from "k6/metrics";

const BASE_URL = __ENV.BASE_URL || "http://api:8000";
const MODE = __ENV.MODE || "warm";
const COLD_CODES = Number(__ENV.CODES || 500);
const CODE_TTL_SECONDS = Number(__ENV.CODE_TTL_SECONDS || 3600);
const CODES_FROM_FILE = __ENV.CODES_FILE ? JSON.parse(open(__ENV.CODES_FILE)) : null;
const rateLimited = new Counter("rate_limited");
const redirectOk = new Counter("redirect_ok");
const serverErrors = new Counter("server_errors");
const otherStatuses = new Counter("other_statuses");
const redirectDuration = new Trend("redirect_duration", true);

const urlFor = (index) => `https://93.184.216.34/loadtest/redirect-${index}`;
const createIp = (index) => `198.51.100.${(index % 250) + 1}`;
const syntheticIp = (seed) => {
  const value = seed % 65025;
  return `198.18.${Math.floor(value / 255)}.${(value % 255) + 1}`;
};
const vuIp = () => syntheticIp(__VU * 1000 + __ITER);

function scenarioOptions() {
  if (MODE === "cold") {
    return {
      cold: {
        executor: "shared-iterations",
        exec: "cold",
        vus: 50,
        iterations: COLD_CODES,
        maxDuration: "3m",
      },
    };
  }
  if (MODE === "ratelimit") {
    return {
      rate_limit: {
        executor: "ramping-arrival-rate",
        exec: "rateLimit",
        startRate: 20,
        timeUnit: "1s",
        preAllocatedVUs: 50,
        maxVUs: 400,
        stages: [
          { target: 50, duration: "10s" },
          { target: 150, duration: "20s" },
          { target: 300, duration: "20s" },
          { target: 300, duration: "10s" },
          { target: 0, duration: "5s" },
        ],
      },
    };
  }
  return {
    warm: {
      executor: "ramping-arrival-rate",
      exec: "warm",
      startRate: 50,
      timeUnit: "1s",
      preAllocatedVUs: 50,
      maxVUs: 150,
      stages: [
        { target: 75, duration: "10s" },
        { target: 100, duration: "20s" },
        { target: 150, duration: "20s" },
        { target: 150, duration: "10s" },
        { target: 0, duration: "5s" },
      ],
    },
  };
}

export const options = {
  setupTimeout: "5m",
  summaryTrendStats: ["avg", "min", "med", "p(50)", "p(90)", "p(95)", "p(99)", "max"],
  scenarios: scenarioOptions(),
  thresholds: {
    ...(MODE === "ratelimit" ? { rate_limited: ["count>0"] } : {}),
  },
};

export function setup() {
  if (MODE === "cold" && CODES_FROM_FILE) {
    if (!Array.isArray(CODES_FROM_FILE) || CODES_FROM_FILE.length === 0) {
      throw new Error(`CODES_FILE ${__ENV.CODES_FILE} is empty or invalid`);
    }
    return { codes: CODES_FROM_FILE };
  }
  const count = MODE === "cold" ? COLD_CODES : 1;
  const codes = [];
  for (let index = 0; index < count; index += 1) {
    const response = http.post(
      `${BASE_URL}/api/v1/links`,
      JSON.stringify({ url: urlFor(index) }),
      {
        headers: {
          "Content-Type": "application/json",
          "X-Forwarded-For": createIp(index),
        },
      },
    );
    if (response.status !== 201) {
      throw new Error(
        `setup create ${index} failed: ${response.status} ${response.body}`,
      );
    }
    codes.push(response.json("code"));
  }
  return { codes };
}

export function warm(data) {
  const response = http.get(`${BASE_URL}/api/v1/r/${data.codes[0]}`, {
    redirects: 0,
    headers: { "X-Forwarded-For": vuIp() },
  });
  redirectDuration.add(response.timings.duration);
  if (response.status === 429) {
    rateLimited.add(1);
  } else if (response.status === 302) {
    redirectOk.add(1);
  } else if (response.status >= 500) {
    serverErrors.add(1);
  } else {
    otherStatuses.add(1);
  }
  check(response, { "warm redirect is 302": (item) => item.status === 302 });
}

export function cold(data) {
  const index = exec.scenario.iterationInTest % data.codes.length;
  const response = http.get(`${BASE_URL}/api/v1/r/${data.codes[index]}`, {
    redirects: 0,
    headers: { "X-Forwarded-For": syntheticIp(__VU * 1000 + index) },
  });
  redirectDuration.add(response.timings.duration);
  if (response.status === 429) {
    rateLimited.add(1);
  } else if (response.status === 302) {
    redirectOk.add(1);
  } else if (response.status >= 500) {
    serverErrors.add(1);
  } else {
    otherStatuses.add(1);
  }
  check(response, { "cold redirect is 302": (item) => item.status === 302 });
}

export function rateLimit(data) {
  const response = http.get(`${BASE_URL}/api/v1/r/${data.codes[0]}`, {
    redirects: 0,
    headers: { "X-Forwarded-For": "203.0.113.201" },
  });
  redirectDuration.add(response.timings.duration);
  if (response.status === 429) {
    rateLimited.add(1);
  } else if (response.status === 302) {
    redirectOk.add(1);
  } else if (response.status >= 500) {
    serverErrors.add(1);
  } else {
    otherStatuses.add(1);
  }
  check(response, {
    "shared-ip redirect is 302 or 429": (item) =>
      item.status === 302 || item.status === 429,
  });
}

export function handleSummary(data) {
  return {
    stdout: JSON.stringify(
      {
        mode: MODE,
        setup_codes: COLD_CODES,
        code_ttl_seconds: CODE_TTL_SECONDS,
        metrics: data.metrics,
      },
      null,
      2,
    ),
  };
}
