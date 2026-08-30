"""Safe, deterministic file I/O helpers."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

import yaml

from .errors import ConfigurationError


def load_document(path: str | Path) -> dict[str, Any]:
    """Load a YAML or JSON mapping from *path*.

    The top-level value must be a mapping because all project schemas use named
    fields. Empty files and sequence-valued documents are rejected explicitly.
    """

    source = Path(path).expanduser().resolve()
    if not source.is_file():
        raise ConfigurationError(f"Document does not exist: {source}")

    try:
        text = source.read_text(encoding="utf-8")
        if source.suffix.lower() == ".json":
            data = json.loads(text)
        else:
            data = yaml.safe_load(text)
    except (OSError, json.JSONDecodeError, yaml.YAMLError) as exc:
        raise ConfigurationError(f"Could not parse {source}: {exc}") from exc

    if not isinstance(data, dict):
        raise ConfigurationError(f"Top-level document must be a mapping: {source}")
    return data


def dump_json_atomic(path: str | Path, value: Any) -> Path:
    """Atomically write canonical, human-readable JSON."""

    destination = Path(path).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"

    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
        text=True,
    )
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, destination)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise
    return destination


def resolve_relative(document_path: str | Path, referenced_path: str | Path) -> Path:
    """Resolve a path relative to the document containing it."""

    document = Path(document_path).expanduser().resolve()
    reference = Path(referenced_path).expanduser()
    if reference.is_absolute():
        return reference.resolve()
    return (document.parent / reference).resolve()
