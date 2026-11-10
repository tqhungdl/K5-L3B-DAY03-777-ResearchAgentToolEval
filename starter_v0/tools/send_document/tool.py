from __future__ import annotations

import os
import requests

from artifact_store import CURRENT_ARTIFACTS
from tools._shared import TIMEOUT


def send_document(artifact_id: str = "", caption: str = "", confirmed: bool = False) -> dict:
    """Upload only a session export, with no filesystem access or model-supplied bytes."""
    if confirmed is not True:
        return {"tool": "send_document", "status": "needs_confirmation"}
    store = CURRENT_ARTIFACTS.get()
    if not isinstance(artifact_id, str) or not store or artifact_id not in store.artifacts:
        return {"tool": "send_document", "error": "ValueError", "message": "Unknown export in this session"}
    if not isinstance(caption, str) or len(caption) > 1024:
        return {"tool": "send_document", "error": "ValueError", "message": "caption must be a string of at most 1024 characters"}
    if artifact_id in store.sent:
        return {"tool": "send_document", "status": "already_sent", "artifact_id": artifact_id}
    token, chat_id = os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return {"tool": "send_document", "error": "ConfigurationError", "message": "Missing TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID"}
    artifact = store.artifacts[artifact_id]
    # Reserve before HTTP: an ambiguous timeout must not cause an automatic duplicate.
    store.sent.add(artifact_id)
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendDocument",
            data={"chat_id": chat_id, "caption": caption},
            files={"document": (artifact["filename"], artifact["content"].encode("utf-8"), artifact["mime_type"].split(";")[0])},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("ok") is not True:
            store.sent.discard(artifact_id)
            return {"tool": "send_document", "error": "TelegramError", "message": "Telegram rejected the document"}
        message_id = payload.get("result", {}).get("message_id")
        if not message_id:
            raise ValueError("Invalid Telegram response")
        return {"tool": "send_document", "status": "sent", "artifact_id": artifact_id, "message_id": message_id, "filename": artifact["filename"], "sha256": artifact["sha256"]}
    except Exception:
        # requests exceptions may embed the bot token in their URL. Never log them.
        return {"tool": "send_document", "error": "DeliveryError", "message": "Delivery could not be verified; check Telegram before sending a new export"}
