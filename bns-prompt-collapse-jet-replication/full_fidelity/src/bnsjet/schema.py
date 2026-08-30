"""JSON-schema validation with compact, actionable errors."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .errors import ConfigurationError
from .io import load_document


def validate_against_schema(
    document: dict[str, Any],
    schema_path: str | Path,
    *,
    document_name: str = "document",
) -> None:
    """Validate *document* and raise one aggregated error on failure."""

    schema = load_document(schema_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path))
    if not errors:
        return

    lines: list[str] = []
    for error in errors:
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        lines.append(f"- {location}: {error.message}")
    detail = "\n".join(lines)
    raise ConfigurationError(f"Invalid {document_name}:\n{detail}")


def project_schema(name: str) -> Path:
    """Return the schema installed with the source checkout.

    This project currently runs from a source checkout for production campaign
    preparation. The fallback path also works from an editable installation.
    """

    candidate = Path(__file__).resolve().parents[2] / "schemas" / name
    if candidate.is_file():
        return candidate
    raise ConfigurationError(f"Project schema not found: {candidate}")
