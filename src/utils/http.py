import time

import requests


RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def request_with_retry(
    method,
    url,
    *,
    max_attempts=4,
    timeout=20,
    **kwargs,
):
    """Make an HTTP request and retry temporary failures."""
    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.request(
                method,
                url,
                timeout=timeout,
                **kwargs,
            )

            if response.status_code not in RETRYABLE_STATUS_CODES:
                return response

            if attempt == max_attempts:
                response.raise_for_status()

            wait = 2 ** attempt
            print(
                f"[retry] HTTP {response.status_code}. "
                f"Waiting {wait}s "
                f"(attempt {attempt}/{max_attempts})..."
            )
            time.sleep(wait)

        except (requests.Timeout, requests.ConnectionError):
            if attempt == max_attempts:
                raise

            wait = 2 ** attempt
            print(
                f"[retry] Network error. "
                f"Waiting {wait}s "
                f"(attempt {attempt}/{max_attempts})..."
            )
            time.sleep(wait)

    raise RuntimeError("HTTP request failed after all retry attempts.")