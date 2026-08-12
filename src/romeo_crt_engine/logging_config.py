from __future__ import annotations

import json
import logging
from collections.abc import Mapping
from typing import Any


def configure_logging(level: int = logging.INFO) -> None:
    """Configure a deterministic process-wide baseline without provider coupling."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        force=True,
    )


def log_event(
    logger: logging.Logger,
    event: str,
    *,
    level: int = logging.INFO,
    fields: Mapping[str, Any] | None = None,
) -> None:
    """Emit a structured JSON event suitable for later ingestion by any log backend."""
    if not event:
        raise ValueError("event must not be empty")
    if fields and "event" in fields:
        raise ValueError("event is a reserved structured-log field")
    payload: dict[str, Any] = dict(fields or {})
    payload["event"] = event
    logger.log(level, json.dumps(payload, sort_keys=True, default=str, separators=(",", ":")))
