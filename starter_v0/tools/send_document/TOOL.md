---
name: send_document
track: bonus
kind: action
provider: Telegram Bot API
requires_env: [TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]
inputs: [artifact_id, caption, confirmed]
outputs: [status, artifact_id, message_id, filename, sha256]
side_effect: true
requires_confirmation: true
---
# send_document

Gửi file Markdown/CSV từ `research_export` tới private channel trong cấu hình.
Chỉ nhận `artifact_id` có trong phiên hiện tại, không nhận đường dẫn hoặc bytes
do model tự tạo. Runtime gắn artifact ID vào kết quả export và hỏi người dùng
xác nhận đúng file, caption và đích gửi. Model không thể tự cấp quyền gửi bằng
`confirmed=true`; runtime chỉ thực thi sau một lượt xác nhận riêng.

Upload UTF-8 trong bộ nhớ qua `sendDocument`, không ghi file. Chỉ trả `sent`
khi Telegram trả `ok=true` và có message ID. Caption tối đa 1024 ký tự.
Mỗi artifact chỉ được gửi một lần; timeout không được tự retry do có thể đã gửi.
Lỗi mạng được che URL/token. Unit test mock HTTP, không gửi thật.

Gửi file là năng lực mở rộng; không tự thay thế bằng chứng bonus `send` gửi text.
