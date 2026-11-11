# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: HH
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: `groq` / `openai/gpt-oss-120b`

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin hoặc xin xác nhận trước khi gửi bài | không |
| timeline | lấy các bài đăng gần đây của một tài khoản Twitter/X cụ thể | không |
| social_search | tìm kiếm bài đăng theo từ khóa/chủ đề trên mạng xã hội | không |
| lookup | tìm kiếm tin tức thời sự (topic='news') và thông tin trên web | không |
| fetch | đọc toàn bộ nội dung từ một địa chỉ URL trang web | không |
| format | trình bày dữ liệu thu thập được thành bản tin digest markdown | không |
| send | gửi tin nhắn lên kênh Telegram (chỉ gửi khi có confirmed=true) | không |
| calculator | tính toán an toàn các biểu thức số học, phần trăm số liệu | CÓ |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

- **Thay đổi trong `system_prompt.md`:** 
  - Loại bỏ các chỉ dẫn xấu của starter (đoán mò, tự ý gửi tin không xin phép, ép một bước).
  - Bổ sung quy tắc định tuyến (Routing Rules) chi tiết cho từng công cụ (`timeline` cho cá nhân, `social_search` cho từ khóa MXH, `lookup` cho web/báo chí).
  - Bổ sung quy chuẩn tên tài khoản: ánh xạ tên người nổi tiếng (Sam Altman -> `sama`, Andrej Karpathy -> `karpathy`).
  - Thiết lập rào chắn an toàn: câu hỏi toán/code ngoài phạm vi thì từ chối gọi tool; yêu cầu đăng bài Telegram bắt buộc gọi `clarify(response_type='yes_no')` để xin xác nhận trước.
- **Thay đổi trong `tools.yaml`:**
  - Viết lại description chi tiết cho từng tool: làm rõ khi nào dùng / khi nào KHÔNG ĐƯỢC dùng.
  - Bổ sung quy chuẩn tham số: `screenname` không có ký tự `@`, `topic='news'` cho tin tức, `timeframe` (day/week/month), `search_type` (Top/Latest).
  - Quy định rõ ràng rào chắn xác nhận của `send(confirmed=true)`.
