# Team

## Thông tin nhóm

- Tên nhóm:
- Lớp: L3A / L3B
- Repo nhóm: `K5-L3A-DAY03-TenNhom-ResearchAgentToolEval` hoặc `K5-L3B-DAY03-TenNhom-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Đức Hiếu | 2A202603772 | 26ai.hieund6@vinuni.edu.vn | https://github.com/Hie24/ | Setup, baseline và tối ưu CP1–CP2; review CP3–CP4 |
|   2 |        |      |       |        |         |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## Nguyễn Đức Hiếu — 2A202603772

### Phần việc phụ trách

- Setup môi trường/API, chạy baseline và tối ưu prompt/tool declaration v1–v3 (CP1–CP2); review, bàn giao CP3–CP4.

### Đóng góp cụ thể

- Tích hợp Groq, bổ sung script giãn cách/retry, lưu run và hash từng version. Accuracy base: **65% → 80% → 85% → 85%**, mỗi run đủ 20 case và không lỗi provider.
- Kiểm thử khi bàn giao CP1–CP2: **62 passed, 17 skipped, 0 failed**; rà soát calculator và case eval nhóm của thành viên phụ trách.

### Bằng chứng

- [Báo cáo cá nhân](report/team/2A202603772_NguyenDucHieu.md), [version log](starter_v0/artifacts/version_log.csv), [commit CP1–CP2](https://github.com/Hie24/K5-L3B-DAY03-HH-ResearchAgentToolEval/commit/5b7dd24b292f2afa7ecc417bb46f846215b0d536).
