# Báo cáo cá nhân — Lê Danh Giang — 2A202603912

## 1. Thông tin thành viên

- **Họ tên:** Lê Danh Giang
- **MSSV:** 2A202603912
- **Email:** 

---

## 2. Phần việc phụ trách

1. **CP5 — Xây dựng Giao diện Demo (Streamlit UI) và Triển khai Dùng thử:** Thiết kế giao diện `starter_v0/app.py` tích hợp vòng lặp agent, hiển thị trực quan tool calls/hash và mở link public phục vụ Team Showdown.
2. **CP5 — Thực thi Live Chat đa lượt và Ghi nhận Transcript:** Chạy hội thoại thực tế với cấu hình `v3`, kiểm chứng các kịch bản định tuyến, hỏi lại khi thiếu thông tin (`clarify`) và chốt chặn xác nhận trước khi gửi (`send`), lưu bằng chứng vào `starter_v0/transcripts/`.
3. **CP5 — Tổng hợp Báo cáo Nhóm và Báo cáo Cá nhân:** Hợp nhất kết quả thực nghiệm từ CP1–CP2 (Nguyễn Đức Hiếu) và CP3–CP4 (Nguyễn Mạnh Quân) vào `report/team/group_report.md` (Phần A & Phần B) và cập nhật `TEAM.md`.

---

## 3. Đóng góp cụ thể

### 3.1. Xây dựng Giao diện Demo (`starter_v0/app.py`)

- **Thiết kế UI bằng Streamlit:**
  - Tích hợp trực tiếp hàm `run_turn` từ `starter_v0/agent.py` và `compute_hashes` từ `starter_v0/versioning.py`.
  - Hỗ trợ chọn nhanh các provider đã cấu hình của nhóm (`groq`, `ollama`, `openrouter`, `gemini`, `openai`) và version (`v3`).
  - Hiển thị trực tiếp mã băm `prompt_hash` và `tools_hash` trên thanh sidebar để đối chiếu tính toàn vẹn của artifact khi demo.
  - Hiển thị chi tiết từng lệnh gọi công cụ (`tool_calls` và `arguments`) dưới dạng khung mở rộng (`st.expander`) ngay dưới câu trả lời và tự động xuất lịch sử hội thoại ra file `.transcript.json`.
- **Cập nhật Dependency & Chia sẻ dùng thử:**
  - Bổ sung `streamlit>=1.32.0` vào `starter_v0/requirements.txt`.
  - Cấu hình chạy local tại `http://localhost:8501` và xuất link public qua Cloudflare Tunnel (`cloudflared tunnel --url http://localhost:8501`).

### 3.2. Thực thi Live Chat & Thu thập Transcript (`starter_v0/transcripts/`)

- Chạy phiên hội thoại đa lượt với cấu hình `v3` và lưu log chuẩn tại `starter_v0/transcripts/openrouter_v3_cp5_demo.transcript.json`, bao phủ đầy đủ các tình huống kiểm thử hành vi thực tế:
  - **Lượt 1 (Tra cứu tin tức web):** Hỏi tin tức mới nhất trong tuần về mô hình ngôn ngữ lớn mã nguồn mở -> Agent gọi đúng `lookup(topic="news", timeframe="week")`.
  - **Lượt 2 & 3 (Hỏi lại khi thiếu thông tin & Chuẩn hóa tham số):** Yêu cầu lấy bài đăng X nhưng không nêu tên tài khoản -> Agent gọi `clarify` hỏi lại; khi bổ sung `@karpathy`, Agent tự động cắt ký tự `@` và gọi `timeline(screenname="karpathy")`.
  - **Lượt 4 & 5 (Chốt chặn an toàn Action Guardrail):** Yêu cầu gửi ngay bản tóm tắt lên Telegram -> Agent chặn lại, gọi `clarify` để xin xác nhận trước; chỉ sau khi người dùng xác nhận ở lượt 5 thì Agent mới gọi `send(confirmed=true)`.

### 3.3. Hoàn thiện Báo cáo Nhóm (`report/team/group_report.md`)

- **Phần A (Mục 2 — Giới thiệu Agent):** Hoàn thiện mô tả năng lực hệ thống, hướng dẫn chạy UI, bảng tổng hợp 11 công cụ (10 tool có sẵn + tool mới `calculator`) và 5 câu hỏi mẫu để nhóm khác dùng thử.
- **Phần B (Mục 3–8 — Bằng chứng thực nghiệm):**
  - Tổng hợp bảng tiến hóa `v0` → `v3` (`65%` → `80%` → `85%` → `85%`) và phân tích các ca lỗi (`R11`, `M02`, `R03`, `R12`, `R13`) từ kết quả CP1–CP2 của bạn Nguyễn Đức Hiếu.
  - Kết nối bảng kết quả 10 case `eval_group.json` (`8/10` trên Groq `openai/gpt-oss-120b` và `10/10` trên Ollama `qwen2.5:7b`) cùng bằng chứng unit test `calculator` (`63 passed, 0 failed`) từ phần CP3–CP4 của bạn Nguyễn Mạnh Quân.
  - Điền đầy đủ bảng **B4 (Live Chat Evidence)**, mục **UI trong B5a**, mục **Khó khăn & Cách xử lý (Mục 5)** và **Reflection (Mục 7)**.

---

## 4. Bằng chứng

- **Giao diện & Cấu hình UI:**
  - `starter_v0/app.py`
  - `starter_v0/requirements.txt`
- **Log Hội thoại Live Chat (Transcript JSON):**
  - `starter_v0/transcripts/openrouter_v3_cp5_demo.transcript.json`
- **Báo cáo & Thông tin Nhóm:**
  - `report/team/group_report.md` (Hoàn thiện đầy đủ Phần A và Phần B)
  - `report/team/2A202603912_LeDanhGiang.md` (Báo cáo cá nhân)
  - `TEAM.md` (Cập nhật phân công thành viên)
- **Công cụ AI đã sử dụng:**
  - Gemini: Hỗ trợ rà soát cấu trúc Streamlit UI, đối chiếu tính nhất quán số liệu giữa các file run JSON/transcript và chuẩn hóa định dạng Markdown cho báo cáo.
- **Cách tự kiểm tra kết quả:**
  - Chạy `pytest` trong `starter_v0/` để đảm bảo việc thêm UI không ảnh hưởng tới 63 unit/contract tests đã pass.
  - Chạy `streamlit run app.py` kiểm tra giao diện phản hồi và ghi nhận file `.transcript.json` hợp lệ.

---

## 5. Tự đánh giá

| Tiêu chí | Điểm tự đánh giá | Minh chứng |
|---|:---:|---|
| **C6 — Live chat & UI dùng thử (CP5)** | **9 / 10** | UI Streamlit chạy ổn định, hiển thị rõ tool calls và hash artifact; có đầy đủ transcript hội thoại đa lượt kiểm chứng `lookup`, `clarify`, `timeline` và rào chắn xác nhận `send`. |
| **C7 & C8 — Báo cáo nhóm & Báo cáo cá nhân** | **18 / 20** | Báo cáo nhóm hoàn thiện đầy đủ cả Phần A và Phần B theo đúng template gốc, mọi bảng số liệu đều dẫn chiếu trực tiếp tới file run JSON, transcript và kết quả `pytest` thật của nhóm. |
| **Phối hợp nhóm & Đồng bộ** | **Tốt** | Khớp nối liền mạch kết quả CP1–CP2 (Hiếu) và CP3–CP4 (Quân) thành bộ hồ sơ nộp bài thống nhất. |
