# Team

## Thông tin nhóm

- Tên nhóm: 777
- Lớp: L3A / L3B
- Repo nhóm: `K5-L3A-DAY03-TenNhom-ResearchAgentToolEval` hoặc `K5-L3B-DAY03-TenNhom-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên           | MSSV        | Email                      | GitHub          | Vai trò                             |
| --: | ---------------- | ----------- | -------------------------- | --------------- | ----------------------------------- |
|   1 | Trần Quang Hưng  | 2A202603767 | 26ai.26ai.hungtq4@vinuni.edu.vn | tqhungdl   | Sửa prompt, viết tool test           |
|   2 | Nguyễn Tiến Đạt  | 2A202603752 | 26ai.datnt24@vinuni.edu.vn | chesschillchill | Cải thiện agent, xây dựng tools, UI |
|   3 | Triệu Quốc Khánh | 2A202603749 | 26ai.khanhtq4@vinuni.edu.vn | qockhah253      | Sửa prompt và khai báo tool (v2, v4)|

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

## 2. Phần việc phụ trách

Cải thiện agent v2 -> v3, quản lý git, hỗ trợ viết eval_group.json, viết các test trong test_tools_todo.py

## 3. Đóng góp cụ thể

- Cải thiện v2 -> v3, làm rõ quy trình clarify
- Hỗ trợ viết eval_group.json

## 4. Bằng chứng

- File/commit/PR:
- **Cải thiện v2 -> v3**: https://github.com/tqhungdl/K5-L3B-DAY03-777-ResearchAgentToolEval/commit/a8384b1cbf1ac3aec4602658e87cfb06b5f4d253
- **Hỗ trợ viết eval_group.json**: https://github.com/tqhungdl/K5-L3B-DAY03-777-ResearchAgentToolEval/commit/d83a15a3f07b96db5dfc3a58b1f04a51b34523bf
- **Viết test**: https://github.com/tqhungdl/K5-L3B-DAY03-777-ResearchAgentToolEval/commit/928c81f80d6d779e5ea04f5a9d7f753eca92d033

## Nguyễn Tiến Đạt - 2A202603752

### Phần việc phụ trách

- Cải thiện agent v1, xây tool, UI, eval nhóm và minh chứng chat live (CP2–CP5).

### Đóng góp cụ thể

- **Cải thiện v1:** làm rõ argument `query` của `lookup`, chạy baseline/v1 và ghi nhận accuracy tăng từ 65% lên 75%.
- **Xây research_export:** xuất nguồn thành Markdown/CSV, đăng ký tool, viết TOOL.md và 21 test case.
- **Xây send_document:** gửi file Telegram sau xác nhận; thêm test upload, input sai, lỗi API và ngăn gửi lặp.
- **Làm UI:** xây Streamlit chat, xem trước/tải file; dùng chung runtime với CLI để giữ nguồn và xác nhận theo phiên.
- **Làm eval nhóm:** xây 10 case (5 single, 5 multi), tự chạy group eval đạt 8/10 và cập nhật B3.
- **Chạy chat live:** thực hiện 3 phiên về research, bổ sung URL và xác nhận gửi file Telegram; cập nhật B4 theo transcript.

### Bằng chứng

- **Cải thiện v1:** commit [8b3181b](https://github.com/tqhungdl/K5-L3B-DAY03-777-ResearchAgentToolEval/commit/8b3181bb56875a0a20d00589c5a507397edea430); [run v1: 15/20](starter_v0/runs/v1_B_base_openrouter_20261110T191359165510.json).
- **research_export:** commit [b238bcf](https://github.com/tqhungdl/K5-L3B-DAY03-777-ResearchAgentToolEval/commit/b238bcf0a966d979846519ffe03a69d70e736697); [tool.py](starter_v0/tools/research_export/tool.py), [unit test](starter_v0/tests/test_tools_todo.py).
- **send_document:** commit [d83a15a](https://github.com/tqhungdl/K5-L3B-DAY03-777-ResearchAgentToolEval/commit/d83a15a3f07b96db5dfc3a58b1f04a51b34523bf); [tool.py](starter_v0/tools/send_document/tool.py), [unit test](starter_v0/tests/test_tools_todo.py).
- **UI và runtime:** commit [d83a15a](https://github.com/tqhungdl/K5-L3B-DAY03-777-ResearchAgentToolEval/commit/d83a15a3f07b96db5dfc3a58b1f04a51b34523bf); [app.py](starter_v0/app.py), [chat_runtime.py](starter_v0/chat_runtime.py), [AppTest](starter_v0/tests/test_app.py).
- **Eval nhóm:** commit [fcd4146](https://github.com/tqhungdl/K5-L3B-DAY03-777-ResearchAgentToolEval/commit/fcd4146d850bb90e5eb12e96fe11cd5eb7132449); [eval_group.json](starter_v0/data/eval_group.json), [run group: 8/10](starter_v0/runs/v4_B_group_openrouter_20261111T014529106049.json).
- **Chat live:** commit [fcd4146](https://github.com/tqhungdl/K5-L3B-DAY03-777-ResearchAgentToolEval/commit/fcd4146d850bb90e5eb12e96fe11cd5eb7132449); [B4](report/team/group_report.md#b4-live-chat-evidence), [transcript gửi file thành công, message_id=6](starter_v0/transcripts/faa91e1df2e2418f85920f6c75cfd0ea.transcript.json).
