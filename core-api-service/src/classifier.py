"""
AI-based article category classifier.

Now uses hybrid semantic + keyword approach:
- Semantic: sentence-transformers multilingual MiniLM embeddings + cosine similarity to category prototypes
- Keyword: fall back when semantic confidence low
"""

import re
from typing import Optional, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer, util


# Category prototypes in Vietnamese (short descriptions)
CATEGORY_DESCRIPTIONS = {
    "Kinh doanh": "Kinh tế, tài chính, doanh nghiệp, chứng khoán, đầu tư, thị trường",
    "Công nghệ": "Công nghệ, AI, phần mềm, internet, thiết bị, kỹ thuật số",
    "Thể thao": "Thể thao, bóng đá, giải đấu, vận động viên, trận đấu",
    "Giải trí": "Giải trí, phim ảnh, âm nhạc, nghệ sĩ, showbiz, thời trang",
    "Chính trị": "Chính trị, chính phủ, quốc hội, chính sách, ngoại giao, an ninh",
}

# Keyword fallback mapping (Vietnamese)
CATEGORY_KEYWORDS = {
    "Kinh doanh": [
        "kinh tế", "doanh nghiệp", "thị trường", "chứng khoán", "đầu tư",
        "ngân hàng", "tài chính", "startup", "cổ phiếu", "bất động sản", "thương mại"
    ],
    "Công nghệ": [
        "công nghệ", "ai", "trí tuệ nhân tạo", "phần mềm", "internet", "kỹ thuật số",
        "điện thoại", "laptop", "blockchain", "robot", "mạng", "data"
    ],
    "Thể thao": [
        "bóng đá", "thể thao", "giải đấu", "cầu thủ", "huấn luyện", "trận đấu",
        "olympic", "sea games", "v-league", "world cup"
    ],
    "Giải trí": [
        "giải trí", "phim", "điện ảnh", "ca sĩ", "âm nhạc", "nghệ sĩ", "show",
        "concert", "fashion", "thời trang", "kpop", "vpop"
    ],
    "Chính trị": [
        "chính trị", "chính phủ", "quốc hội", "thủ tướng", "bộ trưởng", "nghị định",
        "luật", "ngoại giao", "chính sách", "an ninh", "quốc phòng"
    ],
}


# Load model once (shared across worker)
_MODEL = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
_CATEGORY_EMB = {
    cat: _MODEL.encode(desc, convert_to_tensor=True)
    for cat, desc in CATEGORY_DESCRIPTIONS.items()
}


def _semantic_classify(text: str) -> Tuple[str, float]:
    emb = _MODEL.encode(text, convert_to_tensor=True)
    scores = {
        cat: util.cos_sim(emb, proto_emb).item()
        for cat, proto_emb in _CATEGORY_EMB.items()
    }
    best_cat = max(scores.items(), key=lambda x: x[1])
    return best_cat[0], float(best_cat[1])


def _keyword_classify(text: str) -> Tuple[str, int]:
    scores = {}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for kw in keywords:
            kw_lower = kw.lower()
            # weight occurrences
            score += text.count(kw_lower)
        scores[cat] = score
    best_cat = max(scores.items(), key=lambda x: x[1])
    return best_cat[0], best_cat[1]


def classify_article(title: str, summary: Optional[str] = None, content: Optional[str] = None) -> str:
    """Hybrid semantic + keyword classification.

    - Build a short text bundle from title + summary + content (first 800 chars)
    - Semantic: sentence-transformers similarity to category prototypes
    - If semantic confidence below threshold, fall back to keywords
    """
    text_parts = [title or ""]
    if summary:
        text_parts.append(summary)
    if content:
        text_parts.append(content[:800])

    text_full = " ".join(text_parts).strip()
    text_clean = re.sub(r"[^\w\s]", " ", text_full.lower())
    text_clean = re.sub(r"\s+", " ", text_clean)

    # Semantic step
    semantic_cat, semantic_score = _semantic_classify(text_clean)

    # Threshold: if similarity < 0.28, use keyword fallback (tuneable)
    if semantic_score >= 0.28:
        return semantic_cat

    # Keyword fallback
    kw_cat, kw_score = _keyword_classify(text_clean)
    if kw_score > 0:
        return kw_cat

    return "Khác"


def classify_with_confidence(title: str, summary: Optional[str] = None, content: Optional[str] = None) -> tuple[str, float]:
    text_parts = [title or ""]
    if summary:
        text_parts.append(summary)
    if content:
        text_parts.append(content[:800])
    text_full = " ".join(text_parts).strip()
    text_clean = re.sub(r"[^\w\s]", " ", text_full.lower())
    text_clean = re.sub(r"\s+", " ", text_clean)

    semantic_cat, semantic_score = _semantic_classify(text_clean)
    if semantic_score >= 0.28:
        return semantic_cat, semantic_score

    kw_cat, kw_score = _keyword_classify(text_clean)
    if kw_score > 0:
        return kw_cat, 0.2  # low confidence but non-zero

    return "Khác", 0.0
