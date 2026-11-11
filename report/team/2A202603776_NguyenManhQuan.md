# Báo cáo cá nhân — Nguyễn Mạnh Quân (2A202603776)

## 1. Thông tin thành viên

- **Họ tên:** Nguyễn Mạnh Quân
- **MSSV:** 2A202603776
- **Email:** 26ai.quannm9@vinuni.edu.vn

---

## 2. Phần việc phụ trách

1. **CP3 — Phát triển Tool mới và Xây dựng bộ Unit Test** : Thiết kế, cài đặt một công cụ mới cho Agent, đảm bảo các nguyên tắc an toàn, đăng ký vào hệ thống và viết unit test bao phủ các nhánh lỗi biên.
2. **CP4 — Xây dựng Bộ 10 Eval Cases của Nhóm và Thực thi Đánh giá**: Thiết kế bộ dữ liệu benchmark 10 case kế thừa các phân tích lỗi từ CP1 & CP2, đo lường việc định tuyến vào tool mới và thực hiện đánh giá mô hình.

---

## 3. Đóng góp cụ thể

### 3.1. CP3: Thiết kế, cài đặt Tool mới `calculator` và Unit Test

- **Xây dựng Tool `calculator`:**
  - **Mục tiêu:** Cho phép agent thực hiện các phép toán số học thực tế mà các tool tra cứu web/mạng xã hội không xử lý được.
  - **Kiến trúc an toàn:** Sử dụng module `ast` (Abstract Syntax Tree) để phân tích cú pháp biểu thức và thực thi phép tính tuần tự qua node visitor. **Tuyệt đối không dùng hàm `eval()`** để giới hạn cú pháp được thực thi.
  - **Xử lý ngoại lệ chuẩn mực:** Áp dụng nguyên tắc rào chắn của hệ thống, bắt trọn vẹn các ngoại lệ (`ZeroDivisionError`, `ValueError`, lỗi cú pháp) và trả về dictionary `{tool: 'calculate', error: <tên_lỗi>, message: <chi_tiết>}` thông qua hàm `err()` thay vì raise exception làm sập tiến trình agent.
  - **Đặc tả tool:** Soạn thảo đầy đủ metadata frontmatter YAML theo chuẩn lab (`inputs`, `outputs`, `side_effect: false`, `requires_confirmation: false`).

- **Đăng ký và Tích hợp hệ thống:**
  - Đăng ký hàm thực thi `calculate` vào từ điển `TOOL_FUNCTIONS` tại [`starter_v0/tools/__init__.py`](../../starter_v0/tools/__init__.py).
  - Khai báo tool trong [`starter_v0/artifacts/tools.yaml`](../../starter_v0/artifacts/tools.yaml) với mô tả ranh giới rõ ràng: khi nào dùng (tính toán số học, tài chính) và khi nào không dùng.
  - Bổ sung quy tắc định tuyến cho `calculator` vào [`starter_v0/artifacts/system_prompt.md`](../../starter_v0/artifacts/system_prompt.md) kế thừa trực tiếp trên nền bản v3 của bạn Hiếu.

