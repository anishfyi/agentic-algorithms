"""Structured output parsing and JSON repair for LLM responses."""

from __future__ import annotations

import json
import re

from pydantic import BaseModel, ValidationError


def extract_json_block(text: str) -> str:
    """Extract JSON from markdown fences or raw text. Time O(n)."""
    fenced = re.search(r"```(?:json)?\s*(\{[\s\S]*?\}|\[[\s\S]*?\])\s*```", text)
    if fenced:
        return fenced.group(1)
    brace = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", text)
    return brace.group(1) if brace else text.strip()


def repair_json(text: str) -> str:
    """Best-effort JSON repair for common LLM mistakes. Time O(n)."""
    cleaned = extract_json_block(text)
    cleaned = cleaned.replace("'", '"')
    cleaned = re.sub(r",\s*}", "}", cleaned)
    cleaned = re.sub(r",\s*]", "]", cleaned)
    return cleaned


def parse_structured_output[T: BaseModel](text: str, model: type[T]) -> T:
    """Parse and validate LLM output into a Pydantic model. Time O(n)."""
    try:
        payload = json.loads(extract_json_block(text))
    except json.JSONDecodeError:
        payload = json.loads(repair_json(text))
    return model.model_validate(payload)


def validation_errors[T: BaseModel](text: str, model: type[T]) -> list[str]:
    """Return validation error messages without raising. Time O(n)."""
    try:
        parse_structured_output(text, model)
        return []
    except (json.JSONDecodeError, ValidationError) as exc:
        return [str(exc)]
