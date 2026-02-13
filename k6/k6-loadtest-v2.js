import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  insecureSkipTLSVerify: true, // ✅ bypass CA self-signed (local demo)
  stages: [
    { duration: "20s", target: 5 },
    { duration: "40s", target: 25 },
    { duration: "40s", target: 25 },
    { duration: "20s", target: 0 },
  ],
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<800"],
  },
};

const BASE_URL = __ENV.BASE_URL || "https://localhost:8443";
const EMAIL = __ENV.EMAIL || "admin_demo@example.com";
const PASSWORD = __ENV.PASSWORD || "Test1234!";

export function setup() {
  const loginRes = http.post(
    `${BASE_URL}/auth/login`,
    JSON.stringify({ email: EMAIL, password: PASSWORD }),
    { headers: { "Content-Type": "application/json" } }
  );

  check(loginRes, { "login 200": (r) => r.status === 200 });

  if (loginRes.status !== 200) {
    throw new Error(`Login failed: ${loginRes.status} ${loginRes.body}`);
  }

  return { token: loginRes.json("access_token") };
}

export default function (data) {
  const r1 = http.get(`${BASE_URL}/health`);
  check(r1, { "health 200": (r) => r.status === 200 });

  const r2 = http.get(`${BASE_URL}/me`, {
    headers: { Authorization: `Bearer ${data.token}` },
  });
  check(r2, { "me 200": (r) => r.status === 200 });

  const r3 = http.get(`${BASE_URL}/categories`);
  check(r3, { "categories 200": (r) => r.status === 200 });

  sleep(1);
}
