# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: `HH`
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

Local: http://localhost:8501. Chưa có link public cố định; mở phiên bằng `cloudflared tunnel --url http://localhost:8501` khi demo.

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
| `calculator` | Tính số học bằng AST, giữ chính xác số nguyên và giới hạn độ phức tạp; không thay thế thư viện tài chính thập phân | **có** |

### A3. Câu hỏi mẫu để thử

1. **Tính toán số học (`calculator`):** *"Nếu ngân sách nghiên cứu là 120 triệu, tăng thêm 15% rồi chia đều cho 4 quý thì mỗi quý có bao nhiêu?"*
2. **Tìm kiếm tin tức thời sự (`lookup`):** *"Tìm tin tức công nghệ Việt Nam mới nhất trong ngày hôm nay."*
3. **Theo dõi mạng xã hội (`timeline` vs `social_search`):** *"Xem tài khoản @OpenAI vừa đăng gì mới trên X?"*
4. **Hỏi lại khi thiếu thông tin (`clarify` -> `fetch`):** *"Tóm tắt giúp mình nội dung bài báo ở đường link này với."* (Không đưa link ở lượt 1 để kiểm tra Agent hỏi lại).
5. **Chốt chặn xác nhận trước khi gửi (`clarify` -> `send`):** *"Gửi bản tin tóm tắt này lên kênh Telegram ngay giúp mình."*

## 3. Giải pháp

- **Cải tiến `starter_v0/artifacts/system_prompt.md` (v1 → v3):**
  - **v1:** Xóa bỏ các chỉ dẫn xấu cố ý trong bản starter (ép đoán tham số khi thiếu thông tin, tự ý gửi tin nhắn không cần xác nhận). Thiết lập quy tắc bắt buộc gọi `clarify` khi thiếu thực thể (URL, tên tài khoản, biểu thức) và phải xin xác nhận trước khi gọi `send`.
  - **v2 (chỉ sửa tools.yaml, giữ prompt v1):** Làm rõ mô tả định tuyến giữa các công cụ dễ nhầm lẫn (`timeline` cho tài khoản cụ thể vs `social_search` cho từ khóa mạng xã hội vs `lookup` cho tin tức/web) và quy ước chuẩn hóa tham số đầu vào.
  - **v3:** Gỡ bỏ ràng buộc chỉ chọn 1 công cụ mỗi lượt, cho phép định tuyến nhiều nguồn dữ liệu. Tool `calculator` được thêm sau chuỗi base v0–v3; snapshot `v3-calculator` lưu bản group cũ.
- **Cải tiến `starter_v0/artifacts/tools.yaml`:**
  - Viết lại trường `description` của từng tool theo cấu trúc rõ ràng: công cụ làm gì, **khi nào dùng** và **khi nào không dùng**.
  - Đặc tả chặt chẽ quy ước tham số: `screenname` của `timeline` phải bỏ ký tự `@` ở đầu; `lookup` dùng `topic="news"` cho tin tức thời sự kèm `timeframe` (`day`, `week`, `month`, `year`); `send` chỉ được đặt `confirmed=true` sau khi người dùng đã đồng ý tường minh.
- **Tool mới nhóm viết (`calculator` — `starter_v0/tools/calculator/`):**
  - **Làm gì:** Thực hiện các phép tính số học và tài chính (`+`, `-`, `*`, `/`, `**`, ngoặc đơn) thông qua cây cú pháp trừu tượng `ast` của Python, không dùng `eval()`, chỉ cho phép cú pháp số học và giới hạn độ phức tạp, đồng thời bắt toàn bộ ngoại lệ (`ZeroDivisionError`, `ValueError`, `SyntaxError`) để trả về dict lỗi chuẩn qua hàm `err()`.
  - **Khi nào agent nên gọi:** Khi người dùng yêu cầu tính toán con số, tỷ lệ phần trăm, chi phí hoặc biểu thức toán học mà các công cụ tìm kiếm văn bản không xử lý chính xác được.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Cả 4 run trên provider `groq` (`openai/gpt-oss-120b`) đều đạt `provider_error_cases == 0` và `measured_cases == 20/20`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Chạy baseline nguyên bản để đo tỷ lệ lỗi ban đầu và phân loại các ca FAIL | — | 65.0% (13/20) | `runs/v0_B_base_groq_20261110T182244730565.json` |
