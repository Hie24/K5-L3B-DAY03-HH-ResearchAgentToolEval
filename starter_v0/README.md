# Source code

Toàn bộ source code của lab nằm trong folder này. Chạy mọi lệnh từ `starter_v0/`.

- File bắt đầu chạy: `run_eval.py` (chạy eval), `chat.py` (chat live), `scripts/preflight_provider.py` (kiểm tra provider).
- Cách chạy: `python run_eval.py --provider openrouter --version v0 --suite base --eval-cases data/eval_base.json`; `python chat.py --provider openrouter --version v3`; `pytest`.
- Input: `artifacts/system_prompt.md`, `artifacts/tools.yaml`, bộ case `data/*.json`, API key trong `.env` (mẫu ở `.env.example`).
- Output: `runs/*.json` (kết quả eval), `transcripts/*.transcript.json` (chat live), `analysis/*.csv` (nếu chạy `scripts/parse_runs.py`).
- File học viên được sửa: `artifacts/system_prompt.md`, `artifacts/tools.yaml`, `artifacts/version_log.csv`, `data/eval_group.json`, `tools/` (thêm tool mới và đăng ký trong `tools/__init__.py`), `tests/test_tools_todo.py`, code UI và `requirements.txt`. Không sửa nội dung case trong `data/eval_base.json`.

Chi tiết từng bước xem [README.md](../README.md) ở root; cấu hình API key xem [docs/TOOL-SETUP.md](../docs/TOOL-SETUP.md).

Groq: điền `GROQ_API_KEY` trong `.env`, dùng `--provider groq --model openai/gpt-oss-120b` với các lệnh có sẵn. Adapter dùng API tương thích OpenAI theo [tài liệu Groq](https://console.groq.com/docs/openai), giữ nguyên cách chạy tool và chấm điểm.

```powershell
python scripts/preflight_provider.py --provider groq --model openai/gpt-oss-120b
python scripts/run_paced_eval.py --min-interval 20 --provider groq --model openai/gpt-oss-120b --version v3 --suite base --eval-cases data/eval_base.json
```

`run_paced_eval.py` gọi lại bộ chấm `run_eval.py`, chỉ thêm khoảng nghỉ giữa yêu cầu và retry lỗi API tạm thời; log từng lần gọi nằm trong `runs/provider_events/`. Dùng cùng provider/model cho v0–v3 và chỉ so sánh run đủ case, không có provider error.

Prompt/tools của từng vòng được giữ trong `artifacts/versions/v0` đến `v3`. Để tái lập một vòng, chọn đúng `--version` và thêm `--system-prompt artifacts/versions/<version>/system_prompt.md --tools artifacts/versions/<version>/tools.yaml`. Các run dùng để so sánh nằm trong `artifacts/version_log.csv`; các run thử nghiệm Groq không dùng để so sánh được giữ riêng.


## Bản tích hợp CP1–CP5

Cài `pip install -r requirements.txt`, cấu hình `.env`, rồi chạy từ `starter_v0/`:

```powershell
python -m streamlit run app.py
python chat.py --provider groq --model openai/gpt-oss-120b --version v4-integration
python scripts/verify_live_chat.py
python scripts/run_paced_eval.py --min-interval 20 --provider groq --version v4-integration --suite group --eval-cases data/eval_group.json
```

UI mặc định Groq, cho phép chọn model, hiển thị cả lỗi tool và tải transcript. Mỗi phiên có ID riêng cùng model, hash, rounds và tool results; đổi cấu hình sẽ bắt đầu phiên mới. Link local: http://localhost:8501. Có thể mở link tạm bằng `cloudflared tunnel --url http://localhost:8501`; chưa có link public cố định trong repo.

Snapshot v0–v3 giữ nguyên bằng chứng CP1–CP2; `v3-calculator` lưu artifact của run group cũ; `v4-integration` là bản sửa tích hợp. Transcript OpenRouter cũ được đánh dấu chưa xác minh, không dùng làm bằng chứng live hoặc gửi Telegram thật.
