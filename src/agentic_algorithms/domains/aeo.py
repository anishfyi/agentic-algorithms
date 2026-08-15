"""AEO (Answer Engine Optimization) algorithms for AI search visibility."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class AeoPageInput:
    title: str
    body: str
    schema_types: list[str]
    has_faq_section: bool = False
    last_updated_iso: str | None = None
    author_credentials: str | None = None


_REQUIRED_SCHEMA_FIELDS = {
    "Organization": {"name", "url"},
    "Product": {"name", "description"},
    "FAQPage": {"mainEntity"},
    "Article": {"headline", "author", "datePublished"},
}


def schema_completeness_score(
    schema_types: list[str], present_fields: dict[str, set[str]]
) -> float:
    """Score structured data completeness for AEO. Time O(types), space O(1)."""
    if not schema_types:
        return 0.0
    scores: list[float] = []
    for schema_type in schema_types:
        required = _REQUIRED_SCHEMA_FIELDS.get(schema_type, set())
        if not required:
            scores.append(0.5)
            continue
        have = present_fields.get(schema_type, set())
        scores.append(len(required & have) / len(required))
    return sum(scores) / len(scores)


def faq_structure_score(body: str) -> float:
    """Score FAQ formatting (Q/A pairs, headings). Time O(n), space O(1)."""
    questions = len(re.findall(r"^#+\s*.+\?\s*$", body, flags=re.MULTILINE))
    questions += len(re.findall(r"<h[2-4][^>]*>.+\?</h", body, flags=re.IGNORECASE))
    qa_pairs = len(re.findall(r"^Q:\s*.+\nA:\s*.+", body, flags=re.MULTILINE))
    if questions == 0 and qa_pairs == 0:
        return 0.0
    return min(1.0, (questions + qa_pairs) / 5)


def citation_density_score(body: str) -> float:
    """Score citation-worthy signals: stats, dates, named entities. Time O(n)."""
    stats = len(re.findall(r"\b\d+(?:\.\d+)?%|\b\d{4}\b|\$\d+", body))
    citations = len(re.findall(r"\[[^\]]+\]\([^)]+\)|https?://", body))
    sentences = max(1, len(re.findall(r"[.!?]", body)))
    density = (stats + citations) / sentences
    return min(1.0, density / 0.5)


def snippet_answerability_score(title: str, body: str) -> float:
    """Score definitional snippet potential for answer engines. Time O(n)."""
    first_para = body.strip().split("\n\n")[0] if body.strip() else ""
    words = first_para.split()
    length_ok = 40 <= len(words) <= 80
    title_in_body = title.lower().split("|")[0].strip().lower() in first_para.lower()
    has_definition = any(
        phrase in first_para.lower() for phrase in (" is ", " are ", " means ", " refers to ")
    )
    score = 0.0
    if length_ok:
        score += 0.4
    if title_in_body:
        score += 0.3
    if has_definition:
        score += 0.3
    return score


def entity_coverage_score(body: str, target_entities: set[str]) -> float:
    """Fraction of target entities mentioned. Time O(e), space O(1)."""
    if not target_entities:
        return 0.0
    lower = body.lower()
    covered = sum(1 for entity in target_entities if entity.lower() in lower)
    return covered / len(target_entities)


def eeat_signal_score(page: AeoPageInput) -> float:
    """Experience, expertise, authority, trust proxy score. Time O(1)."""
    score = 0.0
    if page.author_credentials:
        score += 0.35
    if page.last_updated_iso:
        score += 0.25
    if page.schema_types:
        score += 0.2
    if page.has_faq_section:
        score += 0.2
    return min(1.0, score)


def aeo_overall(scores: dict[str, float]) -> float:
    weights = {
        "schema": 0.2,
        "faq": 0.15,
        "citations": 0.15,
        "snippet": 0.2,
        "entities": 0.15,
        "eeat": 0.15,
    }
    return sum(scores[key] * weight for key, weight in weights.items())


def aeo_page_score(
    page: AeoPageInput,
    *,
    present_fields: dict[str, set[str]] | None = None,
    target_entities: set[str] | None = None,
) -> dict[str, float]:
    """Composite AEO score breakdown with overall. Time O(n)."""
    fields = present_fields or {}
    entities = target_entities or set()
    scores = {
        "schema": schema_completeness_score(page.schema_types, fields),
        "faq": faq_structure_score(page.body),
        "citations": citation_density_score(page.body),
        "snippet": snippet_answerability_score(page.title, page.body),
        "entities": entity_coverage_score(page.body, entities),
        "eeat": eeat_signal_score(page),
    }
    scores["overall"] = aeo_overall(scores)
    return scores
