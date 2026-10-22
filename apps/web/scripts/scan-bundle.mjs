import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative } from "node:path";

const target = process.argv[2] ?? ".next/static";
const patterns = [
  /postgresql\+asyncpg:\/\//i,
  /redis:\/\//i,
  /-----BEGIN [A-Z ]*PRIVATE KEY-----/,
  /\bsk_live_[A-Za-z0-9]+/,
  /\bAKIA[0-9A-Z]{16}\b/,
  /NEXT_PUBLIC_[A-Z0-9_]*(SECRET|TOKEN|PASSWORD|PRIVATE|DATABASE|REDIS)/,
];

const secretValues = [
  "JWT_SECRET",
  "CSRF_SECRET",
  "SESSION_SECRET",
  "METRICS_TOKEN",
  "GOOGLE_CLIENT_SECRET",
  "DATABASE_URL",
  "REDIS_URL",
]
  .map((name) => process.env[name])
  .filter((value) => typeof value === "string" && value.length >= 12)
  .filter((value) => !value.startsWith("change-me") && !value.startsWith("dev-insecure-"));

if (!existsSync(target)) {
  console.warn(`[scan-bundle] ${target} does not exist; run the production build first.`);
  process.exit(0);
}

function files(directory) {
  const result = [];
  for (const entry of readdirSync(directory)) {
    const path = join(directory, entry);
    if (statSync(path).isDirectory()) {
      result.push(...files(path));
    } else {
      result.push(path);
    }
  }
  return result;
}

const findings = [];
for (const path of files(target)) {
  const source = readFileSync(path, "utf8");
  for (const pattern of patterns) {
    if (pattern.test(source)) {
      findings.push(`${relative(process.cwd(), path)} matched ${pattern}`);
    }
  }
  for (const value of secretValues) {
    if (source.includes(value)) {
      findings.push(`${relative(process.cwd(), path)} contains a configured secret value`);
    }
  }
}

if (findings.length > 0) {
  console.error("[scan-bundle] potential secret exposure:");
  for (const finding of findings) {
    console.error(`- ${finding}`);
  }
  process.exit(1);
}

console.log(`[scan-bundle] ${target} contains no configured secrets or secret-like names.`);
