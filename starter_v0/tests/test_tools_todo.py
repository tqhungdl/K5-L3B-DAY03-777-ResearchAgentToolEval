"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import csv
from copy import deepcopy
from importlib import import_module
import io

import pytest

from artifact_store import ArtifactStore, CURRENT_ARTIFACTS

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    result = TOOL_FUNCTIONS["clarify"](response_type="choice", options=["A", "B"])
    assert result["tool"] == "ask_user"
    assert result["response_type"] == "choice"
    assert result["options"] == ["A", "B"]
    assert result["awaiting_user"] is True
    # pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    result = TOOL_FUNCTIONS["format"](items=[{"section": "A"}, {"section": "B"}, {"section": "A"}], template="bullets")
    # pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    result = TOOL_FUNCTIONS["format"](items=[{"text": "Item 1"}, {"text": "Item 2"}], template="thread")
    # pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    result = TOOL_FUNCTIONS["format"](items=[], template="bullets")
    # pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test_chat_id")
    calls = fake_http(FakeResponse({"ok": True, "result": {"message_id": 123}}))

    result = TOOL_FUNCTIONS["send"](text="Bản tin demo", confirmed=True)
    assert result["status"] == "sent"
    # pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))
    result = TOOL_FUNCTIONS["send"](text="Bản tin demo", confirmed=True)
    # pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": []}))
    result = TOOL_FUNCTIONS["lookup"](query="OpenAI news", topic="news", max_results=3)
    # pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"data": {"markdown": "## T\nSummary", "metadata": {"title": "T", "sourceURL": "https://example.com"}}}))
    result = TOOL_FUNCTIONS["fetch"](url="https://example.com")
    assert result["items"][0]["title"] == "T"
    assert result["items"][0]["url"] == "https://example.com"
    assert result["items"][0]["source"] == "example.com"
    assert "Summary" in result["items"][0]["summary"]
    # pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    long_markdown = "x" * 5000
    calls = fake_http(FakeResponse({"data": {"markdown": long_markdown, "metadata": {"title": "T", "sourceURL": "https://example.com"}}}))
    result = TOOL_FUNCTIONS["fetch"](url="https://example.com")
    # pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    monkeypatch.setenv("RAPIDAPI_TWITTER_HOST", "twitter-api45.p.rapidapi.com")
    calls = fake_http(FakeResponse({"timeline": [
        {"tweet_id": "1", "screen_name": "user1"},
        {"tweet_id": "2", "screen_name": "user2"},
        {"tweet_id": "3", "screen_name": "user3"},
        {"tweet_id": "4", "screen_name": "user4"},
        {"tweet_id": "5", "screen_name": "user5"},
        {"tweet_id": "6", "screen_name": "user6"},
        {"screen_name": "user7"},  # missing tweet_id
    ]}))
    result = TOOL_FUNCTIONS["timeline"](screenname="user1", limit=3)

    assert len(result["items"]) == 3
    assert [item["url"] for item in result["items"]] == [
        "https://x.com/user1/status/1",
        "https://x.com/user2/status/2",
        "https://x.com/user3/status/3",
    ]
    # pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    monkeypatch.setenv("RAPIDAPI_TWITTER_HOST", "twitter-api45.p.rapidapi.com")
    calls = fake_http(FakeResponse({"results": []}))
    result = TOOL_FUNCTIONS["social_search"](query="OpenAI", search_type="Latest")
    assert result["tool"] == "search_tweets"
    assert result["search_type"] == "Latest"
    # pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    result = TOOL_FUNCTIONS["policy"](query="")
    # pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    result = TOOL_FUNCTIONS["policy"](query="privacy", policy_area="data_privacy")
    # pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    result = TOOL_FUNCTIONS["policy"](query="source_citation")
    
    # pytest.skip(TODO)


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

