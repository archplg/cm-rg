"""
Phase 2L · Pre-flight Check 6: Auto-retry with backoff test.

Verifies the retry strategy handles transient failures:
  - HTTP 429 (rate limit) -> retry with backoff
  - HTTP 500/502/503 (server error) -> retry
  - Timeout -> retry
  - HTTP 400/401 (client error) -> DO NOT retry, fail fast
  - HTTP 200 -> success, no retry

Uses a mock HTTP layer. Cost: $0.
Usage: python check6_auto_retry_test.py
"""
from __future__ import annotations

import sys
import time
from typing import Any


# Mock retry implementation matching openrouter section of config_phase2l.yaml
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}
NO_RETRY_STATUS_CODES = {400, 401, 403, 404}
BACKOFF_SECONDS = [10, 30, 90]


class MockResponse:
    def __init__(self, status_code: int, body: Any = None):
        self.status_code = status_code
        self.body = body or {}


def retry_call(make_call, max_retries: int = 3, backoffs: list = None,
               sleep_fn=None) -> tuple[MockResponse, int]:
    """Retry logic. Returns (response, attempts)."""
    backoffs = backoffs or BACKOFF_SECONDS
    sleep_fn = sleep_fn or time.sleep
    attempts = 0
    last_resp = None
    while attempts <= max_retries:
        attempts += 1
        try:
            resp = make_call()
            last_resp = resp
            if resp.status_code == 200:
                return resp, attempts
            if resp.status_code in NO_RETRY_STATUS_CODES:
                return resp, attempts  # don't retry client errors
            if resp.status_code in RETRY_STATUS_CODES and attempts <= max_retries:
                backoff = backoffs[min(attempts - 1, len(backoffs) - 1)]
                sleep_fn(backoff)
                continue
            return resp, attempts
        except TimeoutError:
            if attempts <= max_retries:
                backoff = backoffs[min(attempts - 1, len(backoffs) - 1)]
                sleep_fn(backoff)
                continue
            raise
    return last_resp, attempts


def test_immediate_success():
    calls = [0]
    def make_call():
        calls[0] += 1
        return MockResponse(200, {"ok": True})
    resp, attempts = retry_call(make_call, sleep_fn=lambda s: None)
    assert resp.status_code == 200, f"expected 200, got {resp.status_code}"
    assert attempts == 1, f"expected 1 attempt, got {attempts}"
    print("  [PASS] 200 OK on first call - no retry")


def test_429_then_200():
    seq = [MockResponse(429), MockResponse(200, {"ok": True})]
    idx = [0]
    def make_call():
        r = seq[idx[0]]; idx[0] += 1; return r
    resp, attempts = retry_call(make_call, sleep_fn=lambda s: None)
    assert resp.status_code == 200
    assert attempts == 2, f"expected 2 attempts, got {attempts}"
    print("  [PASS] 429 then 200 - retried once")


def test_500_500_500_500_giveup():
    def make_call(): return MockResponse(500)
    resp, attempts = retry_call(make_call, sleep_fn=lambda s: None)
    assert resp.status_code == 500
    assert attempts == 4, f"expected 4 attempts (1 + 3 retries), got {attempts}"
    print("  [PASS] persistent 500 - gave up after 3 retries")


def test_400_no_retry():
    calls = [0]
    def make_call():
        calls[0] += 1
        return MockResponse(400, {"error": {"message": "invalid model ID"}})
    resp, attempts = retry_call(make_call, sleep_fn=lambda s: None)
    assert resp.status_code == 400
    assert attempts == 1, f"expected 1 attempt (no retry on 400), got {attempts}"
    print("  [PASS] 400 client error - did NOT retry")


def test_401_no_retry():
    def make_call(): return MockResponse(401)
    resp, attempts = retry_call(make_call, sleep_fn=lambda s: None)
    assert resp.status_code == 401
    assert attempts == 1
    print("  [PASS] 401 unauthorized - did NOT retry")


def test_backoff_sequence():
    sleeps = []
    def fake_sleep(s): sleeps.append(s)
    def make_call(): return MockResponse(503)
    retry_call(make_call, sleep_fn=fake_sleep)
    assert sleeps == [10, 30, 90], f"expected [10,30,90], got {sleeps}"
    print(f"  [PASS] backoff sequence correct: {sleeps}")


def test_timeout_retried():
    seq = [TimeoutError("timeout"), MockResponse(200)]
    idx = [0]
    def make_call():
        x = seq[idx[0]]; idx[0] += 1
        if isinstance(x, Exception): raise x
        return x
    resp, attempts = retry_call(make_call, sleep_fn=lambda s: None)
    assert resp.status_code == 200
    assert attempts == 2
    print("  [PASS] timeout then success - retried")


def main() -> int:
    print("Phase 2L Check 6: Auto-retry with backoff")
    print("=" * 80)
    tests = [
        test_immediate_success,
        test_429_then_200,
        test_500_500_500_500_giveup,
        test_400_no_retry,
        test_401_no_retry,
        test_backoff_sequence,
        test_timeout_retried,
    ]
    failures = 0
    for t in tests:
        try:
            t()
        except AssertionError as e:
            print(f"  [FAIL] {t.__name__}: {e}")
            failures += 1
        except Exception as e:
            print(f"  [EXC ] {t.__name__}: {type(e).__name__}: {e}")
            failures += 1
    print("=" * 80)
    print(f"{len(tests) - failures}/{len(tests)} passed. {'GO' if failures == 0 else 'FIX BEFORE RUN'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
