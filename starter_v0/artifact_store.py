"""Immutable exports scoped to one chat session, never a shared global cache."""
from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass, field
import hashlib
from typing import Any
from uuid import uuid4


@dataclass
class ArtifactStore:
    artifacts: dict[str, dict[str, Any]] = field(default_factory=dict)
    sent: set[str] = field(default_factory=set)

    def add(self, result: dict[str, Any]) -> str:
        artifact_id = uuid4().hex
        self.artifacts[artifact_id] = {
            key: result[key] for key in ("filename", "mime_type", "content", "item_count")
        }
        self.artifacts[artifact_id]["sha256"] = hashlib.sha256(result["content"].encode("utf-8")).hexdigest()
        return artifact_id


CURRENT_ARTIFACTS: ContextVar[ArtifactStore | None] = ContextVar("research_artifacts", default=None)
