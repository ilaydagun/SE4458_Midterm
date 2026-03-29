import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = 'http://127.0.0.1:5000';

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
  const res = http.get(
    `${BASE_URL}/flights/query?airport_from=Izmir&airport_to=Istanbul&number_of_people=1&page=1&per_page=10`
  );

  check(res, {
    'query status is 200': (r) => r.status === 200,
  });

  sleep(1);
}