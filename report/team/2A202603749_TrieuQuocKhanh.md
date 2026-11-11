# Báo cáo cá nhân — Triệu Quốc Khánh - 2A202603749

## 1. Thông tin thành viên

- Họ tên: Triệu Quốc Khánh
- MSSV: 2A202603749
- Email: 26ai.khanhtq4@vinuni.edu.vn
- GitHub: qockhah253

## 2. Phần việc phụ trách

| Hạng mục | Nội dung | Vị trí |
|---|---|---|
| CP2: v2 | Sửa `system_prompt.md`: bỏ chỉ dẫn "đoán, đừng hỏi", thêm rule gọi `clarify` khi thiếu thông tin | `starter_v0/artifacts/system_prompt.md` |
| CP2: v4 | Sửa khai báo `clarify` trong `tools.yaml`: bắt buộc `response_type`, mô tả khi nào dùng | `starter_v0/artifacts/tools.yaml` |
| Báo cáo nhóm | Điền hàng v2 và v4 của bảng B1, bảng B2 (phân tích 7 case FAIL của v0) | `report/team/group_report.md` |
| Thử nghiệm v5 (bị loại) | Sửa `system_prompt.md` để `clarify` dùng `text` khi thiếu thông tin, `yes_no` khi xác nhận gửi; không giữ vì không hơn v4 | `starter_v0/runs/v5_B_*.json` |
| Thử nghiệm cá nhân | Chạy riêng chuỗi v1 đến v3 trên nhánh `feature/QuocKhanh` để hiểu từng giả thuyết | nhánh `feature/QuocKhanh` |

## 3. Đóng góp cụ thể

| Version | Giả thuyết | Điểm trước | Điểm sau | Kết quả |
|---|---|---|---|---|
| v2 | Chỉ dẫn "đoán, đừng hỏi" làm model không hỏi lại khi thiếu thông tin (R10, R11) | 0.75 | 0.80 | R10 và R11 đã gọi `clarify` nhưng thiếu `response_type`. R08 và R13 chuyển PASS, M06 chuyển FAIL; chưa tách được cơ chế |
| v4 | Model bỏ `response_type` vì tham số tùy chọn và mô tả sơ sài | 0.85 | 0.95 | R10 và R11 PASS. Còn R12 (gửi ngay không hỏi xác nhận) |

- v5 (thử nghiệm, không dùng): commit `ece7fb1`, run `starter_v0/runs/v5_B_base_openrouter_20261111T091650830418.json` và `starter_v0/runs/v5_B_group_openrouter_20261111T091959082688.json`. Tổng điểm hòa với v4 (27/30), nên revert về v4 ở commit `b557861`.
- Mỗi version chỉ đổi một artifact, hash prompt và tools ghi trong `starter_v0/artifacts/version_log.csv`.
- Bảng B2 lấy `actual_tool_calls` và `failures` từ run v0, cột Fix đối chiếu với run v1 đến v4.
- Trên nhánh cá nhân, chuỗi thử riêng cho kết quả 0.65, 0.85, 0.95, 0.85. Bản v3 cá nhân (thêm ranh giới xác nhận cho `send`) làm R12 không còn tự gửi nhưng sai `response_type`, và M02, M06 mới FAIL ổn định qua 2 lần chạy. Chưa xác định phần nào của thay đổi gây ra việc này.

## 4. Bằng chứng

- File/commit/PR (nhánh `main`):
  - v2: commit `a7d0452`, run `starter_v0/runs/v2_B_base_openrouter_20261110T193758373016.json`
  - v4: commit `e65b1e5`, run `starter_v0/runs/v4_B_base_openrouter_20261110T235816402814.json`
  - Bảng B1: commit `05ffbca`
  - Nhánh cá nhân `feature/QuocKhanh`: commit `7a9e47a` (v1), `aa10542` (v2), `4d604d7` (v3)
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Dùng Claude để hướng dẫn từng bước và soạn nháp nội dung sửa.
  - Tự kiểm tra bằng `pytest tests/test_tool_contract.py` (55 passed) sau mỗi lần sửa `tools.yaml`, chạy `run_eval.py` rồi đọc `actual_tool_calls` và `failures` trong file run để xác định case nào đổi trạng thái, không dựa vào tên nhãn lỗi.
  - Chỉ dùng run hợp lệ (`provider_error_cases = 0`, `measured_cases = 20`).

## 5. Tự đánh giá

- Làm tốt: mỗi version có một giả thuyết, một run hợp lệ và điểm trước và sau đọc được từ file run.
- Hạn chế: R12 chưa PASS ở bản nào. Các chuyển trạng thái của R08, R13, R14 (v1, v2) và M02, M06 (v3 cá nhân) chưa được giải thích bằng thí nghiệm riêng từng phần.
- Chưa làm: CP3 đến CP5 do thành viên khác phụ trách.
