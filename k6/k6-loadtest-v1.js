import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  stages: [
    { duration: "30s", target: 5 },   // warm-up
    { duration: "2m", target: 50 },   // ramp-up
    { duration: "3m", target: 50 },   // palier
    { duration: "2m", target: 100 },  // stress léger (optionnel mais utile)
    { duration: "30s", target: 0 },   // cooldown
  ],
  thresholds: {
    http_req_failed: ["rate<0.01"],       // < 1% d'erreurs
    http_req_duration: ["p(95)<800"],     // p95 global (objectif V1)
  },
};

const BASE_URL = __ENV.BASE_URL || "http://localhost:8000";
const TOKEN = __ENV.TOKEN || "";

export default function () {
  // E1: health
  const r1 = http.get(`${BASE_URL}/health`);
  check(r1, { "health 200": (r) => r.status === 200 });

  // E2: me (auth)
  const params = {
    headers: {
      Authorization: `Bearer ${TOKEN}`,
    },
  };
  const r2 = http.get(`${BASE_URL}/me`, params);
  check(r2, { "me 200": (r) => r.status === 200 });

  sleep(1);
}
