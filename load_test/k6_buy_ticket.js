import http from 'k6/http';
import { check, sleep } from 'k6';


const BASE_URL = 'http://127.0.0.1:5000';
const TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NDc5NjU0MywianRpIjoiOGRkYmFhNjMtMWZmZS00MjY0LTk1MWEtNjVkMDg5MDEwNGNkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NzQ3OTY1NDMsImNzcmYiOiI5ODBlMDEwZC0zMDFjLTQxMjMtYjVjNS1iNjNiZjA4YmI5MzUiLCJleHAiOjE3NzQ3OTc0NDN9.X9F90iIe1fxZzKAodnhXRo14gcMRZBaoazdrM3Bn3w4';

export const options = {
  scenarios: {
    normal_load: {
      executor: 'constant-vus',
      vus: 20,
      duration: '30s',
    },
    peak_load: {
      executor: 'constant-vus',
      vus: 50,
      duration: '30s',
      startTime: '35s',
    },
    stress_load: {
      executor: 'constant-vus',
      vus: 100,
      duration: '30s',
      startTime: '70s',
    },
  },
};

export default function () {
  const uniquePassenger = `LoadTestUser_${__VU}_${__ITER}_${Date.now()}`;

  const payload = JSON.stringify({
    flight_number: 'TK900',
    date: '2026-04-20T09:00:00',
    passenger_names: [uniquePassenger],
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + TOKEN,
    },
  };

  const res = http.post(`${BASE_URL}/tickets/buy`, payload, params);

  check(res, {
    'buy ticket status is success': (r) => r.status === 200 || r.status === 201,
  });

  sleep(1);
}