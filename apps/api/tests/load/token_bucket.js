import http from "k6/http";
import { check, sleep } from "k6";
import { Counter } from "k6/metrics";

const BASE_URL = __ENV.BASE_URL || "http://api:8000";
const rateLimited = new Counter("rate_limited");
const notFound = new Counter("not_found");

export const options = {
  scenarios: {
    redirect_flood: {
      executor: "constant-vus",
      exec: "redirect",
      vus: 20,
      duration: "10s",
      tags: { scenario: "redirect_flood" },
    },
    negative_scan: {
      executor: "constant-vus",
      exec: "negative",
      vus: 10,
      duration: "5s",
      tags: { scenario: "negative_scan" },
    },
    cold_stampede: {
      executor: "per-vu-iterations",
      exec: "stampede",
      vus: 100,
      iterations: 1,
      maxDuration: "20s",
      tags: { scenario: "cold_stampede" },
    },
  },
  thresholds: {
    rate_limited: ["count>0"],
    not_found: ["count>0"],
    http_req_duration: ["p(95)<1500"],
  },
};

function headers(ip) {
  return {
    "X-Forwarded-For": ip,
    Accept: "application/json",
  };
}

export function setup() {
  const create = (path) => {
    const response = http.post(
      `${BASE_URL}/api/v1/links`,
      JSON.stringify({ url: `https://93.184.216.34/${path}` }),
      {
        headers: {
          "Content-Type": "application/json",
          "X-Forwarded-For": "203.0.113.250",
        },
      },
    );
    if (response.status !== 201) {
      throw new Error(`setup create failed: ${response.status} ${response.body}`);
    }
    return response.json("code");
  };
  return {
    floodCode: create("load-flood"),
    stampedeCode: create("load-stampede"),
  };
}

export function redirect(data) {
  const response = http.get(`${BASE_URL}/api/v1/r/${data.floodCode}`, {
    redirects: 0,
    headers: headers("203.0.113.201"),
  });
  if (response.status === 429) {
    rateLimited.add(1);
  }
  check(response, {
    "redirect is 302 or rate limited": (item) => item.status === 302 || item.status === 429,
  });
  sleep(0.01);
}

export function negative() {
  const suffix = Math.random().toString(36).slice(2, 12);
  const response = http.get(`${BASE_URL}/api/v1/r/zz${suffix}`, {
    redirects: 0,
    headers: headers("203.0.113.202"),
  });
  if (response.status === 404) {
    notFound.add(1);
  }
  if (response.status === 429) {
    rateLimited.add(1);
  }
  check(response, {
    "missing code is 404 or rate limited": (item) => item.status === 404 || item.status === 429,
  });
}

export function stampede(data) {
  const response = http.get(`${BASE_URL}/api/v1/r/${data.stampedeCode}`, {
    redirects: 0,
    headers: headers(`203.0.113.${(__VU % 200) + 1}`),
  });
  check(response, {
    "cold redirect succeeds": (item) => item.status === 302,
  });
}
