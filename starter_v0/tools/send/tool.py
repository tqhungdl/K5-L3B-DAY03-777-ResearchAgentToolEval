from __future__ import annotations

import os
from typing import Any

import requests

from tools._shared import TIMEOUT


def send_telegram(text: str = "", confirmed: bool = False) -> dict[str, Any]:
    if confirmed is not True:
        return {
            "tool": "send_telegram",
            "status": "needs_confirmation",
            "message": "Only send after the user explicitly confirms.",
        }
    try:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not token or not chat_id:
            raise RuntimeError("Missing TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID env var")
        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("ok") is not True:
            return {"tool": "send_telegram", "error": "TelegramError", "message": "Telegram rejected the message"}
        return {"tool": "send_telegram", "status": "sent", "message_id": payload.get("result", {}).get("message_id")}
    except Exception as exc:
        # HTTP exception URLs contain the bot token; never serialize them.
        return {"tool": "send_telegram", "error": type(exc).__name__, "message": "Telegram delivery failed; verify channel configuration and delivery before retrying"}

