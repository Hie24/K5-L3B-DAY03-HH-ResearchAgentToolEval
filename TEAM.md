# Team

## Thông tin nhóm

- Tên nhóm:
- Lớp: L3A / L3B
- Repo nhóm: `K5-L3A-DAY03-TenNhom-ResearchAgentToolEval` hoặc `K5-L3B-DAY03-TenNhom-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Mạnh Quân | 2A202603776 | 26ai.quannm9@vinuni.edu.vn | osgi23 | Phụ trách CP3 & CP4 (Tool mới `calculator`, Unit test, 10 eval cases) |
|   2 |        |      |       |        |         |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Sao chép mục dưới đây cho từng thành viên.

## Nguyễn Mạnh Quân - 2A202603776

### Phần việc phụ trách

- CP3: Phát triển tool mới `calculator` và viết unit test (mốc 15:30).
- CP4: Thiết kế bộ dữ liệu 10 case `eval_group.json` và thực thi đánh giá mô hình (mốc 16:00).

### Đóng góp cụ thể

- Cài đặt `tools/calculator/tool.py` dùng AST an toàn (chống code injection, trả dict lỗi khi gặp ngoại lệ), hoàn thành `TOOL.md`, đăng ký trong `tools/__init__.py`, `tools.yaml` và `system_prompt.md`.
- Viết 3 unit test trong `tests/test_tools_todo.py` (happy path, input xấu, chia cho 0); pytest đạt 63 passed, 0 failed.
- Thiết kế 10 eval cases tại `data/eval_group.json` (5 single-turn, 5 multi-turn) bao gồm routing tool mới và bám sát các lỗi từ CP1/CP2 (R03, R11, R12, M02).
- Thực thi đánh giá trên Groq (`openai/gpt-oss-120b`, đạt 8/10) và đối chiếu trên Ollama local (`qwen2.5:7b`, đạt 10/10).

### Bằng chứng

- Code & test: `starter_v0/tools/calculator/`, `starter_v0/tests/test_tools_todo.py`, `starter_v0/data/eval_group.json`
- Run JSON: `starter_v0/runs/v3_B_group_groq_20261110T193553495897.json`, `starter_v0/runs/v3_B_group_ollama_20261110T190101423006.json`
- Báo cáo cá nhân: `report/team/2A202603776_NguyenManhQuan.md`

## HoVaTen-MSSV

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
