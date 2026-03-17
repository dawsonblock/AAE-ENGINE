"""repository_intelligence/indexing/full_text_indexer — BM25-style index."""
from __future__ import annotations

import logging
import math
import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

log = logging.getLogger(__name__)


@dataclass
class IndexDocument:
    """A document stored in the full-text index."""

    doc_id: str
    content: str
    file: str = ""
    language: str = ""
    tokens: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.tokens:
            self.tokens = _tokenize(self.content)


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z_]\w*", text.lower())


class FullTextIndexer:
    """Simple inverted-index full-text search over repository files.

    Uses a TF-IDF-inspired scoring function.
    """

    def __init__(self) -> None:
        self._docs: Dict[str, IndexDocument] = {}
        self._index: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
        self._df: Dict[str, int] = defaultdict(int)

    def add(self, doc: IndexDocument) -> None:
        self._docs[doc.doc_id] = doc
        freq: Dict[str, int] = {}
        for tok in doc.tokens:
            freq[tok] = freq.get(tok, 0) + 1
        for tok, count in freq.items():
            self._index[tok].append((doc.doc_id, count))
            self._df[tok] += 1

    def add_many(self, docs: List[IndexDocument]) -> None:
        for doc in docs:
            self.add(doc)

    def search(
        self, query: str, top_k: int = 10
    ) -> List[Tuple[str, float]]:
        """Return ``[(doc_id, score), …]`` ranked by relevance."""
        qtokens = _tokenize(query)
        N = len(self._docs)
        if N == 0 or not qtokens:
            return []
        scores: Dict[str, float] = defaultdict(float)
        for tok in qtokens:
            if tok not in self._index:
                continue
            idf = math.log((N + 1) / (self._df[tok] + 1)) + 1
            for doc_id, tf in self._index[tok]:
                doc = self._docs.get(doc_id)
                doc_len = len(doc.tokens) if doc else 1
                tf_norm = tf / (1 + 0.5 * doc_len / 100)
                scores[doc_id] += tf_norm * idf
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

    def get_doc(self, doc_id: str) -> Optional[IndexDocument]:
        return self._docs.get(doc_id)

    def stats(self) -> Dict:
        return {
            "documents": len(self._docs),
            "unique_tokens": len(self._index),
        }