| v1 | `system_prompt.md` | Bỏ chỉ dẫn đoán mò/gửi thẳng của starter; bắt buộc gọi `clarify` khi thiếu thông tin và xác nhận trước khi `send` sẽ giảm lỗi `missing_info` và `wrong_boundary` | 65.0% (13/20) | 80.0% (16/20) | `runs/v1_B_base_groq_20261110T182835864967.json` |
| v2 | `tools.yaml` | Làm rõ ranh giới chọn tool (`timeline` vs `social_search` vs `lookup`) và quy ước định dạng tham số (`screenname` không `@`, `topic="news"`, `timeframe`) sẽ tăng độ chính xác arguments | 80.0% (16/20) | 85.0% (17/20) | `runs/v2_B_base_groq_20261110T183811591909.json` |
| v3 | `system_prompt.md` | Bỏ ép buộc chỉ gọi một tool đơn lẻ, cải thiện định tuyến yêu cầu nhiều nguồn dữ liệu | 85.0% (17/20) | 85.0% (17/20) | `runs/v3_B_base_groq_20261110T184556678670.json` |
| v4-integration (base) | Bản tích hợp CP1–CP5 | Kiểm tra tương thích sau sửa calculator, prompt và case xác nhận | 85% | 85.0% (17/20) | `runs/v4-integration_B_base_groq_20261111T111423438575.json` |
| v4-integration (group) | Bản tích hợp CP1–CP5 | Kiểm tra tương thích sau sửa calculator, prompt và case xác nhận | 80% | 90.0% (9/10) | `runs/v4-integration_B_group_groq_20261111T110724190757.json` |

Bản tích hợp đo đủ base 20 case và group 10 case, không lỗi provider. GM03 đã thay đổi để có nội dung bản tin cụ thể, nên chênh lệch group không phải phép so sánh mô hình trên bộ case hoàn toàn giữ nguyên.


### B2. Failure Analysis

Đủ 7 case FAIL của baseline v0; nhãn case và mismatch quan sát được ghi riêng. Bằng chứng: `starter_v0/analysis/v0_failures.csv`.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| `R01` (v0) | `wrong_tool`; quan sát `wrong_arg_value` | `[{"name":"timeline","args":{"limit":1,"screenname":"SamAltman"}}]` | screenname: expected 'sama', got 'SamAltman' | Chuẩn hóa handle; PASS từ v1 |
| `R03` (v0) | `wrong_tool`; quan sát `wrong_arg_value` | `[{"name":"lookup","args":{"max_results":5,"query":"AI news today","timeframe":"day","topic":"news"}}]` | query: expected 'AI', got 'AI news today' | Chuẩn hóa query; review exact-match; chưa đạt ở v3 |
| `R10` (v0) | `missing_info`; quan sát `missing_tool_call` | `[{"name":"timeline","args":{"limit":5,"screenname":"sama"}}]` | missing tool call clarify; extra tool call timeline | Hỏi lại handle; PASS từ v1 |
| `R11` (v0) | `missing_info`; quan sát `missing_tool_call` | `[{"name":"lookup","args":{"max_results":3,"query":"OpenAI GPT-4 Turbo announcement","timeframe":"week","topic":"news"}}]` | missing tool call clarify; extra tool call lookup | Hỏi lại URL, không đoán nguồn; PASS từ v1 |
| `R12` (v0) | `wrong_boundary`; quan sát `missing_tool_call` | `[{"name":"lookup","args":{"max_results":5,"query":"latest tech news November 2026","timeframe":"day","topic":"news"}}]` | missing tool call clarify; extra tool call lookup | Xác nhận đúng nội dung; review response_type; chưa đạt ở v3 |
| `R13` (v0) | `wrong_tool`; quan sát `wrong_arg_value` | `[{"name":"lookup","args":{"max_results":10,"query":"AI news today","timeframe":"day","topic":"news"}}]` | query: expected 'AI', got 'AI news today'; missing tool call social_search | Gọi đủ lookup và social_search; chưa đạt ở v3 |
| `M02` (v0) | `wrong_arg_value`; quan sát `wrong_arg_value` | `[{"name":"lookup","args":{"max_results":5,"query":"robotics news","timeframe":"day","topic":"news"}}]` | query: expected 'robotics', got 'robotics news' | Giữ timeframe và cập nhật query; PASS từ v2 |

### B3. Team Eval Cases

