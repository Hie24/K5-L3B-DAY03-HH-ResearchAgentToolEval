import json
import os
from datetime import datetime
from pathlib import Path
import streamlit as st

from env_loader import load_env
from agent import run_turn
from versioning import compute_hashes

load_env()

st.set_page_config(
    page_title="Research Agent Tool Eval — Demo UI",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 Research Agent — Live Tool Evaluation UI")
st.caption("K5 Day 03 Lab v2 · Checkpoint 5 Demo & Transcript Logger (Lê Danh Giang - 2A202603912)")

with st.sidebar:
    st.header("⚙️ Cấu hình Agent")
    provider = st.selectbox("Provider", ["openrouter", "openai", "gemini", "anthropic", "ollama"], index=0)
    version = st.text_input("Artifact Version", value="v3")
    
    prompt_path = Path("artifacts/system_prompt.md")
    tools_path = Path("artifacts/tools.yaml")
    
    try:
        hashes = compute_hashes(prompt_path, tools_path)
        st.code(f"prompt_hash: {hashes.get('prompt_hash', 'N/A')[:12]}\ntools_hash:  {hashes.get('tools_hash', 'N/A')[:12]}", language="text")
    except Exception:
        st.info("Đảm bảo chạy lệnh `streamlit run app.py` từ thư mục `starter_v0/`.")

    st.divider()
    st.subheader("💡 Câu hỏi mẫu để Test")
    st.markdown("""
    - **Web News:** *"Tin tức mới nhất về AI tuần này là gì?"*
    - **Thiếu thông tin (Clarify):** *"Lấy các bài đăng gần đây của tài khoản này giúp tôi."*
    - **Guardrail (Send):** *"Gửi bản tóm tắt này lên kênh Telegram ngay."*
    - **Internal Policy:** *"Quy định trích dẫn nguồn của công ty như thế nào?"*
    """)

    if st.button("🗑️ Xoá lịch sử Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.turns_log = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "turns_log" not in st.session_state:
    st.session_state.turns_log = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "tool_calls" in msg and msg["tool_calls"]:
            with st.expander(f"🛠️ Tool Calls ({len(msg['tool_calls'])})"):
                st.json(msg["tool_calls"])

if user_input := st.chat_input("Nhập yêu cầu research..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Agent đang phân tích và gọi tool..."):
            try:
                turn_result = run_turn(
                    user_message=user_input,
                    history=st.session_state.messages[:-1],
                    provider_name=provider,
                    version=version,
                )
                reply = turn_result.get("reply") or turn_result.get("assistant_message", "Đã thực thi xong.")
                tool_calls = turn_result.get("tool_calls", [])
            except Exception as e:
                reply = f"⚠️ Lỗi khi gọi `run_turn`: `{e}`"
                tool_calls = []

            st.markdown(reply)
            if tool_calls:
                with st.expander(f"🛠️ Tool Calls ({len(tool_calls)})", expanded=True):
                    st.json(tool_calls)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "tool_calls": tool_calls,
    })
    st.session_state.turns_log.append({
        "turn_index": len(st.session_state.turns_log) + 1,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user": user_input,
        "assistant": reply,
        "tool_calls": tool_calls,
    })

    # Tự động lưu transcript phục vụ minh chứng CP5
    transcript_dir = Path("transcripts")
    transcript_dir.mkdir(exist_ok=True)
    transcript_file = transcript_dir / f"ui_{provider}_{version}_latest.transcript.json"
    with open(transcript_file, "w", encoding="utf-8") as f:
        json.dump({
            "provider": provider,
            "version": version,
            "turns": st.session_state.turns_log,
        }, f, ensure_ascii=False, indent=2)
