# Team

## Thông tin nhóm

- Tên nhóm: 777
- Lớp: L3A / L3B
- Repo nhóm: `K5-L3A-DAY03-TenNhom-ResearchAgentToolEval` hoặc `K5-L3B-DAY03-TenNhom-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên           | MSSV        | Email                      | GitHub          | Vai trò                             |
| --: | ---------------- | ----------- | -------------------------- | --------------- | ----------------------------------- |
|   1 | Trần Quang Hưng  | 2A202603767 |                            | tqhungdl        |                                     |
|   2 | Nguyễn Tiến Đạt  | 2A202603752 | 26ai.datnt24@vinuni.edu.vn | chesschillchill | Cải thiện agent, xây dựng tools, UI |
|   3 | Triệu Quốc Khánh | 2A202603749 |                            | qockhah253      | Sửa prompt và khai báo tool (v2, v4)|

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## Triệu Quốc Khánh - 2A202603749

### Phần việc phụ trách

- CP2: v2 (`system_prompt.md`), v4 (`tools.yaml`).
- Báo cáo nhóm: bảng B1 (v2, v4, v5), bảng B2.
- Báo cáo cá nhân: `report/team/2A202603749_TrieuQuocKhanh.md`.

### Đóng góp cụ thể

- v2: bỏ chỉ dẫn "đoán, đừng hỏi", thêm rule gọi `clarify` (0.75 → 0.80).
- v4: sửa khai báo `clarify`, bắt buộc `response_type` (0.85 → 0.95).
- v5: thử nghiệm bị loại (hòa 27/30 với v4), đã revert về v4.
- B2: phân tích 7 case FAIL của v0; sửa `version_log.csv` (bọc ngoặc kép dòng v1, thêm `runs/` cho dòng v3).

### Bằng chứng

- Commit: `a7d0452` (v2), `e65b1e5` (v4), `05ffbca` (B1), `0657db9` (B2), `ece7fb1` (v5), `b557861` (revert về v4), `9195b65` (báo cáo cá nhân).
- Run: `starter_v0/runs/v2_B_base_openrouter_20261110T193758373016.json`, `starter_v0/runs/v4_B_base_openrouter_20261110T235816402814.json`.

## Tran Quang Hung - 2A202603767

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
