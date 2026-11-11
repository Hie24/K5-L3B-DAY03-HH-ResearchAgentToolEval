"""Run reproducible lab requests through chat.py with a real Groq provider.

No model/tool responses are mocked. The final send request stops at asking for
confirmation, so this script never supplies approval to send a message.
"""
from __future__ import annotations

import builtins
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import chat


def main() -> None:
    original_factory = chat.make_provider
    original_input = builtins.input

    class Paced:
        def __init__(self, inner):
            self.inner = inner
            self.default_model = inner.default_model
            self.last = time.monotonic()

        def complete(self, *args, **kwargs):
            for attempt in range(3):
                time.sleep(max(0, 20 - (time.monotonic() - self.last)))
                self.last = time.monotonic()
                try:
                    return self.inner.complete(*args, **kwargs)
                except Exception as exc:
                    if getattr(exc, "status_code", None) != 429 or attempt == 2:
                        raise
                    time.sleep(30)

    requests = iter([
        "Tính giúp tôi 120 * 1.15 / 4.",
        "Lấy bài đăng gần nhất của tài khoản X này giúp tôi.",
        "Tài khoản @karpathy, chỉ lấy 1 bài gần nhất.",
        "Đăng nguyên văn nội dung này lên Telegram giúp tôi: Bản tin thử: ngân sách nghiên cứu là 120 triệu đồng.",
        "/exit",
    ])

    def user_input(prompt=""):
        value = next(requests)
        print(prompt + value, flush=True)
        return value

    chat.make_provider = lambda name: Paced(original_factory(name))
    builtins.input = user_input
    sys.argv = ["chat.py", "--provider", "groq", "--model", "openai/gpt-oss-120b",
                "--version", "v4-integration", "--max-tool-rounds", "3"]
    before = set((ROOT / "transcripts").glob("v4-integration_groq_*.transcript.json"))
    try:
        chat.main()
    finally:
        chat.make_provider = original_factory
        builtins.input = original_input
    paths = set((ROOT / "transcripts").glob("v4-integration_groq_*.transcript.json")) - before
    for path in paths:
        data = json.loads(path.read_bytes())
        data["verification"] = {
            "scenario_source": "scripts/verify_live_chat.py: scripted requests, real provider and tools",
            "provider_pacing_seconds": 20,
            "external_send_requested_but_not_confirmed": True,
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("LIVE_STATUSES", [(turn["turn_index"], turn["status"]) for turn in data["turns"]])


if __name__ == "__main__":
    main()
