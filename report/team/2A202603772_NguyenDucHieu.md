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

Điểm dưới đây là mức tự chấm đề xuất theo rubric, dựa trên bằng chứng của phần việc phụ trách.

| Tiêu chí | Điểm tự đánh giá | Minh chứng |
|---|:---:|---|
| **C1 — Setup, baseline và phân tích lỗi (CP1)** | **9 / 10** | Tích hợp Groq khi Gemini thiếu quota; baseline v0 đo đủ 20 case, không lỗi provider; lưu run, hash và phân tích đủ 7 case FAIL. |
| **C2 — System prompt và tool declaration (CP2)** | **13 / 15** | Bổ sung quy tắc hỏi lại, xác nhận trước khi gửi, định tuyến nguồn và quy ước arguments; accuracy tăng từ 65% lên 85%, còn lỗi query và phối hợp nhiều tool. |
| **C3 — Ba vòng tối ưu v1–v3 có bằng chứng (CP2)** | **18 / 20** | Mỗi vòng có giả thuyết, artifact thay đổi, snapshot/hash và run thật trên cùng model; ghi trung thực việc v3 không tăng điểm so với v2. |
| **Phối hợp nhóm và tích hợp hệ thống** | **Hoàn thành** | Review CP3–CP4, gộp code ba nhánh, sửa lỗi UI/calculator và đồng bộ báo cáo; bản tích hợp đạt 85 passed, 14 skipped, base 17/20, group 9/10 và có transcript Groq thật 4 lượt. |

Bằng chứng tích hợp: [commit f94a52e](https://github.com/Hie24/K5-L3B-DAY03-HH-ResearchAgentToolEval/commit/f94a52e87f1657eaa5523736e1275e323383e5b5). Phần phát triển ban đầu calculator và UI thuộc các thành viên phụ trách; đóng góp bổ sung của tôi là review, sửa lỗi và tích hợp.

Cần tiếp tục xử lý R03 (query), R12 (response_type xác nhận) và R13 (thiếu tool mạng xã hội). Kết quả mới phản ánh bộ case đã đo; bản tích hợp chưa có link UI public và chưa kiểm chứng gửi Telegram thật.