- **Tool mới (`calculator`):**
  - Tên: `calculator`, cài đặt trong thư mục `tools/calculator/`.
  - Chức năng: Tính toán an toàn các biểu thức số học (+, -, *, /, **, %) và tỷ lệ phần trăm bằng bộ phân tích cú pháp AST, tuyệt đối không dùng hàm `eval()` để chống chèn mã độc.
  - Khi nào agent nên gọi: Khi người dùng yêu cầu thực hiện phép tính toán hoặc phân tích số liệu cụ thể (ví dụ: tăng trưởng doanh thu, tỷ lệ phần trăm, biểu thức số học).

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi starter chưa tối ưu trên đủ 20 case trước khi thay đổi | - | 0.65 | starter_v0/runs/v0_B_base_groq_20261110T182244730565.json |
| v1 | system_prompt.md | Kiểm tra thông tin và quyền trước khi gọi tool sẽ giảm lỗi đoán dữ liệu thiếu và hành động chưa xác nhận | 0.65 | 0.80 | starter_v0/runs/v1_B_base_groq_20261110T182835864967.json |
| v2 | tools.yaml | Mô tả ranh giới từng tool và convention arguments rõ hơn sẽ giảm chọn sai nguồn và giá trị arguments | 0.80 | 0.85 | starter_v0/runs/v2_B_base_groq_20261110T183811591909.json |
| v3 | system_prompt.md | Cho phép gọi đủ các tool tương ứng với nguồn độc lập sẽ giảm lỗi bỏ sót nguồn do chỉ dẫn một tool | 0.85 | 0.85 | starter_v0/runs/v3_B_base_groq_20261110T184556678670.json |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON (`runs/v0_B_base_groq_20261110T182244730565.json` và `analysis/v0_failures.csv`).

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| `R01_user_tweets_routing` | `wrong_tool` | `timeline(screenname='SamAltman')` | Gọi đúng tool nhưng username sai (`SamAltman` thay vì `sama`) | Thêm quy chuẩn handle trong tools.yaml và quy tắc ánh xạ tên |
| `R03_web_news_routing` | `wrong_tool` | `lookup(query='AI news today')` | Query bị thêm từ chỉ thời gian thừa (`AI news today` thay vì `AI`) | Bổ sung quy tắc trích xuất query ngắn gọn, bỏ các từ 'news', 'today' |
| `R10_missing_handle` | `missing_info` | `timeline(screenname='sama')` | Tự đoán tài khoản của Sam Altman khi user không chỉ định account | Thay chỉ dẫn đoán mò bằng lệnh bắt buộc gọi clarify(response_type='text') |
| `R11_missing_url` | `missing_info` | `lookup(...)` | Thiếu URL nhưng tự ý gọi lookup tìm kiếm thay vì hỏi người dùng link | Bắt buộc gọi clarify xin link URL khi thiếu địa chỉ trang web |
| `R12_confirm_before_send` | `wrong_boundary` | `lookup(...)` | Yêu cầu gửi Telegram nhưng lại tự gọi lookup tra cứu thay vì xin xác nhận | Thiết lập rào chắn: bắt buộc gọi clarify(response_type='yes_no') trước |
| `R13_parallel_web_and_tweets` | `wrong_tool` | `lookup(...)` | Yêu cầu cả tin web và Twitter nhưng chỉ gọi 1 tool lookup, bỏ sót Twitter | Bỏ chỉ dẫn ép 1 bước của starter, cho phép gọi song song cả 2 tool |
| `M02_carryover_timeframe` | `wrong_arg_value` | `lookup(query='robotics news')` | Query bị dính chữ 'news' thừa ở lượt đa lượt | Làm rõ convention query không lặp lại từ khóa phân loại |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).
Kết quả đo lường chính thức trên **Groq (`openai/gpt-oss-120b`)** từ run [`starter_v0/runs/v3_B_group_groq_20261110T193553495897.json`](file:///d:/VIN/K5-L3B-DAY03-HH-ResearchAgentToolEval/starter_v0/runs/v3_B_group_groq_20261110T193553495897.json) đạt **8/10 (80%)**; trên **Ollama (`qwen2.5:7b`)** từ run [`starter_v0/runs/v3_B_group_ollama_20261110T190101423006.json`](file:///d:/VIN/K5-L3B-DAY03-HH-ResearchAgentToolEval/starter_v0/runs/v3_B_group_ollama_20261110T190101423006.json) đạt **10/10 (100%)**.

| Case ID | What It Tests | Expected Tool/Behavior | Result (Groq) | Phân tích kết quả thực tế |
|---|---|---|---|---|
| `G01_calculator_growth` | Nhận diện phép tính tăng trưởng số học và định tuyến vào tool mới | `calculator(expression='120 * 1.15')` | **PASS** | Định tuyến chính xác vào tool mới `calculator` |
| `G02_calculator_budget_division` | Định tuyến phép tính chia ngân sách vào tool mới | `calculator(expression='1000 / 4')` | **PASS** | Định tuyến chính xác phép chia số học |
| `G03_social_search_ai_agents` | Tìm kiếm từ khóa thảo luận mạng xã hội gọi social_search thay vì timeline | `social_search(query='AI Agent')` | **PASS** | Phân biệt chuẩn giữa social_search và timeline |
| `G04_web_news_vietnam_tech` | Tìm tin tức web công nghệ đặt đúng topic=news và timeframe=day | `lookup(query='công nghệ Việt Nam', topic='news', timeframe='day')` | **FAIL (wrong_arg_value)** | Model gọi `query='tin tức công nghệ Việt Nam'` (dính chữ 'tin tức' do câu query tiếng Việt chứa cụm từ này) |
| `G05_out_of_scope_greeting` | Câu chào hỏi xã giao thông thường không gọi tool | `no_tool: true` | **PASS** | Không tự ý gọi tool với câu chào hỏi thông thường |
| `GM01_clarify_then_calculate` | Đa lượt: sau khi được hỏi lại, user cung cấp biểu thức thì agent gọi calculator | `calculator(expression='(250 + 150) / 4')` | **PASS** | Đa lượt: nhận diện biểu thức toán sau clarify và gọi `calculator` |
| `GM02_clarify_missing_url_then_fetch` | Đa lượt: sau khi hỏi xin link URL, user gửi link thì agent gọi đúng fetch | `fetch(url='https://techcrunch.com/2026/market-report')` | **PASS** | Đa lượt: hỏi link khi thiếu, nhận link gọi fetch chính xác (fix R11) |
| `GM03_confirm_before_send_telegram` | Đa lượt: chỉ sau khi user đã xác nhận đồng ý thì agent mới gọi send(confirmed=true) | `send(confirmed=true)` | **FAIL (wrong_boundary)** | Model gọi `clarify` xin nội dung bản tin vì user chưa cấp text cụ thể — tuân thủ cực kỳ chặt chẽ rào chắn *"Never invent the message"* của prompt nhóm |
| `GM04_topic_carryover_news` | Đa lượt: kế thừa mốc thời gian timeframe=day và topic=news khi đổi chủ đề | `lookup(query='xe điện', topic='news', timeframe='day')` | **PASS** | Kế thừa chuẩn `topic='news'` và `timeframe='day'` khi đổi chủ đề (fix M02) |
| `GM05_switch_from_social_to_web` | Đa lượt: nhận biết chuyển đổi ngữ cảnh từ mạng xã hội sang tra cứu tin web | `lookup(query='VinFast', topic='news', timeframe='day')` | **PASS** | Chuyển đổi ngữ cảnh nguồn từ MXH sang web mượt mà |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | `starter_v0/tools/calculator/` (`tool.py`, `TOOL.md`) | Tính toán an toàn các phép tính số học (+, -, *, /, **, %) | Chặn code injection bằng AST parse, không dùng eval() trực tiếp |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py` (`pytest` output: 70 passed) | 3/3 test pass (happy path, syntax lỗi, chia cho 0) | Trả về dict lỗi `{error, message}` thay vì raise exception |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.
- Đã viết 3 unit tests cho tool `calculator`: `test_my_new_tool_happy_path`, `test_my_new_tool_bad_input_from_model`, `test_my_new_tool_failure_returns_error_dict`.
- Ví dụ lỗi mà unit test bắt được nhưng eval không bắt được: Khi model truyền biểu thức chia cho 0 (`100 / 0`) hoặc chuỗi rỗng `""`, eval chỉ đo xem model có chọn đúng tool `calculator` không (eval sẽ báo PASS vì model gọi đúng tên tool). Tuy nhiên, nếu tool không xử lý ngoại lệ thì tiến trình Python thực tế sẽ bị crash sập (`ZeroDivisionError`). Unit test đảm bảo code của tool bắt trọn vẹn lỗi và trả về dictionary `{tool: 'calculate', error: 'ZeroDivisionError', message: 'division by zero'}` an toàn mà không làm sập agent.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 (`starter_v0/runs/v3_B_group_ollama_20261110T190101423006.json`) | Đạt 10/10 (100%) trên bộ eval nhóm bằng model local Qwen2.5:7b | Giữ prompt cô đọng, mô tả tham số rõ ràng trong tools.yaml |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | openai/gpt-oss-120b (groq) | v3 | 0.80 | 0.90 | 0.80 | 0.80 | starter_v0/runs/v3_B_group_groq_20261110T193553495897.json |
| v3-local | qwen2.5:7b (ollama) | v3 | 1.00 | 1.00 | 1.00 | 1.00 | starter_v0/runs/v3_B_group_ollama_20261110T190101423006.json |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