Bản hiện hành có đúng 5 single + 5 multi turn; run `starter_v0/runs/v4-integration_B_group_groq_20261111T110724190757.json` đạt 9/10. Điểm eval chấm lựa chọn tool và arguments, không chứng minh mọi tool thực thi thành công.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| `G01_calculator_growth` | Kiểm tra model nhận diện phép tính tăng trưởng số học và định tuyến chính xác tới tool mới calculator | `{"tool_calls":[{"name":"calculator","args":{"expression":"120 * 1.15"}}]}` | PASS |
| `G02_calculator_budget_division` | Kiểm tra model định tuyến phép tính chia ngân sách vào tool mới calculator | `{"tool_calls":[{"name":"calculator","args":{"expression":"1000 / 4"}}]}` | PASS |
| `G03_social_search_ai_agents` | Kiểm tra tìm kiếm từ khóa thảo luận mạng xã hội gọi social_search thay vì timeline | `{"tool_calls":[{"name":"social_search","args":{"query":"AI Agent"}}]}` | PASS |
| `G04_web_news_vietnam_tech` | Kiểm tra tìm tin tức web đặt đúng topic=news và timeframe=day | `{"tool_calls":[{"name":"lookup","args":{"query":"công nghệ Việt Nam","topic":"news","timeframe":"day"}}]}` | FAIL: query: expected 'công nghệ Việt Nam', got 'tin công nghệ Việt Nam' |
| `G05_out_of_scope_greeting` | Kiểm tra câu chào hỏi xã giao thông thường không được gọi bất kỳ công cụ nào | `{"no_tool":true}` | PASS |
| `GM01_clarify_then_calculate` | Đa lượt: sau khi được hỏi lại, user cung cấp biểu thức thì agent phải gọi calculator | `{"tool_calls":[{"name":"calculator","args":{"expression":"(250 + 150) / 4"}}]}` | PASS |
| `GM02_clarify_missing_url_then_fetch` | Đa lượt: sau khi hỏi xin link URL, user gửi link thì agent gọi đúng fetch với url đó | `{"tool_calls":[{"name":"fetch","args":{"url":"https://techcrunch.com/2026/market-report"}}]}` | PASS |
| `GM03_confirm_before_send_telegram` | Đa lượt: chỉ sau khi user đã xác nhận đồng ý thì agent mới được gọi send với confirmed=true | `{"tool_calls":[{"name":"send","args":{"text":"Bản tin nội bộ: Ngân sách nghiên cứu quý này là 120 triệu đồng.","confirmed":true}}]}` | PASS |
| `GM04_topic_carryover_news` | Đa lượt: kế thừa mốc thời gian timeframe=day và topic=news khi đổi chủ đề sang xe điện | `{"tool_calls":[{"name":"lookup","args":{"query":"xe điện","topic":"news","timeframe":"day"}}]}` | PASS |
| `GM05_switch_from_social_to_web` | Đa lượt: nhận biết chuyển đổi ngữ cảnh từ mạng xã hội sang tra cứu tin tức web | `{"tool_calls":[{"name":"lookup","args":{"query":"VinFast","topic":"news","timeframe":"day"}}]}` | PASS |

Lỗi tool trong run này: GM03_confirm_before_send_telegram / send: RuntimeError. Chưa có cấu hình Telegram, không khẳng định đã gửi tin. Run group v3 cũ được giữ nguyên trong runs, khác bộ GM03 hiện tại.

### B4. Live Chat Evidence

Transcript thật từ `chat.py`, provider Groq, model `openai/gpt-oss-120b`: `starter_v0/transcripts/v4-integration_groq_20261111T111623117923.transcript.json`. Có model, hash, rounds và kết quả tool gốc.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Tính giúp tôi 120 * 1.15 / 4. | `[{"name":"calculator","args":{"expression":"120 * 1.15 / 4"}}]` | `v4-integration+p7ae25695d3f2+t19acd1e40905` | answered |
| 2 | Lấy bài đăng gần nhất của tài khoản X này giúp tôi. | `[{"name":"clarify","args":{"question":"Bạn có thể cho tôi tên người dùng (username) của tài khoản X mà bạn muốn lấy bài đăng gần nhất không? Vui lòng cung cấp tên người dùng (không có dấu @).","response_type":"text"}}]` | `v4-integration+p7ae25695d3f2+t19acd1e40905` | waiting_for_user |
| 3 | Tài khoản @karpathy, chỉ lấy 1 bài gần nhất. | `[{"name":"timeline","args":{"limit":1,"screenname":"karpathy"}}]` | `v4-integration+p7ae25695d3f2+t19acd1e40905` | answered |
| 4 | Đăng nguyên văn nội dung này lên Telegram giúp tôi: Bản tin thử: ngân sách nghiên cứu là 120 triệu đồng. | `[{"name":"clarify","args":{"question":"Bạn có chắc muốn gửi tin nhắn sau lên Telegram không?\n\nBản tin thử: ngân sách nghiên cứu là 120 triệu đồng","response_type":"yes_no"}}]` | `v4-integration+p7ae25695d3f2+t19acd1e40905` | waiting_for_user |

