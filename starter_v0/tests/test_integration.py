from __future__ import annotations

import json
from pathlib import Path

import pytest

from providers.base import ModelResponse, ToolCall
from tools.calculator.tool import calculate


@pytest.mark.parametrize("expression, expected", [
    ("9007199254740993 + 2", 9007199254740995),
    ("120 * 1.15 / 4", 34.5), ("10 % 3", 1),
])
def test_calculator_preserves_integers_and_documents_percent(expression, expected):
    assert calculate(expression)["result"] == expected


@pytest.mark.parametrize("expression", [True, 12, "True", "20%", "1e309", "2 ** 1000000", "__import__('os')", "1+" * 300])
def test_calculator_rejects_invalid_or_excessive_input(expression):
    assert "error" in calculate(expression)


class SequenceProvider:
    def __init__(self, responses):
        self.responses = iter(responses)

    def complete(self, *args, **kwargs):
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        return response


def test_ui_loop_preserves_tools_clarification_and_transcript(tmp_path):
    from ui_runtime import new_session, run_ui_turn
    session = new_session("groq", "test")
    history = []
    provider = SequenceProvider([
        ModelResponse(tool_calls=[ToolCall("calculator", {"expression": "2+3"})]),
        ModelResponse(text="Kết quả là 5."),
        ModelResponse(tool_calls=[ToolCall("clarify", {"question": "Bạn muốn đọc URL nào?"})]),
    ])
    first = run_ui_turn("Tính 2+3", history, session, provider=provider, transcripts_dir=tmp_path)
    second = run_ui_turn("Đọc bài này", history, session, provider=provider, transcripts_dir=tmp_path)
    assert first["tool_events"][0]["result"]["result"] == 5
    assert second["status"] == "waiting_for_user"
    saved = json.loads(next(tmp_path.glob("*.transcript.json")).read_text(encoding="utf-8"))
    assert saved["prompt_hash"] and saved["tools_hash"] and saved["model"]
    assert len(saved["turns"]) == 2 and len(history) == 4


def test_provider_failure_keeps_executed_tool_evidence(tmp_path):
    from ui_runtime import new_session, run_ui_turn
    provider = SequenceProvider([
        ModelResponse(tool_calls=[ToolCall("calculator", {"expression": "2+3"})]),
        RuntimeError("provider request failed"),
    ])
    result = run_ui_turn("Tính 2+3", [], new_session("groq", "test"), provider=provider, transcripts_dir=tmp_path)
    assert result["status"] == "provider_error"
    assert result["tool_events"][0]["result"]["result"] == 5


def test_send_error_remains_visible_in_transcript(tmp_path):
    from ui_runtime import new_session, run_ui_turn
    provider = SequenceProvider([
        ModelResponse(tool_calls=[ToolCall("send", {"text": "Bản tin thử", "confirmed": True})]),
        ModelResponse(text="Không gửi được vì chưa cấu hình Telegram."),
    ])
    result = run_ui_turn("Xác nhận gửi bản tin thử", [], new_session("groq", "test"), provider=provider, transcripts_dir=tmp_path)
    assert result["tool_events"][0]["result"]["error"] == "RuntimeError"
    assert result["tool_events"][0]["result"].get("status") != "sent"


def test_ui_starts_and_executes_chat_without_real_provider(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest
    import ui_runtime
    monkeypatch.setattr("env_loader.load_lab_env", lambda root: None)
    real_run = ui_runtime.run_ui_turn
    provider = SequenceProvider([ModelResponse(text="Kết nối vòng lặp thành công.")])
    monkeypatch.setattr(ui_runtime, "run_ui_turn", lambda user, history, session: real_run(
        user, history, session, provider=provider, transcripts_dir=tmp_path))
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run(timeout=20)
    assert not app.exception
    assert app.selectbox[0].value == "groq"
    app.chat_input[0].set_value("Chào bạn").run(timeout=20)
    assert not app.exception
    assert app.session_state.session["turns"][0]["assistant_text"] == "Kết nối vòng lặp thành công."
