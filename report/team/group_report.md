# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: `K5-L3B-DAY03-HH`
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
  - Nguyễn Đức Hiếu (`2A202603772`) — CP1 & CP2 (Setup, Provider Groq, Baseline v0 & Tối ưu v1–v3)
  - Nguyễn Mạnh Quân (`2A202603776`) — CP3 & CP4 (Tool mới `calculator`, Unit tests, 10 case `eval_group.json`)
  - Lê Danh Giang (`2A202603912`) — CP5 (Streamlit Demo UI, Live Chat Transcript, Tổng hợp Báo cáo nhóm & cá nhân)
- Provider/model dùng cho v0–v3: `groq` (`openai/gpt-oss-120b`) — đối chiếu bổ sung trên `ollama` (`qwen2.5:7b`)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research Agent hỗ trợ tìm kiếm tin tức/web theo từ khóa (`lookup`), theo dõi bài đăng mạng xã hội theo tài khoản (`timeline`) hoặc chủ đề (`social_search`), đọc nội dung URL (`fetch`), tra cứu quy định nội bộ (`policy`), tìm bài báo arXiv (`papers`, `paper_text`), tính toán biểu thức số học an toàn (`calculator`), tổng hợp digest (`format`) và gửi thông báo lên Telegram (`send`) sau khi người dùng đã xác nhận.

**Cách chạy UI:**

- Lệnh chạy UI từ thư mục `starter_v0/`:
  ```bash
  streamlit run app.py
  ```
- Dependency đã thêm vào `starter_v0/requirements.txt`: `streamlit>=1.32.0`

**Link dùng thử (deploy):**



### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| `clarify` | Hỏi lại người dùng khi thiếu thông tin bắt buộc hoặc xin xác nhận trước khi hành động | không |
| `lookup` | Tìm kiếm thông tin chung (`topic="general"`) hoặc tin tức thời sự (`topic="news"`) trên web kèm `timeframe` | không |
| `fetch` | Đọc và trích xuất nội dung chi tiết từ một đường dẫn URL cụ thể | không |
| `timeline` | Lấy các bài đăng gần đây của một tài khoản X/Twitter (`screenname` không có `@`) | không |
| `social_search` | Tìm kiếm bài đăng mạng xã hội theo từ khóa (`search_type="Latest"` hoặc `"Top"`) | không |
| `format` | Tổng hợp và trình bày danh sách các mục thông tin thành bản tin Markdown digest | không |
| `send` | Gửi nội dung bản tin lên kênh Telegram (chỉ thực thi khi `confirmed=true`) | không |
| `policy` | Tra cứu tài liệu quy định nội bộ của công ty trong `company_policy/*.md` | không |
| `papers` | Tìm kiếm bài báo khoa học trên kho dữ liệu arXiv | không |
| `paper_text` | Tải PDF bài báo arXiv và trích xuất văn bản phục vụ đọc sâu | không |
| `calculator` | Tính toán biểu thức số học/tài chính chính xác và an toàn bằng bộ phân tích cú pháp `ast` | **có** |

### A3. Câu hỏi mẫu để thử

1. **Tính toán số học (`calculator`):** *"Nếu ngân sách nghiên cứu là 120 triệu, tăng thêm 15% rồi chia đều cho 4 quý thì mỗi quý có bao nhiêu?"*
2. **Tìm kiếm tin tức thời sự (`lookup`):** *"Tìm tin tức công nghệ Việt Nam mới nhất trong ngày hôm nay."*
3. **Theo dõi mạng xã hội (`timeline` vs `social_search`):** *"Xem tài khoản @OpenAI vừa đăng gì mới trên X?"*
4. **Hỏi lại khi thiếu thông tin (`clarify` -> `fetch`):** *"Tóm tắt giúp mình nội dung bài báo ở đường link này với."* (Không đưa link ở lượt 1 để kiểm tra Agent hỏi lại).
5. **Chốt chặn xác nhận trước khi gửi (`clarify` -> `send`):** *"Gửi bản tin tóm tắt này lên kênh Telegram ngay giúp mình."*