Transcript OpenRouter cũ được đánh dấu `unverified_legacy_summary`, không dùng làm bằng chứng đo hoặc gửi thành công. Phiên kiểm tra hiện tại dừng ở yêu cầu xác nhận, không gửi tin Telegram thật.

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới calculator | `starter_v0/tools/calculator/tool.py`, `TOOL.md`, registry/YAML | Số nguyên lớn được giữ nguyên, cú pháp số học có kiểm soát | Từ chối boolean, input sai kiểu, kết quả vô hạn và biểu thức quá lớn; phần trăm viết thành tỷ lệ |
| Unit test tool mới và tích hợp | `starter_v0/tests/test_tools_todo.py`, `test_integration.py`, `starter_v0/analysis/pytest.txt` | 85 passed, 14 skipped; có test hồi quy calculator và Streamlit AppTest | 14 stub tool có sẵn còn skip; không tuyên bố hoàn thành bonus toàn suite |
| UI | `starter_v0/app.py`, `ui_runtime.py`, `requirements.txt` | Dùng vòng lặp chat thật, chọn Groq/model, hiển thị lỗi tool, lưu và tải transcript theo phiên riêng | Đổi cấu hình tạo phiên mới; thiếu link public cố định |

Tool mới có 3 test bắt buộc, thêm test hồi quy cho sai số nguyên lớn, kiểu dữ liệu, phép dư và giới hạn tài nguyên. Unit test bắt lỗi thực thi calculator mà eval routing/arguments không tự chấm. AppTest chạy offline với fake provider, không được dùng thay cho live transcript.


### B5. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | Run Ollama lịch sử, xem B7 | Có thử một model local | Chưa đủ điều kiện bonus; khác hash bản hiện tại |
| Hơn 3 tool mới (≥ 4) | — | — | — |
| `send` gửi thật lên Telegram sau xác nhận | — | — | — |
| Test challenge (0 skipped / regression test) | — | — | — |

### B7. Small Local Model Challenge (bonus)

Có run lịch sử bằng `qwen2.5:7b` trong `starter_v0/runs/`. Group Ollama đạt 10/10 theo bộ chấm nhưng hash khác artifact hiện hành; GM03 tạo nội dung chưa có trong hội thoại và tool gửi trả lỗi thiếu cấu hình Telegram. Không coi đây là bằng chứng gửi thành công hoặc so sánh cùng artifact với Groq.

| Version | Model (provider) | Prompt/Tools | Suite | case_accuracy | Run File |
|---|---|---|---|---:|---|
| v3 (Cloud Base) | openai/gpt-oss-120b (groq) | Snapshot v3 | base | 85% | `runs/v3_B_base_groq_20261110T184556678670.json` |
| v3 (Cloud Group) | openai/gpt-oss-120b (groq) | Snapshot v3-calculator | group cũ | 80% | `runs/v3_B_group_groq_20261110T193553495897.json` |
| v3 (Local) | qwen2.5:7b (ollama) | Artifact lịch sử, khác bản hiện hành | group cũ | 100% theo bộ chấm | `runs/v3_B_group_ollama_20261110T190101423006.json` |

Chưa đủ điều kiện bonus: mới có một model local, chưa đủ hai vòng tối ưu local và kiểm tra ngược cloud theo README. Các run chỉ là dữ liệu tham khảo.


## 5. Khó khăn và cách xử lý

- **Tích hợp CP1–CP5:** Giữ lịch sử cả ba thành viên, giải quyết xung đột registry/schema/prompt/version log và giữ snapshot cũ. Sửa ba import không tồn tại trong UI, dùng vòng lặp chat thật; bổ sung log và test cho lỗi provider sau khi tool đã chạy.

- **Giới hạn Quota & Rate Limit của Provider:**
  - *Khó khăn:* Khi chạy eval liên tục 20 case, Gemini gặp giới hạn quota và các provider dễ trả lỗi HTTP 429 làm sai lệch kết quả đo (`provider_error_cases > 0`).
  - *Cách xử lý:* Thành viên Nguyễn Đức Hiếu đã tích hợp thêm `starter_v0/providers/groq_provider.py` sử dụng thống nhất model `openai/gpt-oss-120b`, đồng thời viết script `starter_v0/scripts/run_paced_eval.py` có cơ chế giãn cách thời gian giữa các request (`--min-interval 20` trong lần kiểm tra tích hợp) và retry có giới hạn. Nhờ đó toàn bộ các bản chạy `v0`–`v3` và `group` đều đạt `provider_error_cases == 0`.
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
