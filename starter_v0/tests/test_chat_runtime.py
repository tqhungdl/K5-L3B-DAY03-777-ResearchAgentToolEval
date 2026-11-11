from copy import deepcopy

import pytest
import requests

from artifact_store import CURRENT_ARTIFACTS
from chat_runtime import ChatSession
from conftest import FakeResponse
from providers.base import ModelResponse, ToolCall
from tools import TOOL_FUNCTIONS

ITEM = {"title": "Nghiên cứu", "url": "https://example.com/paper", "summary": "Kết quả tiếng Việt"}


class ScriptedProvider:
    def __init__(self, *responses):
        self.responses = iter(responses)
        self.messages = []

    def complete(self, messages, *args, **kwargs):
        self.messages.append(deepcopy(messages))
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        return response


def call(name, **args):
    return ModelResponse(tool_calls=[ToolCall(name, args)])


def session(provider=None, **kwargs):
    return ChatSession(provider or ScriptedProvider(), system_prompt="test", tools=[], **kwargs)


def export(s):
    return s.artifacts.add(TOOL_FUNCTIONS["research_export"](items=[ITEM], output_format="csv"))


@pytest.fixture
def telegram(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-secret")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100000")


@pytest.mark.parametrize("response", [FakeResponse({"ok": False}), FakeResponse(status_code=429), requests.Timeout("https://api.telegram.org/bottest-secret/sendDocument")])
def test_document_api_failures_never_claim_success_or_leak_token(telegram, fake_http, response):
    s = session()
    aid = export(s)
    fake_http(response)
    token = CURRENT_ARTIFACTS.set(s.artifacts)
    try:
        result = TOOL_FUNCTIONS["send_document"](artifact_id=aid, confirmed=True)
    finally:
        CURRENT_ARTIFACTS.reset(token)
    assert "error" in result
    assert "test-secret" not in str(result)
    assert result.get("status") != "sent"


def test_model_cannot_self_confirm_delivery(telegram, fake_http):
    p = ScriptedProvider()
    s = session(p)
    aid = export(s)
    p.responses = iter([call("send_document", artifact_id=aid, confirmed=True)])
    http = fake_http(FakeResponse({"ok": True, "result": {"message_id": 8}}))
    first = s.turn("Gửi file này")
    assert first["status"] == "waiting_for_user"
    assert http == []
    second = s.turn("Xác nhận gửi")
    assert second["tool_events"][0]["result"]["status"] == "sent"
    assert len(http) == 1 and s.pending is None


@pytest.mark.parametrize("change", ["file", "filename", "mime_type", "destination"])
def test_modified_delivery_expires_approval(telegram, fake_http, monkeypatch, change):
    s = session()
    aid = export(s)
    s.prepare_send("send_document", {"artifact_id": aid})
    if change == "file":
        s.artifacts.artifacts[aid]["content"] += "Changed"
    elif change in ("filename", "mime_type"):
        s.artifacts.artifacts[aid][change] = "changed"
    else:
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100999")
    http = fake_http(FakeResponse())
    result = s.turn("Xác nhận gửi")
    assert result["tool_events"][0]["result"]["error"] == "ApprovalExpired"
    assert http == []


def test_cancel_and_edit_clear_approval_without_sending(telegram, fake_http):
    s = session(ScriptedProvider(ModelResponse(text="Đã thay đổi yêu cầu.")))
    aid = export(s)
    http = fake_http(FakeResponse())
    s.prepare_send("send_document", {"artifact_id": aid})
    assert s.turn("Hủy gửi")["tool_events"] == []
    assert s.pending is None
    s.prepare_send("send_document", {"artifact_id": aid})
    s.turn("Đổi thành Markdown, chưa gửi")
    assert s.pending is None and http == []


def test_prior_tool_sources_are_available_for_followup_export(monkeypatch, tmp_path):
    monkeypatch.setitem(TOOL_FUNCTIONS, "papers", lambda **kw: {"items": [ITEM]})
    p = ScriptedProvider(call("papers", query="AI"), ModelResponse(text="Có một paper."),
                         call("research_export", items=[ITEM], output_format="csv"), ModelResponse(text="Đã tạo file."))
    s = session(p, transcripts_dir=tmp_path)
    s.turn("Tìm paper AI")
    s.turn("Xuất danh sách vừa tìm thành CSV")
    assert ITEM["url"] in str(p.messages[2])
    assert len(s.artifacts.artifacts) == 1
    assert len(s.transcript["turns"]) == 2 and s.path.is_file()


def test_provider_error_keeps_completed_tool_events_and_redacts_secret(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-secret")
    p = ScriptedProvider(call("research_export", items=[ITEM]), RuntimeError("test-secret"))
    result = session(p).turn("Xuất nguồn")
    assert result["status"] == "provider_error"
    assert len(result["tool_events"]) == 1
    assert "test-secret" not in result["error"]


def test_followup_export_uses_original_source_not_model_rewritten_summary(monkeypatch):
    import csv
    import io
    original = {**ITEM, "summary": "Nguyên bản, đầy đủ\n" * 100}
    changed = {**ITEM, "title": "Rewritten", "summary": "Shortened"}
    p = ScriptedProvider(call("research_export", items=[changed], output_format="csv"), ModelResponse(text="Done"))
    s = session(p)
    s.sources = [original]
    record = s.turn("Xuất danh sách nguồn gốc")
    artifact = next(iter(s.artifacts.artifacts.values()))
    assert list(csv.DictReader(io.StringIO(artifact["content"]))) == [{**original, "source": "example.com"}]
    assert record["rounds"][0]["tool_calls"][0]["args"]["items"] == [changed]
    assert record["tool_events"][0]["args"]["items"] == [original]


def test_clarify_stops_before_later_tool_calls(monkeypatch):
    calls = []
    monkeypatch.setitem(TOOL_FUNCTIONS, "papers", lambda **kw: calls.append(kw))
    p = ScriptedProvider(ModelResponse(tool_calls=[ToolCall("clarify", {"question": "URL?", "response_type": "text"}), ToolCall("papers", {"query": "x"})]))
    result = session(p).turn("Đọc bài này")
    assert result["status"] == "waiting_for_user"
    assert calls == []


def test_repeated_tool_calls_stop_without_duplicate_execution(monkeypatch):
    count = []
    monkeypatch.setitem(TOOL_FUNCTIONS, "papers", lambda **kw: count.append(1) or {"items": []})
    p = ScriptedProvider(call("papers", query="AI"), call("papers", query="AI"))
    result = session(p).turn("Tìm AI")
    assert result["status"] == "stopped" and count == [1]


def test_group_dataset_has_exactly_five_single_and_five_multi():
    import json
    from pathlib import Path
    data = json.loads((Path(__file__).parents[1] / "data/eval_group.json").read_text(encoding="utf-8"))
    cases = data["cases"]
    assert len(cases) == len({c["id"] for c in cases}) == 10
    assert sum("query" in c for c in cases) == sum("turns" in c for c in cases) == 5
    assert all(c["phase"] == "B" and c["metadata"]["what_it_tests"] for c in cases)
    assert any(call["name"] == "research_export" for c in cases for call in c["expect"].get("tool_calls", []))
