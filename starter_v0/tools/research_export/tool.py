from __future__ import annotations

import csv
import io
from typing import Any
from urllib.parse import urlsplit

from tools._shared import domain, err


COLUMNS = ("title", "url", "source", "summary")


def research_export(
    items: list[dict[str, Any]] | None = None,
    output_format: str = "markdown",
    title: str = "",
) -> dict[str, Any]:
    """Serialize existing research sources in memory; never fetch or write files."""
    try:
        if output_format not in ("markdown", "csv"):
            raise ValueError("output_format must be 'markdown' or 'csv'")
        if not isinstance(title, str):
            raise ValueError("title must be a string")
        if not isinstance(items, list) or not items:
            raise ValueError("items must be a non-empty list of source objects")

        rows: list[dict[str, str]] = []
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                raise ValueError(f"items[{index}] must be an object")
            for field in COLUMNS:
                value = item.get(field, "")
                if not isinstance(value, str):
                    raise ValueError(f"items[{index}].{field} must be a string")
                if field in ("title", "url") and not value.strip():
                    raise ValueError(f"items[{index}].{field} is required")
            url = item["url"]
            parsed = urlsplit(url)
            if (
                parsed.scheme not in ("http", "https")
                or not parsed.hostname
                or any(char.isspace() for char in url)
            ):
                raise ValueError(f"items[{index}].url must be an HTTP(S) source URL")
            rows.append({
                "title": item["title"],
                "url": url,
                "source": item.get("source") or domain(url),
                "summary": item.get("summary", ""),
            })

        if output_format == "csv":
            buffer = io.StringIO(newline="")
            writer = csv.DictWriter(buffer, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
            content = buffer.getvalue()
            extension, mime_type = "csv", "text/csv; charset=utf-8"
        else:
            parts = [f"# {title.strip() or 'Research Briefing'}"]
            for index, row in enumerate(rows, start=1):
                parts.append(
                    f"## {index}. {row['title']}\n\n"
                    f"{row['summary']}\n\n"
                    f"Source: {row['source']}\n\nURL: <{row['url']}>"
                )
            content = "\n\n".join(parts) + "\n"
            extension, mime_type = "md", "text/markdown; charset=utf-8"

        return {
            "tool": "research_export",
            "filename": f"research_brief.{extension}",
            "mime_type": mime_type,
            "content": content,
            "item_count": len(rows),
        }
    except Exception as exc:
        return err("research_export", exc)