## 3. Giải pháp

- **Cải tiến `starter_v0/artifacts/system_prompt.md` (v1 → v3):**
  - **v1:** Xóa bỏ các chỉ dẫn xấu cố ý trong bản starter (ép đoán tham số khi thiếu thông tin, tự ý gửi tin nhắn không cần xác nhận). Thiết lập quy tắc bắt buộc gọi `clarify` khi thiếu thực thể (URL, tên tài khoản, biểu thức) và phải xin xác nhận trước khi gọi `send`.
  - **v2:** Bổ sung quy tắc định tuyến rõ ràng giữa các công cụ dễ nhầm lẫn (`timeline` cho tài khoản cụ thể vs `social_search` cho từ khóa mạng xã hội vs `lookup` cho tin tức/web) và quy ước chuẩn hóa tham số đầu vào.
  - **v3:** Gỡ bỏ ràng buộc cứng nhắc chỉ chọn 1 công cụ duy nhất mỗi lượt, cho phép định tuyến linh hoạt nhiều nguồn dữ liệu và tích hợp quy tắc gọi tool mới `calculator`.
- **Cải tiến `starter_v0/artifacts/tools.yaml`:**
  - Viết lại trường `description` của từng tool theo cấu trúc rõ ràng: công cụ làm gì, **khi nào dùng** và **khi nào không dùng**.
  - Đặc tả chặt chẽ quy ước tham số: `screenname` của `timeline` phải bỏ ký tự `@` ở đầu; `lookup` dùng `topic="news"` cho tin tức thời sự kèm `timeframe` (`day`, `week`, `month`, `year`); `send` chỉ được đặt `confirmed=true` sau khi người dùng đã đồng ý tường minh.
- **Tool mới nhóm viết (`calculator` — `starter_v0/tools/calculator/`):**
  - **Làm gì:** Thực hiện các phép tính số học và tài chính (`+`, `-`, `*`, `/`, `**`, ngoặc đơn) thông qua cây cú pháp trừu tượng `ast` của Python, tuyệt đối không dùng `eval()` để đảm bảo an toàn bảo mật, đồng thời bắt toàn bộ ngoại lệ (`ZeroDivisionError`, `ValueError`, `SyntaxError`) để trả về dict lỗi chuẩn qua hàm `err()`.
  - **Khi nào agent nên gọi:** Khi người dùng yêu cầu tính toán con số, tỷ lệ phần trăm, chi phí hoặc biểu thức toán học mà các công cụ tìm kiếm văn bản không xử lý chính xác được.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Cả 4 run trên provider `groq` (`openai/gpt-oss-120b`) đều đạt `provider_error_cases == 0` và `measured_cases == 20/20`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Chạy baseline nguyên bản để đo tỷ lệ lỗi ban đầu và phân loại các ca FAIL | — | 65.0% (13/20) | `runs/v0_B_base_groq_20261110T182244730565.json` |
