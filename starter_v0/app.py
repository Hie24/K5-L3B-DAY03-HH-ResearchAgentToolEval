"""Run from starter_v0: python -m streamlit run app.py."""
from __future__ import annotations

import json

import streamlit as st

from env_loader import load_lab_env
from ui_runtime import ROOT, new_session, run_ui_turn
from versioning import artifact_version_dict, build_artifact_version

load_lab_env(ROOT)
st.set_page_config(page_title="Research Agent", page_icon="🔍", layout="wide")
st.title("🔍 Research Agent")
st.caption("Tìm thông tin, đọc nguồn và tính toán; hỏi lại khi thiếu dữ liệu và xác nhận trước khi gửi.")

with st.sidebar:
    st.header("Cấu hình")
    provider = st.selectbox("Provider", ["groq", "ollama", "openrouter", "openai", "gemini", "anthropic"])
    model = st.text_input("Model (để trống dùng mặc định)").strip() or None
    version = st.text_input("Version", value="v4-integration").strip() or "v4-integration"
    artifacts = build_artifact_version(version, ROOT / "artifacts/system_prompt.md", ROOT / "artifacts/tools.yaml")
    with st.expander("Phiên bản và bằng chứng"):
        st.json(artifact_version_dict(artifacts))
    st.markdown('Ví dụ: "Tính 120 * 1.15 / 4"; "Tin AI hôm nay"; "Đọc bài ở đường link này".')
    reset = st.button("Xoá lịch sử / Phiên mới")

fingerprint = (provider, model, artifacts.artifact_version)
if reset or st.session_state.get("fingerprint") != fingerprint:
    st.session_state.fingerprint = fingerprint
    st.session_state.history = []
    st.session_state.session = new_session(provider, version, model)


def render_turn(turn):
    with st.chat_message("user"):
        st.markdown(turn["user"])
    with st.chat_message("assistant"):
        st.markdown(turn["assistant_text"])
        if turn["status"] == "provider_error":
            st.error("Không hoàn tất lượt này do lỗi provider; chưa có bằng chứng thành công.")
        for event in turn["tool_events"]:
            if event.get("result", {}).get("error"):
                st.error(f"Tool {event['tool']} lỗi: {event['result']['error']}")
        if turn["tool_events"]:
            with st.expander("Tool calls và kết quả"):
                st.json(turn["tool_events"])


for turn in st.session_state.session["turns"]:
    render_turn(turn)

if user_input := st.chat_input("Nhập yêu cầu research..."):
    with st.spinner("Đang xử lý..."):
        record = run_ui_turn(user_input, st.session_state.history, st.session_state.session)
    render_turn(record)

st.download_button(
    "Tải transcript của phiên",
    data=json.dumps(st.session_state.session, ensure_ascii=False, indent=2),
    file_name=f"{st.session_state.session['transcript_id']}.transcript.json",
    mime="application/json",
)
