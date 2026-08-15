"""Search algorithms: BM25, TF-IDF, hybrid retrieval."""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field


def _tokenize(text: str) -> list[str]:
    return [token for token in re.split(r"[^a-z0-9]+", text.lower()) if token]


@dataclass
class SearchIndex:
    """In-memory inverted index with BM25 scoring."""

    documents: dict[str, str] = field(default_factory=dict)
    _postings: dict[str, dict[str, int]] = field(default_factory=lambda: defaultdict(dict))
    _doc_lengths: dict[str, int] = field(default_factory=dict)
    _avg_doc_length: float = 0.0
    _k1: float = 1.5
    _b: float = 0.75

    def add(self, doc_id: str, text: str) -> None:
        self.documents[doc_id] = text
        counts = Counter(_tokenize(text))
        self._doc_lengths[doc_id] = sum(counts.values())
        for term, freq in counts.items():
            self._postings[term][doc_id] = freq
        total_len = sum(self._doc_lengths.values())
        self._avg_doc_length = total_len / max(1, len(self._doc_lengths))

    def search(self, query: str, *, top_k: int = 10) -> list[tuple[str, float]]:
        """BM25 search. Time O(q * posting_list), space O(results)."""
        scores: dict[str, float] = defaultdict(float)
        query_terms = _tokenize(query)
        n_docs = len(self.documents)
        for term in query_terms:
            postings = self._postings.get(term, {})
            df = len(postings)
            if df == 0:
                continue
            idf = math.log(1 + (n_docs - df + 0.5) / (df + 0.5))
            for doc_id, tf in postings.items():
                doc_len = self._doc_lengths[doc_id]
                numerator = tf * (self._k1 + 1)
                denominator = tf + self._k1 * (
                    1 - self._b + self._b * doc_len / self._avg_doc_length
                )
                scores[doc_id] += idf * numerator / denominator
        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return ranked[:top_k]


def bm25_score(
    term_freq: int,
    doc_freq: int,
    total_docs: int,
    doc_length: int,
    avg_doc_length: float,
    *,
    k1: float = 1.5,
    b: float = 0.75,
) -> float:
    """Single-term BM25 contribution. Time O(1)."""
    idf = math.log(1 + (total_docs - doc_freq + 0.5) / (doc_freq + 0.5))
    numerator = term_freq * (k1 + 1)
    denominator = term_freq + k1 * (1 - b + b * doc_length / max(1.0, avg_doc_length))
    return idf * numerator / denominator


def tf_idf_vectorize(corpus: list[str]) -> list[dict[str, float]]:
    """TF-IDF vectors for a corpus. Time O(n * avg_len), space O(vocab)."""
    tokenized = [_tokenize(doc) for doc in corpus]
    df: Counter[str] = Counter()
    for tokens in tokenized:
        df.update(set(tokens))
    n_docs = len(corpus)
    vectors: list[dict[str, float]] = []
    for tokens in tokenized:
        tf = Counter(tokens)
        total = sum(tf.values()) or 1
        vector = {
            term: (count / total) * math.log((1 + n_docs) / (1 + df[term]))
            for term, count in tf.items()
        }
        vectors.append(vector)
    return vectors


def cosine_similarity_sparse(left: dict[str, float], right: dict[str, float]) -> float:
    """Cosine similarity for sparse vectors. Time O(unique terms)."""
    dot = sum(left[key] * right.get(key, 0.0) for key in left)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def hybrid_search_rrf(
    ranked_lists: list[list[str]],
    *,
    k: int = 60,
    top_n: int = 10,
) -> list[tuple[str, float]]:
    """Reciprocal Rank Fusion across multiple retrievers. Time O(lists * ranks)."""
    scores: dict[str, float] = defaultdict(float)
    for ranked in ranked_lists:
        for rank, doc_id in enumerate(ranked, start=1):
            scores[doc_id] += 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)[:top_n]


def faceted_filter(
    documents: list[dict[str, str]],
    facets: dict[str, set[str]],
) -> list[dict[str, str]]:
    """Filter documents by facet equality. Time O(n * facets)."""
    result = []
    for document in documents:
        if all(document.get(key) in values for key, values in facets.items()):
            result.append(document)
    return result
