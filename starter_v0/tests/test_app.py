from pathlib import Path

from streamlit.testing.v1 import AppTest

import chat
from chat_runtime import ChatSession
from providers.base import ModelResponse, ToolCall


class ExportProvider:
    def __init__(self):
        self.calls = 0

    def complete(self, *args, **kwargs):
        self.calls += 1
        if self.calls == 1:
            return ModelResponse(tool_calls=[ToolCall("research_export", {"items": [{"title": "Paper", "url": "https://example.com/paper"}], "output_format": "csv"})])
        return ModelResponse(text="Đã xuất CSV.")


def test_ui_export_and_rerender_do_not_repeat_provider_calls(monkeypatch, tmp_path):
    provider = ExportProvider()
    session = ChatSession(provider, system_prompt="test", tools=[], transcripts_dir=tmp_path)
    monkeypatch.setattr(chat, "create_session", lambda: session)
    at = AppTest.from_file(str(Path(__file__).parents[1] / "app.py")).run()
    assert not at.exception and len(at.chat_input) == 1
    at.chat_input[0].set_value("Xuất nguồn thành CSV").run()
    assert not at.exception
    assert len(at.get("download_button")) == 1
    assert len(session.artifacts.artifacts) == 1
    assert provider.calls == 2
    at.run()
    assert provider.calls == 2
    assert session.path.is_file()


def test_ui_cancel_confirmation_never_calls_provider_or_network(monkeypatch, tmp_path):
    provider = ExportProvider()
    session = ChatSession(provider, system_prompt="test", tools=[], transcripts_dir=tmp_path)
    session.pending = {"tool": "send_document", "args": {"artifact_id": "fixture"}, "destination": "-100", "digest": "fixture"}
    monkeypatch.setattr(chat, "create_session", lambda: session)
    at = AppTest.from_file(str(Path(__file__).parents[1] / "app.py")).run()
    cancel = next(button for button in at.button if button.label == "Hủy gửi")
    cancel.click().run()
    assert not at.exception
    assert session.pending is None and provider.calls == 0
    assert session.transcript["turns"][-1]["assistant_text"] == "Đã hủy gửi."
