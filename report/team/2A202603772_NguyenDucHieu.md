# Báo cáo cá nhân — Nguyễn Đức Hiếu — 2A202603772

## 1. Thông tin thành viên

- Họ tên: Nguyễn Đức Hiếu
- MSSV: 2A202603772
- Email: 26ai.hieund6@vinuni.edu.vn

## 2. Phần việc phụ trách

- Setup môi trường, cấu hình API và chạy baseline (CP1).
- Tối ưu prompt, tool declaration qua v1–v3 và phân tích kết quả (CP2).
- Kiểm tra bằng chứng, bàn giao và review nhánh thành viên làm CP3–CP4.

## 3. Đóng góp cụ thể

Tích hợp Groq khi Gemini gặp giới hạn quota; dùng thống nhất model `openai/gpt-oss-120b` cho chuỗi eval. Bổ sung script giãn cách yêu cầu và retry có giới hạn, lưu snapshot cùng hash để đối chiếu từng version.

| Version | Thay đổi chính | Case đạt | Accuracy |
|---|---|---:|---:|
| v0 | Baseline nguyên bản | 13/20 | 65% |
| v1 | Hỏi lại khi thiếu thông tin, kiểm tra xác nhận trước hành động | 16/20 | 80% |
| v2 | Làm rõ khi dùng từng tool và quy ước arguments | 17/20 | 85% |
| v3 | Bỏ ép chọn một tool, định tuyến nhiều nguồn | 17/20 | 85% |

Cả bốn run đều đo đủ 20 case, không có lỗi provider. Kết quả kiểm thử khi bàn giao: **62 passed, 17 skipped, 0 failed**; các test skip là stub TODO. Không sửa bộ case cố định hoặc đưa API key vào commit.

Ngoài CP1–CP2, tôi review calculator, case eval nhóm và xung đột tích hợp trên nhánh `NguyenManhQuan`; phần code CP3–CP4 thuộc thành viên phụ trách.

## 4. Bằng chứng

- Commit: [5b7dd24 — CP1–CP2](https://github.com/Hie24/K5-L3B-DAY03-HH-ResearchAgentToolEval/commit/5b7dd24b292f2afa7ecc417bb46f846215b0d536).
- Code: [Groq provider](https://github.com/Hie24/K5-L3B-DAY03-HH-ResearchAgentToolEval/blob/5b7dd24b292f2afa7ecc417bb46f846215b0d536/starter_v0/providers/groq_provider.py), [script chạy eval](https://github.com/Hie24/K5-L3B-DAY03-HH-ResearchAgentToolEval/blob/5b7dd24b292f2afa7ecc417bb46f846215b0d536/starter_v0/scripts/run_paced_eval.py).
- Version và kết quả: [version_log.csv](https://github.com/Hie24/K5-L3B-DAY03-HH-ResearchAgentToolEval/blob/5b7dd24b292f2afa7ecc417bb46f846215b0d536/starter_v0/artifacts/version_log.csv), [version_summary.csv](https://github.com/Hie24/K5-L3B-DAY03-HH-ResearchAgentToolEval/blob/5b7dd24b292f2afa7ecc417bb46f846215b0d536/starter_v0/analysis/version_summary.csv).
- Run gốc: [v0](https://github.com/Hie24/K5-L3B-DAY03-HH-ResearchAgentToolEval/blob/5b7dd24b292f2afa7ecc417bb46f846215b0d536/starter_v0/runs/v0_B_base_groq_20261110T182244730565.json), [v1](https://github.com/Hie24/K5-L3B-DAY03-HH-ResearchAgentToolEval/blob/5b7dd24b292f2afa7ecc417bb46f846215b0d536/starter_v0/runs/v1_B_base_groq_20261110T182835864967.json), [v2](https://github.com/Hie24/K5-L3B-DAY03-HH-ResearchAgentToolEval/blob/5b7dd24b292f2afa7ecc417bb46f846215b0d536/starter_v0/runs/v2_B_base_groq_20261110T183811591909.json), [v3](https://github.com/Hie24/K5-L3B-DAY03-HH-ResearchAgentToolEval/blob/5b7dd24b292f2afa7ecc417bb46f846215b0d536/starter_v0/runs/v3_B_base_groq_20261110T184556678670.json).
- Kiểm thử và lỗi còn lại: [pytest.txt](https://github.com/Hie24/K5-L3B-DAY03-HH-ResearchAgentToolEval/blob/5b7dd24b292f2afa7ecc417bb46f846215b0d536/starter_v0/analysis/pytest.txt), [v3_failures.csv](https://github.com/Hie24/K5-L3B-DAY03-HH-ResearchAgentToolEval/blob/5b7dd24b292f2afa7ecc417bb46f846215b0d536/starter_v0/analysis/v3_failures.csv).

**AI/công cụ:** Sử dụng ChatGPT/Codex hỗ trợ đọc đề, sửa code, phân tích log và soạn báo cáo; dùng Git, PowerShell và Python để chạy, kiểm tra. Kết quả được đối chiếu bằng preflight thật.

## 5. Tự đánh giá

Phần kỹ thuật CP1–CP2 có đủ baseline và ba vòng tối ưu, accuracy tăng từ 65% lên 85%. V3 không cải thiện so với v2. Ba lỗi còn lại là query khác kỳ vọng (R03), kiểu câu hỏi xác nhận chưa khớp (R12) và thiếu tool tìm mạng xã hội (R13).

Cần tiếp tục kiểm tra yêu cầu nhiều nguồn và review thủ công các lỗi boundary. Kết quả hiện chỉ phản ánh bộ base 20 case; UI, live chat và gửi Telegram thật chưa thuộc phần bằng chứng triển khai cá nhân này.