| v1 | `system_prompt.md` | Bỏ chỉ dẫn đoán mò/gửi thẳng của starter; bắt buộc gọi `clarify` khi thiếu thông tin và xác nhận trước khi `send` sẽ giảm lỗi `missing_info` và `wrong_boundary` | 65.0% (13/20) | 80.0% (16/20) | `runs/v1_B_base_groq_20261110T182835864967.json` |
| v2 | `tools.yaml` (+ đồng bộ `system_prompt.md`) | Làm rõ ranh giới chọn tool (`timeline` vs `social_search` vs `lookup`) và quy ước định dạng tham số (`screenname` không `@`, `topic="news"`, `timeframe`) sẽ tăng độ chính xác arguments | 80.0% (16/20) | 85.0% (17/20) | `runs/v2_B_base_groq_20261110T183811591909.json` |
| v3 | `system_prompt.md` | Bỏ ép buộc chỉ gọi một tool đơn lẻ, cải thiện định tuyến yêu cầu nhiều nguồn dữ liệu | 85.0% (17/20) | 85.0% (17/20) | `runs/v3_B_base_groq_20261110T184556678670.json` |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong các file run JSON và bảng tổng hợp `starter_v0/analysis/v3_failures.csv`.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| `R11` (v0) | `missing_info` | Tự đoán URL/tham số để gọi tool tra cứu thay vì hỏi lại | Starter prompt ép agent tự đoán khi thiếu thông tin thay vì gọi `clarify` | Sửa `system_prompt.md` ở `v1`: bắt buộc gọi `clarify` khi thiếu URL hoặc handle (Đã PASS từ `v1`) |
| `M02` (v0–v1) | `wrong_arg_value` | Gọi `lookup` nhưng truyền sai `topic` / `timeframe` hoặc nhiễu từ khóa ở lượt sau | Mô tả tham số trong `tools.yaml` chưa quy định rõ khi nào dùng `topic="news"` và cách giữ ngữ cảnh thời gian | Cập nhật mô tả argument trong `tools.yaml` ở `v2` (Đã PASS từ `v2`) |
| `R03` (v0–v3) | `wrong_arg_value` | `lookup(query=..., topic="news", ...)` | Chuỗi `query` model sinh ra khác biệt nhỏ về từ khóa so với chuỗi kỳ vọng cứng trong bộ test base | Cần bổ sung hướng dẫn trích xuất từ khóa tối giản (bỏ từ đệm "tin tức", "mới nhất") trong `tools.yaml` |
| `R12` (v0–v3) | `wrong_boundary` | Gọi `clarify` để hỏi xác nhận/nội dung thay vì khớp hoàn toàn mẫu tool call kỳ vọng | Cách đặt câu hỏi xác nhận trước khi `send` chưa khớp tuyệt đối với kịch bản chấm tự động của case `R12` | Chuẩn hóa mẫu hành vi xác nhận 2 bước cho `send` và kết hợp review thủ công cho các ca boundary |
| `R13` (v0–v3) | `wrong_tool` | Chỉ gọi một phần chuỗi tool, thiếu `social_search` | Câu hỏi yêu cầu kết hợp nhiều nguồn thông tin nhưng model chưa gọi đủ tổ hợp tool kỳ vọng | Tinh chỉnh thêm chỉ dẫn multi-tool routing trong `system_prompt.md` |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn `G01`–`G05` + 5 multi turn `GM01`–`GM05`), đánh giá trên `runs/v3_B_group_groq_20261110T193553495897.json` (đạt **8/10 PASS — 80%** trên Groq và **10/10 PASS — 100%** trên Ollama `qwen2.5:7b` tại `runs/v3_B_group_ollama_20261110T190101423006.json`).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| `G01` | Định tuyến đơn lượt vào tool mới `calculator` với phép tính cơ bản | Gọi `calculator` với biểu thức số học tương ứng | **PASS** |
| `G02` | Định tuyến đơn lượt vào `calculator` cho bài toán tính tỷ lệ/chi phí thực tế | Gọi `calculator` với biểu thức có ngoặc/phần trăm | **PASS** |
| `G03` | Phân biệt ranh giới giữa `social_search` (tìm theo từ khóa) và `timeline` (tài khoản) | Gọi `social_search` với `search_type` phù hợp | **PASS** |
| `G04` | Trích xuất `query` sạch (`"công nghệ Việt Nam"`) kèm `topic="news"`, `timeframe="day"` (kiểm tra lỗi `R03`) | `lookup(query="công nghệ Việt Nam", topic="news", timeframe="day")` | **FAIL** (Groq giữ chữ `"tin tức công nghệ Việt Nam"` trong query; Ollama PASS) |
| `G05` | Từ chối gọi tool (`no_tool: true`) khi người dùng chỉ chào hỏi/tán gẫu ngoài phạm vi | Không gọi tool nào (`no_tool`) | **PASS** |
| `GM01` | Đa lượt: Lượt 1 thiếu số liệu để tính -> `clarify`; Lượt 2 đủ số liệu -> gọi `calculator` | Lượt 1: `clarify` -> Lượt 2: `calculator` | **PASS** |
| `GM02` | Đa lượt: Lượt 1 yêu cầu đọc bài nhưng thiếu URL -> `clarify`; Lượt 2 đưa URL -> gọi `fetch` (kiểm tra lỗi `R11`) | Lượt 1: `clarify` -> Lượt 2: `fetch(url=...)` | **PASS** |
| `GM03` | Đa lượt: Kiểm tra chốt chặn xác nhận trước khi gửi Telegram (`confirmed=true`) (kiểm tra lỗi `R12`) | Lượt 1: `clarify` xin xác nhận -> Lượt 2: `send(confirmed=true)` | **FAIL** trên Groq (Model gọi `clarify` hỏi lại nội dung bản tin để không tự bịa message; Ollama PASS) |
| `GM04` | Đa lượt: Kế thừa ngữ cảnh `topic="news"` và `timeframe="day"` khi chuyển chủ đề sang xe điện (kiểm tra lỗi `M02`) | Lượt 2 gọi `lookup` giữ nguyên `topic="news", timeframe="day"` | **PASS** |
| `GM05` | Đa lượt: Chuyển đổi linh hoạt nguồn dữ liệu từ tra cứu mạng xã hội X sang tìm kiếm báo chí web | Lượt 1: `timeline`/`social_search` -> Lượt 2: `lookup` | **PASS** |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/openrouter_v3_cp5_demo.transcript.json` (và phiên chạy thực tế qua `chat.py` / `app.py`).

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | *"Tìm tin tức mới nhất trong tuần này về mô hình ngôn ngữ lớn (LLM) mã nguồn mở."* | `lookup(query="open source large language models LLM release", topic="news", timeframe="week")` | `v3` | Agent chọn đúng `lookup` với `topic="news"` và `timeframe="week"`, trả về bản tóm tắt tin tức |
| 2 | *"Lấy giúp mình các bài đăng gần đây trên X của tài khoản đó nhé."* | `clarify(question="Bạn muốn lấy bài đăng từ tài khoản X (Twitter) nào?...")` | `v3` | Phát hiện thiếu tên tài khoản, không đoán mò mà gọi `clarify` để hỏi người dùng |
| 3 | *"Tài khoản @karpathy nhé."* | `timeline(screenname="karpathy")` | `v3` | Tự động loại bỏ ký tự `@` ở đầu và gọi đúng tool `timeline` để lấy bài đăng |
| 4 | *"Gửi bản tóm tắt các bài đăng của Karpathy lên kênh Telegram luôn giúp mình."* | `clarify(question="Bạn có chắc chắn muốn gửi bản tóm tắt này lên kênh Telegram chính thức không?...")` | `v3` | Chặn hành động gửi ngay, gọi `clarify` yêu cầu xác nhận trước khi phát tán ra kênh ngoài |
| 5 | *"Xác nhận, gửi đi bạn."* | `send(text="...", confirmed=True)` | `v3` | Sau khi có xác nhận tường minh từ người dùng, Agent mới gọi `send` với `confirmed=True` |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/calculator/`) | `starter_v0/tools/calculator/tool.py`, `starter_v0/tools/calculator/TOOL.md` | Tính toán chính xác số nguyên, số thực, lũy thừa, ngoặc đơn; tích hợp mượt vào `tools/__init__.py` và `tools.yaml` | Dùng `ast` node visitor thay vì `eval()` để chặn 100% lỗi thực thi mã tùy ý; bắt ngoại lệ trả về `err()` dict |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py`, `starter_v0/analysis/pytest.txt` (**63 passed, 0 failed**) | Bao phủ đầy đủ 3 kịch bản: `test_my_new_tool_happy_path`, `test_my_new_tool_bad_input_from_model`, `test_my_new_tool_failure_returns_error_dict` | Chạy hoàn toàn offline, đảm bảo hàm không bao giờ raise unhandled exception làm sập vòng lặp agent |
| UI (lệnh chạy + link dùng thử) | `starter_v0/app.py`, `starter_v0/requirements.txt` | Giao diện Streamlit hiển thị trực tiếp `prompt_hash`, `tools_hash`, lịch sử chat, JSON `tool_calls` và tự động lưu file transcript | Kiểm soát lỗi khi gọi provider và lưu log từng lượt vào `starter_v0/transcripts/` |

- **Tool unit tests:** Đã viết **3 unit tests** cho tool `calculator` (tổng toàn bộ suite đạt **63 passed, 0 failed**).
- **Ví dụ lỗi mà unit test bắt được nhưng eval không bắt được:** Trong `run_eval.py`, bộ chấm chỉ kiểm tra xem model có gọi đúng tên tool `calculator` và truyền string `expression` hợp lệ hay không. Nếu người dùng hoặc model truyền biểu thức chia cho 0 (ví dụ `100 / 0`) hoặc chuỗi rỗng `""`, eval routing vẫn có thể chấm PASS nhưng nếu code tool không bắt `ZeroDivisionError` / `SyntaxError` thì ứng dụng thực tế sẽ bị crash. Unit test `test_my_new_tool_failure_returns_error_dict` và `test_my_new_tool_bad_input_from_model` kiểm tra trực tiếp việc trả về dict lỗi `{tool: "calculate", error: ...}` an toàn.

### B5. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | `starter_v0/runs/v3_B_group_ollama_20261110T190101423006.json` (xem mục B7) | Chạy đối chiếu thành công bộ 10 case `eval_group.json` với model local `qwen2.5:7b` qua Ollama đạt **10/10 PASS (100%)** | Chạy hoàn toàn local không tốn API quota; cần lưu ý tốc độ suy luận phụ thuộc phần cứng máy cá nhân |
| Hơn 3 tool mới (≥ 4) | — | — | — |
| `send` gửi thật lên Telegram sau xác nhận | — | — | — |
| Test challenge (0 skipped / regression test) | — | — | — |

### B7. Small Local Model Challenge (bonus)

Nhóm thực hiện chạy đối chiếu bản cấu hình `v3` giữa Cloud Provider (`groq` — `openai/gpt-oss-120b`) và Local Model qua Ollama (`qwen2.5:7b`) trên bộ `eval_group.json`:

| Version | Model (provider) | Prompt/Tools | Suite | case_accuracy | Run File |
|---|---|---|---|---:|---|
| v3 (Cloud Base) | `openai/gpt-oss-120b` (`groq`) | v3 | `base` (20 cases) | 85.0% (17/20) | `runs/v3_B_base_groq_20261110T184556678670.json` |
| v3 (Cloud Group) | `openai/gpt-oss-120b` (`groq`) | v3 | `group` (10 cases) | 80.0% (8/10) | `runs/v3_B_group_groq_20261110T193553495897.json` |
| v3-qwen7b (Local) | `qwen2.5:7b` (`ollama`) | v3 | `group` (10 cases) | 100.0% (10/10) | `runs/v3_B_group_ollama_20261110T190101423006.json` |

- **Nhận xét đối chiếu Cloud vs Local (`qwen2.5:7b`):**
  - Nhờ việc làm rõ mô tả tham số trong `tools.yaml` và quy tắc định tuyến ngắn gọn, cấu trúc hóa theo gạch đầu dòng trong `system_prompt.md` ở bản `v3`, model nhỏ `qwen2.5:7b` chạy qua Ollama có thể bám sát schema và đạt `10/10` trên bộ `eval_group.json`.
  - Khi nào chọn model local thay vì cloud: Khi cần bảo mật dữ liệu nội bộ (`company_policy`), không muốn phụ thuộc vào giới hạn rate-limit/quota của API cloud, và tác vụ đã có tool schema được định nghĩa tường minh.

## 5. Khó khăn và cách xử lý

- **Giới hạn Quota & Rate Limit của Provider:**
  - *Khó khăn:* Khi chạy eval liên tục 20 case, Gemini gặp giới hạn quota và các provider dễ trả lỗi HTTP 429 làm sai lệch kết quả đo (`provider_error_cases > 0`).
  - *Cách xử lý:* Thành viên Nguyễn Đức Hiếu đã tích hợp thêm `starter_v0/providers/groq_provider.py` sử dụng thống nhất model `openai/gpt-oss-120b`, đồng thời viết script `starter_v0/scripts/run_paced_eval.py` có cơ chế giãn cách thời gian giữa các request (`--min-interval 5`) và retry có giới hạn. Nhờ đó toàn bộ các bản chạy `v0`–`v3` và `group` đều đạt `provider_error_cases == 0`.
- **Xung đột khi tích hợp nhánh (Git Merge giữa CP1–CP2 và CP3–CP4):**
  - *Khó khăn:* Việc vừa cập nhật `system_prompt.md`/`tools.yaml` ở CP2 vừa đăng ký thêm tool `calculator` ở CP3 dễ gây lệch hash hoặc hỏng contract test.
  - *Cách xử lý:* Kế thừa trực tiếp trên nền `v3` của CP2, dùng `pytest starter_v0/tests/test_tool_contract.py` làm chốt chặn kiểm tra đồng bộ trước mỗi lần commit.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân:
- [`report/team/2A202603772_NguyenDucHieu.md`](2A202603772_NguyenDucHieu.md)
- [`report/team/2A202603776_NguyenManhQuan.md`](2A202603776_NguyenManhQuan.md)
- [`report/team/2A202603912_LeDanhGiang.md`](2A202603912_LeDanhGiang.md)

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix nào thuộc `system_prompt.md`?**
  - Các quy tắc điều phối hành vi tổng thể: không tự đoán thông tin thiếu (ưu tiên gọi `clarify`), quy trình 2 bước xin xác nhận trước khi thực thi công cụ có tác động ra ngoài (`send`), và nguyên tắc phối hợp nhiều công cụ theo ngữ cảnh hội thoại.
- **Fix nào thuộc `tools.yaml`?**
  - Các quy ước gắn liền với từng công cụ và định dạng tham số: khi nào chọn `timeline` thay vì `social_search`, quy tắc cắt bỏ ký tự `@` khỏi `screenname`, cách chọn enum `topic="news"` / `timeframe` trong `lookup`, và mô tả điều kiện kích hoạt `calculator`.
- **Failure nào cần review thủ công thay vì chấm tự động?**
  - Các lỗi dạng `R03` / `G04` (câu truy vấn tìm kiếm vẫn đúng ý nghĩa thực tế nhưng dư từ khóa tiếng Việt như *"tin tức"* so với chuỗi exact-match trong đáp án) và lỗi `R12` / `GM03` (model cẩn thận gọi `clarify` để hỏi lại nội dung tin nhắn trước khi gửi nhằm tuân thủ nguyên tắc *"Never invent the message"*).
- **Nếu có thêm một vòng (`v4`), nhóm sẽ thử giả thuyết nào?**
  - Bổ sung 1–2 ví dụ ngắn (few-shot) ngay trong description của `lookup.query` trong `tools.yaml` để hướng dẫn model lược bỏ hoàn toàn các từ chỉ loại hình (*"tin tức"*, *"bài báo"*, *"mới nhất"*) khỏi chuỗi `query` khi đã chuyển thông tin đó sang tham số `topic="news"` và `timeframe`, từ đó giải quyết triệt để ca `R03` và `G04`.

## 8. Tài liệu tham khảo

- Tài liệu hướng dẫn Lab: `README.md`, `CHECKPOINTS.md`, `RUBRIC.md`, `docs/TOOL-SETUP.md`.
- Tệp nhật ký và dữ liệu thực nghiệm của nhóm trong `starter_v0/runs/`, `starter_v0/analysis/` và `starter_v0/artifacts/version_log.csv`.
