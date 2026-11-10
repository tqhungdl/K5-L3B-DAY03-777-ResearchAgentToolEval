# Source code

Toàn bộ source code của lab nằm trong folder này. Chạy mọi lệnh từ `starter_v0/`.

- File bắt đầu chạy: `run_eval.py` (chạy eval), `chat.py` (chat live), `scripts/preflight_provider.py` (kiểm tra provider).
- Cách chạy: `python run_eval.py --provider openrouter --version v0 --suite base --eval-cases data/eval_base.json`; `python chat.py --provider openrouter --version v3`; `pytest`.
- Input: `artifacts/system_prompt.md`, `artifacts/tools.yaml`, bộ case `data/*.json`, API key trong `.env` (mẫu ở `.env.example`).
- Output: `runs/*.json` (kết quả eval), `transcripts/*.transcript.json` (chat live), `analysis/*.csv` (nếu chạy `scripts/parse_runs.py`).
- File học viên được sửa: `artifacts/system_prompt.md`, `artifacts/tools.yaml`, `artifacts/version_log.csv`, `data/eval_group.json`, `tools/` (thêm tool mới và đăng ký trong `tools/__init__.py`), `tests/test_tools_todo.py`, code UI và `requirements.txt`. Không sửa nội dung case trong `data/eval_base.json`.

Chi tiết từng bước xem [README.md](../README.md) ở root; cấu hình API key xem [docs/TOOL-SETUP.md](../docs/TOOL-SETUP.md).

## UI và eval nhóm (CP4–CP5)

Chạy từ `starter_v0/` trong Python environment đã cài `requirements.txt`:

```bash
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
python run_eval.py --provider openrouter --version v3 --suite group --eval-cases data/eval_group.json
python chat.py --provider openrouter --version v3
```

Mở link thử bằng `cloudflared tunnel --url http://127.0.0.1:8501` trong terminal khác.
Cấu hình Telegram xem [TOOL-SETUP.md](../docs/TOOL-SETUP.md). File từ
`research_export` được tải trong UI hoặc gửi qua `send_document` sau xác nhận.
Tool gửi file hiện cần context artifact của phiên CLI/UI.

Prompt và version log của nhóm được giữ nguyên; cần chạy lại group/live chat trước
khi ghi metric cho cấu hình hiện tại. Không dùng số đo của prompt đã loại bỏ.
