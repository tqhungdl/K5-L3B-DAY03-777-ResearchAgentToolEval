# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
>
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: chưa cập nhật trong TEAM.md.
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md).
- Provider/model: OpenRouter / `openai/gpt-4o-mini` (theo run JSON).

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

AI Research Briefing giúp tìm tin/paper AI, đọc nguồn cụ thể, tổng hợp có dẫn nguồn, xuất Markdown/CSV và gửi Telegram sau xác nhận.

**Chạy UI** (từ `starter_v0/`, sau khi cài `requirements.txt`):

```bash
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

**Link thử:** https://developed-coaching-nickname-leaves.trycloudflare.com

Link tạm thời qua Cloudflare Tunnel; server và tunnel cần còn chạy. Cần bắt đầu phiên mới sau khi khôi phục prompt; chưa nghiệm thu lại UI với prompt này.

### A2. Tool agent có

| Tool | Chức năng | Tool mới? |
|---|---|---|
| clarify | Hỏi bổ sung và dừng chờ | không |
| lookup | Tìm nguồn web/tin tức | không |
| fetch | Đọc URL cụ thể | không |
| papers | Tìm paper arXiv | không |
| paper_text | Đọc text PDF arXiv | không |
| format | Trình bày bản tin trong chat | không |
| timeline | Bài đăng từ một account X | không |
| social_search | Tìm bài đăng X theo từ khóa | không |
| policy | Tra policy nội bộ mẫu | không |
| send | Gửi text Telegram sau xác nhận | không |
| research_export | Tạo nội dung file Markdown/CSV | có |
| send_document | Gửi export của phiên tới Telegram | có |

### A3. Câu hỏi mẫu để thử

1. Tìm 3 nguồn trên web về đánh giá tool calling của AI agent.
2. Tìm 3 paper arXiv về đánh giá AI agent.
3. Xuất danh sách vừa tìm thành CSV, giữ nguyên dữ liệu nguồn.
4. Tôi muốn đọc một bài khác nhưng chưa cung cấp URL; hãy hỏi tôi URL.
5. Gửi file vừa xuất tới Telegram nhóm; hãy hỏi xác nhận trước.

## 3. Giải pháp

- Giữ nguyên system prompt và declaration của các tool có sẵn do nhóm chốt; chỉ bổ sung declaration cho `send_document`.
- `research_export` tạo file trong bộ nhớ. `send_document` upload UTF-8 từ artifact của phiên, không đọc đường dẫn do model cung cấp.
- CLI/UI dùng chung `chat_runtime.py`: giữ nguồn gốc theo URL, xác nhận gắn với file/caption/đích gửi; đổi yêu cầu làm hết hiệu lực xác nhận.
- Transcript ghi tool/model args và args thực thi; provider lỗi vẫn giữ tool event đã hoàn thành.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
| ------- | ---------------- | ---------- | ------------: | -----------: | -------- |
| v0      | baseline         |            |               |              |          |
| v1      |                  |            |               |              |          |
| v2      |                  |            |               |              |          |
| v3      |                  |            |               |              |          |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
| ------- | ------------ | ----------------- | ----------- | --- |
|         |              |                   |             |     |

### B3. Team Eval Cases

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_export_csv | Export file thay vì format chat; định dạng CSV | research_export {"output_format": "csv"} | Chưa đo lại |
| G02_export_markdown | Markdown export từ dữ liệu có sẵn | research_export {"output_format": "markdown"} | Chưa đo lại |
| G03_format_only | Phân biệt format và export | format {"template": "bullets"} | Chưa đo lại |
| G04_missing_sources | Không bịa items khi chưa có dữ liệu | clarify {"response_type": "text"} | Chưa đo lại |
| G05_explain_formats | Câu hỏi giải thích không cần tool | no_tool | Chưa đo lại |
| G06_context_export | Dùng nguồn ở lượt trước | research_export {"output_format": "csv"} | Chưa đo lại |
| G07_change_format | Yêu cầu mới nhất thay định dạng cũ | research_export {"output_format": "markdown"} | Chưa đo lại |
| G08_send_unconfirmed | Thiếu file không được đoán artifact_id hoặc gửi | clarify {"response_type": "text"} | Chưa đo lại |
| G09_cancel_send | User từ chối gửi; không gọi action | no_tool | Chưa đo lại |
| G10_edit_after_confirmation | Đổi nội dung/định dạng không tái dùng xác nhận cũ | research_export {"output_format": "markdown"} | Chưa đo lại |

Đúng 5 single + 5 multi. Cần chạy group eval với prompt đã khôi phục; chưa có metric cho cấu hình này.

### B4. Live Chat Evidence

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| — | Chưa thu lại sau khi khôi phục prompt | — | — | Cần chạy chat live |

Transcript sử dụng UI của người dùng được giữ nguyên; không đổi version hay nội dung để làm bằng chứng cho prompt mới.

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| research_export | [tool + TOOL.md](../../starter_v0/tools/research_export/), [tests](../../starter_v0/tests/test_tools_todo.py) | Markdown/CSV, Unicode và CSV quoting | Offline, không tự tìm/bịa nguồn |
| send_document | [tool + TOOL.md](../../starter_v0/tools/send_document/), [tool tests](../../starter_v0/tests/test_tools_todo.py), [runtime tests](../../starter_v0/tests/test_chat_runtime.py) | Upload bytes gốc; kiểm tra lỗi, phiên và xác nhận | Không gửi khi model tự xác nhận; không tự retry timeout |
| Unit test | [pytest output](../../starter_v0/analysis/cp4_cp5_pytest.txt) | 119 passed, 14 skipped, 0 failed; contract và AppTest xanh | Stub tool cũ được phép skip |
| UI | [app.py](../../starter_v0/app.py), [AppTest](../../starter_v0/tests/test_app.py) | Chat, preview, tải file, xác nhận/hủy; rerender không gọi lại provider | Cần người ngoài nhóm thử link |

Unit test CSV đọc ngược bằng `csv.DictReader` để bắt lỗi tách cột/hàng mà routing eval không kiểm tra. Regression runtime bắt lỗi model rút gọn summary khi export bằng cách so với record nguồn gốc.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus                                        | Evidence File   | What Worked | Risk / Guardrail |
| -------------------------------------------- | --------------- | ----------- | ---------------- |
| Small Local Model                            | xem B7          |             |                  |
| Hơn 3 tool mới (≥ 4)                         |                 |             |                  |
| `send` gửi thật lên Telegram sau xác nhận    | transcript      |             |                  |
| Test challenge (0 skipped / regression test) | `pytest` output |             |                  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version    | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
| ---------- | ---------------- | ------------ | ------------- | ------------ | -------- | --------- | -------- |
| v3         | (cloud)          | v3           |               |              |          |           |          |
| v3-<model> | (ollama)         | v3           |               |              |          |           |          |
| v3-<model> | (ollama)         | v3           |               |              |          |           |          |
| v4-local   |                  |              |               |              |          |           |          |
| v5-local   |                  |              |               |              |          |           |          |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern                               | Count | Example Case | Fix Tried | Helped? |
| --------------------------------------------- | ----- | ------------ | --------- | ------- |
| wrong / hallucinated tool                     |       |              |           |         |
| invalid JSON args (`_invalid_json_arguments`) |       |              |           |         |
| no tool call / answered directly              |       |              |           |         |
| missed `clarify`                              |       |              |           |         |
| repeated / unnecessary calls                  |       |              |           |         |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

- Đã khôi phục prompt/version log của nhóm; cần đo lại group và thu lại transcript đúng cấu hình.
- Gửi file đã có unit test; chưa gửi Telegram thật.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Chưa có group run và live transcript cho prompt đã khôi phục.
- Routing eval không xác minh nội dung bản tin; cần đọc đối chiếu nguồn.
- `send_document` hiện cần artifact của phiên CLI/UI; không hoạt động độc lập trong runner eval chưa có context phiên.

## 8. Tài liệu tham khảo

- [Đề bài](../../README.md), [checkpoints](../../CHECKPOINTS.md), [rubric](../../RUBRIC.md).
- [Telegram sendDocument](https://core.telegram.org/bots/api#senddocument).
- [Streamlit Session State](https://docs.streamlit.io/develop/concepts/architecture/session-state), [AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest).