- **Viết 3 Unit Test chuyên sâu ([`starter_v0/tests/test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py)):**
  1. `test_my_new_tool_happy_path`: Kiểm thử biểu thức `(100 + 50) * 2` trả 300 và giữ nguyên expression. Các ca số thực, số nguyên lớn, phép dư và giới hạn đầu vào được bổ sung trong `tests/test_integration.py`.
  2. `test_my_new_tool_bad_input_from_model`: Kiểm thử chuỗi rỗng `""` và biểu thức cú pháp sai lạ (`invalid_syntax_!@#`).
  3. `test_my_new_tool_failure_returns_error_dict`: Kiểm thử phép chia cho 0 (`100 / 0`), chứng minh hàm trả về dictionary lỗi `ZeroDivisionError` mà không raise exception.

- **Kết quả kiểm thử tự động:**
  - Lệnh: `pytest starter_v0/tests/test_tool_contract.py starter_v0/tests/test_tools_todo.py -v`
  - Đạt: **63 passed, 0 failed** (60/60 test hợp đồng công cụ và 3/3 test tool mới đều XANH).

---

### 3.2. CP4: Thiết kế Bộ dữ liệu 10 Eval Cases của Nhóm và Thực thi Đánh giá

- **Xây dựng Dataset 10 Cases ([`starter_v0/data/eval_group.json`](../../starter_v0/data/eval_group.json)):**
  - Thiết kế đúng cấu trúc gồm **5 single-turn queries** và **5 multi-turn turns**, có đầy đủ `failure_type`, `expect`, `metadata.what_it_tests`. Tất cả đều là tình huống nghiên cứu tiếng Việt thực tế, không sao chép lại bộ dữ liệu có sẵn.
  - **Mối liên hệ chặt chẽ với CP1 & CP2 và Tool mới:**
    - `G01`, `G02`, `GM01`: Kiểm tra mô hình định tuyến chính xác vào tool mới `calculator` (cả đơn lượt và đa lượt sau khi được hỏi lại).
    - `G03`: Kiểm tra ranh giới phân biệt giữa `social_search` và `timeline` theo định nghĩa v2.
    - `G04`: Kiểm tra trích xuất query sạch (`query='công nghệ Việt Nam'`) và truyền đúng `topic='news'`, `timeframe='day'` — trực tiếp kiểm tra việc khắc phục lỗi **R03** (query dính từ thừa) từ run baseline của bạn Hiếu.
    - `G05`: Kiểm tra hành vi từ chối gọi tool (`no_tool: true`) với câu chào hỏi thông thường.
    - `GM02`: Đa lượt kiểm tra hành vi hỏi xin link URL khi thiếu thông tin rồi mới gọi `fetch` — khắc phục lỗi **R11** (tự đoán web).
    - `GM03`: Đa lượt kiểm tra ranh giới xác nhận nghiêm ngặt trước khi gửi Telegram (`confirmed=true`) — khắc phục lỗi **R12** (vi phạm ranh giới xác nhận).
    - `GM04`: Đa lượt kiểm tra kế thừa mốc thời gian và chủ đề (`topic='news'`, `timeframe='day'`) khi người dùng đổi sang tìm xe điện — khắc phục lỗi **M02** (nhiễu từ khóa).
    - `GM05`: Đa lượt kiểm tra chuyển đổi nguồn dữ liệu linh hoạt từ Twitter sang báo chí web.

- **Thực thi Đo lường và Đánh giá Mô hình:**
  - **Chạy trên Groq Cloud (`openai/gpt-oss-120b`):** Sử dụng script nhịp độ [`scripts/run_paced_eval.py`](../../starter_v0/scripts/run_paced_eval.py) đồng bộ hoàn toàn với môi trường của bạn Hiếu:
    - Lệnh: `python scripts/run_paced_eval.py --min-interval 5 --provider groq --model openai/gpt-oss-120b --version v3 --suite group --eval-cases data/eval_group.json`
    - Kết quả: **8/10 PASS (80%)** — file run: [`runs/v3_B_group_groq_20261110T193553495897.json`](../../starter_v0/runs/v3_B_group_groq_20261110T193553495897.json).
    - Phân tích sâu 2 trường hợp fail:
      1. `G04`: Model dính chữ 'tin tức' (`query='tin tức công nghệ Việt Nam'`).
      2. `GM03`: Model Groq từ chối bịa nội dung bản tin và gọi `clarify` để xin nội dung trước khi gửi, tuân thủ xuất sắc rào chắn an toàn *"Never invent the message"* của nhóm.
  - **Chạy đối chiếu trên Local Ollama (`qwen2.5:7b`):**
    - Lệnh: `python run_eval.py --provider ollama --model qwen2.5:7b --version v3 --suite group --eval-cases data/eval_group.json`
    - Kết quả: **10/10 PASS (100%)** — file run: [`runs/v3_B_group_ollama_20261110T190101423006.json`](../../starter_v0/runs/v3_B_group_ollama_20261110T190101423006.json).

### 3.3. Hoàn thiện Tài liệu Báo cáo Nhóm

- Hoàn thành nội dung kỹ thuật tại các mục trong [`report/team/group_report.md`](../../report/team/group_report.md):
  - **Mục 3 (Giải thích cải tiến):** Mô tả chi tiết chức năng, cơ chế AST an toàn và điều kiện kích hoạt của `calculator`.
  - **Bảng B3 (Team Eval Cases):** Liệt kê chi tiết 10 cases, kỳ vọng hành vi, kết quả đo thực tế trên Groq và lý giải chi tiết cho từng kết quả.
  - **Bảng B5a (Required Evidence):** Điền bằng chứng tool mới, unit test và phân tích lỗi mà unit test bắt được nhưng eval tự động bỏ sót (như `ZeroDivisionError` và chuỗi rỗng).
  - **Bảng B7 & B5 (Small Local Model Challenge):** Ghi nhận bằng chứng chạy đối chiếu với model nội bộ Qwen2.5:7b local đạt 10/10.

---

## 4. Bằng chứng

- **File mã nguồn, cấu hình & dữ liệu:**
  - Tool mới: [`starter_v0/tools/calculator/tool.py`](../../starter_v0/tools/calculator/tool.py), [`TOOL.md`](../../starter_v0/tools/calculator/TOOL.md)
  - Đăng ký tool: [`starter_v0/tools/__init__.py`](../../starter_v0/tools/__init__.py), [`starter_v0/artifacts/tools.yaml`](../../starter_v0/artifacts/tools.yaml)
  - Unit tests: [`starter_v0/tests/test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py)
  - Dataset 10 cases: [`starter_v0/data/eval_group.json`](../../starter_v0/data/eval_group.json)
- **File kết quả đo lường (Run JSON):**
  - Groq chính thức: [`starter_v0/runs/v3_B_group_groq_20261110T193553495897.json`](../../starter_v0/runs/v3_B_group_groq_20261110T193553495897.json) (8/10 PASS)
  - Ollama local: [`starter_v0/runs/v3_B_group_ollama_20261110T190101423006.json`](../../starter_v0/runs/v3_B_group_ollama_20261110T190101423006.json) (10/10 PASS)
- **Công cụ AI đã sử dụng:**
  - Antigravity AI Assistant: Hỗ trợ kiểm tra cú pháp AST an toàn cho `calculator`, sinh các trường hợp kiểm thử biên (zero division, cú pháp hỏng) và rà soát tính hợp lệ của schema `eval_group.json`.
- **Cách tự kiểm tra kết quả:**
  - Chạy `pytest starter_v0/tests/test_tool_contract.py starter_v0/tests/test_tools_todo.py -v` đảm bảo 100% test xanh (0 failed).
  - Chạy `preflight_provider.py --provider groq` xác thực kết nối model trước khi eval.
  - Chạy `run_paced_eval.py` xác nhận log kết quả đủ 10 case không có lỗi hệ thống (`provider_error_cases == 0`).

---

## 5. Tự đánh giá

| Tiêu chí | Điểm tự đánh giá | Minh chứng |
|---|:---:|---|
| **C4 — Tool mới và unit test (CP3)** | **13 / 15** | Tool `calculator` viết đúng chuẩn AST, trả dictionary lỗi khi có ngoại lệ thay vì raise crash; 3 unit tests bao phủ happy path + edge cases; `pytest` 0 failed. |
| **C5 — 10 case eval nhóm (CP4)** | **8 / 10** | Đủ đúng 5 single-turn và 5 multi-turn, thiết kế độc lập không chép bộ base, có 3 case route tới tool mới, schema hợp lệ 100%, chạy ra file run JSON thật trên Groq. |
| **Phối hợp nhóm & Tương thích** | **Tốt** | Tích hợp hoàn hảo trên nền tảng CP1 & CP2 (v3) của thành viên Nguyễn Đức Hiếu, duy trì tính nhất quán về provider và model trong toàn bộ báo cáo nhóm. |


Ghi chú tích hợp: calculator đã được bổ sung kiểm tra kiểu dữ liệu, giới hạn độ phức tạp và giữ chính xác số nguyên; GM03 được bổ sung nội dung bản tin. Run Ollama cũ khác hash bản hiện tại và không chứng minh gửi Telegram thành công. Xem báo cáo nhóm và `analysis/pytest.txt` cho kết quả bản cuối.
