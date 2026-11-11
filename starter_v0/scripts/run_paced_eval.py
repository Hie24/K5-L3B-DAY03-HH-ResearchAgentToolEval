"""Run the unchanged live evaluator with provider pacing and transient retries.

Example (from starter_v0):
    python scripts/run_paced_eval.py --min-interval 20 --provider groq \
        --model openai/gpt-oss-120b --version v3 --suite base \
        --eval-cases data/eval_base.json

Only provider request timing changes. Cases, model responses, tool execution,
grading, artifact hashes and run JSON are handled by the starter evaluator.
Provider attempts are recorded separately under runs/provider_events/.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import run_eval


def main() -> None:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--min-interval", type=float, default=15.0)
    parser.add_argument("--max-attempts", type=int, default=3)
    pacing, eval_args = parser.parse_known_args()
    if pacing.min_interval < 0 or pacing.max_attempts < 1:
        raise SystemExit("Require min-interval >= 0 and max-attempts >= 1.")
    if "--help" in eval_args or "-h" in eval_args:
        sys.argv = [sys.argv[0], *eval_args]
        run_eval.main()
        return

    version_index = eval_args.index("--version") if "--version" in eval_args else -1
    version = eval_args[version_index + 1] if version_index >= 0 else "unknown"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    event_file = ROOT / "runs" / "provider_events" / f"{run_eval.safe_slug(version)}_{stamp}.jsonl"
    event_file.parent.mkdir(parents=True, exist_ok=True)

    def event(kind: str, **fields: Any) -> None:
        record = {"at": datetime.now(timezone.utc).isoformat(), "event": kind, "version": version, **fields}
        with event_file.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")

    event("settings", min_interval=pacing.min_interval, max_attempts=pacing.max_attempts)
    original_factory = run_eval.make_provider

    class PacedProvider:
        def __init__(self, inner: Any) -> None:
            self.inner = inner
            self.default_model = getattr(inner, "default_model", None)
            self.last_started: float | None = None
            self.request_number = 0
            self.daily_quota_error: Exception | None = None

        def complete(self, *args: Any, **kwargs: Any) -> Any:
            self.request_number += 1
            if self.daily_quota_error is not None:
                event("skipped_request", number=self.request_number, reason="daily_quota_exhausted")
                raise self.daily_quota_error
            for attempt in range(1, pacing.max_attempts + 1):
                if self.last_started is not None:
                    remaining = pacing.min_interval - (time.monotonic() - self.last_started)
                    if remaining > 0:
                        time.sleep(remaining)
                self.last_started = time.monotonic()
                model = kwargs.get("model") or self.default_model
                event("request", number=self.request_number, attempt=attempt, model=model)
                try:
                    response = self.inner.complete(*args, **kwargs)
                except Exception as exc:
                    code = getattr(exc, "status_code", None) or getattr(exc, "code", None)
                    event("error", number=self.request_number, attempt=attempt, code=code, error=type(exc).__name__)
                    if code not in (429, 500, 502, 503, 504) or attempt == pacing.max_attempts:
                        raise
                    # A daily quota cannot be fixed by retrying within this run.
                    detail = str(exc)
                    if code == 429 and ("PerDay" in detail or "per day" in detail.lower()):
                        self.daily_quota_error = exc
                        raise
                    match = re.search(r"(?:retry|try again) in ([\d.]+)s", detail, re.IGNORECASE)
                    headers = getattr(getattr(exc, "response", None), "headers", {})
                    retry_after = headers.get("retry-after", "")
                    server_delay = float(retry_after) if re.fullmatch(r"[\d.]+", retry_after) else (float(match.group(1)) if match else 30.0)
                    cooldown = max(pacing.min_interval, server_delay + 1)
                    event("cooldown", number=self.request_number, seconds=round(cooldown, 2))
                    print(f"Provider {code}: retry {attempt + 1}/{pacing.max_attempts} after {cooldown:.1f}s", flush=True)
                    while cooldown > 0:
                        chunk = min(cooldown, 15.0)
                        time.sleep(chunk)
                        cooldown -= chunk
                else:
                    event("response", number=self.request_number, attempt=attempt, seconds=round(time.monotonic() - self.last_started, 3))
                    return response
            raise AssertionError("Provider attempt loop ended unexpectedly")

    run_eval.make_provider = lambda name: PacedProvider(original_factory(name))
    sys.argv = [sys.argv[0], *eval_args]
    try:
        run_eval.main()
    finally:
        run_eval.make_provider = original_factory
        event("finished")
        print(f"Provider events: {event_file}", flush=True)


if __name__ == "__main__":
    main()
