# Báo cáo cá nhân — Nguyễn Tiến Đạt — 2A202603752

## 1. Thông tin thành viên

- Họ tên: Nguyễn Tiến Đạt
- MSSV: 2A202603752
- Email: 26ai.datnt24@vinuni.edu.vn

## 2. Phần việc phụ trách

- Cải thiện agent v1, xây tool, UI, eval nhóm và minh chứng chat live (CP2–CP5).

## 3. Đóng góp cụ thể

- **Cải thiện v1:** làm rõ argument `query` của `lookup`, chạy baseline/v1 và ghi nhận accuracy tăng từ 65% lên 75%.
- **Xây research_export:** xuất nguồn thành Markdown/CSV, đăng ký tool, viết TOOL.md và 21 test case.
- **Xây send_document:** gửi file Telegram sau xác nhận; thêm test upload, input sai, lỗi API và ngăn gửi lặp.
- **Làm UI:** xây Streamlit chat, xem trước/tải file; dùng chung runtime với CLI để giữ nguồn và xác nhận theo phiên.
- **Làm eval nhóm:** xây 10 case (5 single, 5 multi), tự chạy group eval đạt 8/10 và cập nhật B3.
- **Chạy chat live:** thực hiện 3 phiên về research, bổ sung URL và xác nhận gửi file Telegram; cập nhật B4 theo transcript.

## 4. Bằng chứng

- **Cải thiện v1:** commit [8b3181b](https://github.com/tqhungdl/K5-L3B-DAY03-777-ResearchAgentToolEval/commit/8b3181bb56875a0a20d00589c5a507397edea430); [run v1: 15/20](../../starter_v0/runs/v1_B_base_openrouter_20261110T191359165510.json).
- **research_export:** commit [b238bcf](https://github.com/tqhungdl/K5-L3B-DAY03-777-ResearchAgentToolEval/commit/b238bcf0a966d979846519ffe03a69d70e736697); [tool.py](../../starter_v0/tools/research_export/tool.py), [unit test](../../starter_v0/tests/test_tools_todo.py).
- **send_document:** commit [d83a15a](https://github.com/tqhungdl/K5-L3B-DAY03-777-ResearchAgentToolEval/commit/d83a15a3f07b96db5dfc3a58b1f04a51b34523bf); [tool.py](../../starter_v0/tools/send_document/tool.py), [unit test](../../starter_v0/tests/test_tools_todo.py).
- **UI và runtime:** commit [d83a15a](https://github.com/tqhungdl/K5-L3B-DAY03-777-ResearchAgentToolEval/commit/d83a15a3f07b96db5dfc3a58b1f04a51b34523bf); [app.py](../../starter_v0/app.py), [chat_runtime.py](../../starter_v0/chat_runtime.py), [AppTest](../../starter_v0/tests/test_app.py).
- **Eval nhóm:** commit [fcd4146](https://github.com/tqhungdl/K5-L3B-DAY03-777-ResearchAgentToolEval/commit/fcd4146d850bb90e5eb12e96fe11cd5eb7132449); [eval_group.json](../../starter_v0/data/eval_group.json), [run group: 8/10](../../starter_v0/runs/v4_B_group_openrouter_20261111T014529106049.json).
- **Chat live:** commit [fcd4146](https://github.com/tqhungdl/K5-L3B-DAY03-777-ResearchAgentToolEval/commit/fcd4146d850bb90e5eb12e96fe11cd5eb7132449); [B4](group_report.md#b4-live-chat-evidence), [transcript gửi file thành công, message_id=6](../../starter_v0/transcripts/faa91e1df2e2418f85920f6c75cfd0ea.transcript.json).

- **AI đã dùng:** Codex hỗ trợ viết code/test, đọc log và soạn báo cáo; tôi kiểm tra lại phạm vi, tự chạy eval và chat live.
- **Kết quả kiểm tra:** [pytest do Codex chạy](../../starter_v0/analysis/cp4_cp5_pytest.txt): 119 passed, 14 skipped; đối chiếu thêm run JSON và transcript ở trên.

## 5. Tự đánh giá

- Hoàn thành tương đối tốt các phần việc được giao.
- Do thời gian tương đối ngắn, bản thân có sử dụng AI nhiều trong việc phát triển và viết tài liệu, nhưng đã đọc và điều chỉnh cẩn thận.