def test_research_export_markdown_preserves_sources_and_full_summaries() -> None:
    summary = "Nghiên cứu AI tiếng Việt. " * 30
    result = TOOL_FUNCTIONS["research_export"](
        items=[
            {"title": "Bài A", "url": "https://example.com/a", "summary": summary},
            {"title": "Bài B", "url": "https://example.com/b", "source": "Nhóm B"},
        ],
        title="Bản tin nghiên cứu",
    )

    assert result["tool"] == "research_export"
    assert result["filename"] == "research_brief.md"
    assert result["mime_type"] == "text/markdown; charset=utf-8"
    assert result["item_count"] == 2
    content = result["content"]
    assert content.startswith("# Bản tin nghiên cứu\n")
    assert "## 1. Bài A" in content and "## 2. Bài B" in content
    assert content.index("Bài A") < content.index("Bài B")
    assert summary in content
    assert "Source: example.com" in content
    assert "Source: Nhóm B" in content
    assert "<https://example.com/a>" in content
    assert "<https://example.com/b>" in content


def test_research_export_csv_roundtrips_unicode_commas_quotes_and_newlines() -> None:
    items = [{
        "title": 'Bài báo, "AI"',
        "url": "https://example.com/paper?a=1&b=2",
        "source": "Nguồn nghiên cứu",
        "summary": 'Dòng 1, có dấu phẩy\nDòng 2: "kết quả"',
        "authors": ["Extra metadata is not exported"],
    }]
    result = TOOL_FUNCTIONS["research_export"](
        items=items, output_format="csv", title="Not a CSV row",
    )

    assert result["filename"] == "research_brief.csv"
    assert result["mime_type"] == "text/csv; charset=utf-8"
    assert result["item_count"] == 1
    reader = csv.DictReader(io.StringIO(result["content"], newline=""))
    assert reader.fieldnames == ["title", "url", "source", "summary"]
    assert list(reader) == [{key: items[0][key] for key in reader.fieldnames}]
    assert result["content"].encode("utf-8").decode("utf-8") == result["content"]


@pytest.mark.parametrize("kwargs, message", [
    ({}, "non-empty list"),
    ({"items": []}, "non-empty list"),
    ({"items": "not a list"}, "non-empty list"),
    ({"items": [None]}, "must be an object"),
    ({"items": [{"url": "https://example.com"}]}, "title is required"),
    ({"items": [{"title": "   ", "url": "https://example.com"}]}, "title is required"),
    ({"items": [{"title": "T"}]}, "url is required"),
    ({"items": [{"title": "T", "url": "file:///tmp/source"}]}, "HTTP(S)"),
    ({"items": [{"title": "T", "url": "https://"}]}, "HTTP(S)"),
    ({"items": [{"title": "T", "url": "https://example.com/a b"}]}, "HTTP(S)"),
    ({"items": [{"title": "T", "url": "https://example.com", "summary": None}]}, "summary must be a string"),
    ({"items": [{"title": "T", "url": "https://example.com", "source": 42}]}, "source must be a string"),
    ({"output_format": "pdf"}, "output_format"),
    ({"output_format": []}, "output_format"),
    ({"title": None}, "title must be a string"),
])
def test_research_export_bad_input_returns_error_dict(kwargs, message) -> None:
    result = TOOL_FUNCTIONS["research_export"](**kwargs)

    assert result["tool"] == "research_export"
    assert result["error"] == "ValueError"
    assert message in result["message"]
    assert "content" not in result


def test_research_export_serialization_failure_returns_error_dict(monkeypatch) -> None:
    module = import_module("tools.research_export.tool")

    def broken_writer(*args, **kwargs):
        raise OSError("serialization unavailable")

    monkeypatch.setattr(module.csv, "DictWriter", broken_writer)
    result = TOOL_FUNCTIONS["research_export"](
        items=[{"title": "T", "url": "https://example.com"}], output_format="csv",
    )

    assert result == {
        "tool": "research_export",
        "error": "OSError",
        "message": "serialization unavailable",
    }


