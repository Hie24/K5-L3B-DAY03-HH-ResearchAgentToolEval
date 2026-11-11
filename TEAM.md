# Team

## Thông tin nhóm

- Tên nhóm: `HH`
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-HH-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt: `https://github.com/Hie24/K5-L3B-DAY03-HH-ResearchAgentToolEval` (nhánh `main`)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Đức Hiếu | 2A202603772 |  |  | CP1 & CP2 (Setup, Groq Provider, Baseline v0 & Tối ưu v1–v3) |
|   2 | Nguyễn Mạnh Quân | 2A202603776 |  | — | CP3 & CP4 (Tool mới `calculator`, Unit tests, 10 case eval nhóm) |
|   3 | Lê Danh Giang | 2A202603912 | 26ai.giangld@vinuni.edu.vn | `giangj` | CP5 (Streamlit Demo UI, Live Chat Transcript, Tổng hợp Báo cáo) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## NguyenDucHieu-2A202603772

### Phần việc phụ trách

- Setup môi trường, cấu hình API và chạy baseline (CP1).
- Tối ưu prompt, tool declaration qua v1–v3 và phân tích kết quả (CP2).
- Kiểm tra bằng chứng, bàn giao và review nhánh thành viên làm CP3–CP4.

### Đóng góp cụ thể

- Tích hợp Groq khi Gemini gặp giới hạn quota; dùng thống nhất model `openai/gpt-oss-120b` cho chuỗi eval.
- Bổ sung script giãn cách yêu cầu và retry có giới hạn, lưu snapshot cùng hash để đối chiếu từng version (đạt accuracy từ 65% lên 85%).
- Review code, case eval nhóm và xử lý xung đột tích hợp.

### Bằng chứng

- Commit: [5b7dd24 — CP1–CP2](https://github.com/Hie24/K5-L3B-DAY03-HH-ResearchAgentToolEval/commit/5b7dd24b292f2afa7ecc417bb46f846215b0d536)
- Code & Script: `starter_v0/providers/groq_provider.py`, `starter_v0/scripts/run_paced_eval.py`
- Version & Run: `starter_v0/artifacts/version_log.csv`, `starter_v0/runs/v0_...json` đến `v3_...json`

## NguyenManhQuan-2A202603776

### Phần việc phụ trách

- CP3: Phát triển Tool mới `calculator` và xây dựng bộ Unit Test.
- CP4: Xây dựng Bộ 10 Eval Cases của Nhóm (`eval_group.json`) và thực thi đánh giá.

### Đóng góp cụ thể

- Thiết kế tool `calculator` sử dụng `ast` node visitor để đảm bảo an toàn (không dùng `eval()`) và chuẩn hóa việc trả dictionary lỗi khi có ngoại lệ.
- Viết 3 unit test chuyên sâu cho tool mới và giữ suite `pytest` xanh (63 passed, 0 failed).
- Xây dựng 10 eval cases độc lập (5 single-turn + 5 multi-turn) và thực thi chạy đo lường thực tế trên Groq lẫn Ollama local (`qwen2.5:7b`).

### Bằng chứng

- Code Tool & Test: `starter_v0/tools/calculator/`, `starter_v0/tests/test_tools_todo.py`
- Dataset & Runs: `starter_v0/data/eval_group.json`, `starter_v0/runs/v3_B_group_groq_...json`, `starter_v0/runs/v3_B_group_ollama_...json`

## LeDanhGiang-2A202603912

### Phần việc phụ trách

- CP5: Xây dựng Giao diện Demo (Streamlit UI), chạy Live Chat thu thập Transcript, và hoàn thiện Báo cáo Nhóm & Cá nhân.

### Đóng góp cụ thể

- Thiết kế và triển khai giao diện tương tác `starter_v0/app.py` tích hợp vòng lặp agent, hiển thị trực quan tool calls, hash phiên bản và hỗ trợ Cloudflare Tunnel.
- Thực hiện phiên live chat đa lượt (`v3`) kiểm chứng các kịch bản `lookup`, `clarify`, `timeline` và rào chắn xác nhận `send`, lưu log tại `starter_v0/transcripts/`.
- Tổng hợp và hoàn thiện nội dung Phần A và Phần B của báo cáo nhóm `report/team/group_report.md`.

### Bằng chứng

- UI & Transcript: `starter_v0/app.py`, `starter_v0/requirements.txt`, `starter_v0/transcripts/openrouter_v3_cp5_demo.transcript.json`
- Báo cáo: `report/team/group_report.md`, `report/team/2A202603912_LeDanhGiang.md`