@pytest.mark.parametrize("output_format", ["markdown", "csv"])
def test_research_export_does_not_mutate_input(output_format) -> None:
    items = [{"title": "T", "url": "https://www.example.com/a", "authors": ["A"]}]
    before = deepcopy(items)

    result = TOOL_FUNCTIONS["research_export"](items=items, output_format=output_format)

    assert "error" not in result
    assert items == before


def test_research_export_defaults_support_minimal_source_item() -> None:
    result = TOOL_FUNCTIONS["research_export"](
        items=[{"title": "T", "url": "https://example.com"}],
    )

    assert result["content"].startswith("# Research Briefing\n")
    assert "Source: example.com" in result["content"]
    assert result["item_count"] == 1


# ---------------- send_document (CP4/CP5 extension) ----------------

@pytest.fixture
def telegram(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-secret")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100000")


def _document_store():
    store = ArtifactStore()
    aid = store.add(TOOL_FUNCTIONS["research_export"](
        items=[{"title": "Nghiên cứu", "url": "https://example.com/paper", "summary": "Kết quả tiếng Việt"}],
        output_format="csv",
    ))
    return store, aid


def test_document_upload_uses_exact_export_bytes_and_no_duplicate(telegram, fake_http):
    store, aid = _document_store()
    http = fake_http(FakeResponse({"ok": True, "result": {"message_id": 123}}))
    token = CURRENT_ARTIFACTS.set(store)
    try:
        result = TOOL_FUNCTIONS["send_document"](artifact_id=aid, confirmed=True)
        second = TOOL_FUNCTIONS["send_document"](artifact_id=aid, confirmed=True)
    finally:
        CURRENT_ARTIFACTS.reset(token)
    assert result["status"] == "sent" and result["message_id"] == 123
    assert result["sha256"] == store.artifacts[aid]["sha256"]
    assert second["status"] == "already_sent"
    assert len(http) == 1
    assert http[0]["data"] == {"chat_id": "-100000", "caption": ""}
    assert http[0]["files"]["document"] == ("research_brief.csv", store.artifacts[aid]["content"].encode("utf-8"), "text/csv")
    assert http[0]["url"].endswith("/sendDocument")


@pytest.mark.parametrize("confirmed", [False, "true", 1, None])
def test_document_without_boolean_confirmation_never_calls_network(confirmed, fake_http):
    http = fake_http(FakeResponse())
    result = TOOL_FUNCTIONS["send_document"](artifact_id="x", confirmed=confirmed)
    assert result["status"] == "needs_confirmation"
    assert http == []


def test_document_rejects_artifact_from_another_session(telegram, fake_http):
    one, aid = _document_store()
    two = ArtifactStore()
    http = fake_http(FakeResponse())
    token = CURRENT_ARTIFACTS.set(two)
    try:
        result = TOOL_FUNCTIONS["send_document"](artifact_id=aid, confirmed=True)
    finally:
        CURRENT_ARTIFACTS.reset(token)
    assert result["error"] == "ValueError"
    assert http == []


def test_document_missing_config_returns_error_without_request(fake_http):
    store, aid = _document_store()
    http = fake_http(FakeResponse())
    token = CURRENT_ARTIFACTS.set(store)
    try:
        result = TOOL_FUNCTIONS["send_document"](artifact_id=aid, confirmed=True)
    finally:
        CURRENT_ARTIFACTS.reset(token)
    assert result["error"] == "ConfigurationError"
    assert http == []


def test_send_rejects_telegram_ok_false(telegram, fake_http):
    fake_http(FakeResponse({"ok": False}))
    result = TOOL_FUNCTIONS["send"](text="Bản tin demo", confirmed=True)
    assert result["error"] == "TelegramError"
    assert result.get("status") != "sent"


def test_send_network_error_does_not_leak_bot_token(telegram, fake_http):
    fake_http(RuntimeError("https://api.telegram.org/bottest-secret/sendMessage"))
    result = TOOL_FUNCTIONS["send"](text="Bản tin demo", confirmed=True)
    assert "error" in result
    assert "test-secret" not in str(result)
