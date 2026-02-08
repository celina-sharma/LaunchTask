# src/evaluation/rag_eval.py

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _clean(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text.strip()


def context_match_score(context: str, answer: str) -> float:
    """
    Measures how much the answer overlaps with retrieved context
    """
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(
        [_clean(context), _clean(answer)]
    )

    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(float(similarity), 3)


def faithfulness_score(context: str, answer: str) -> float:
    """
    Penalize facts not present in context
    """
    context_words = set(_clean(context).split())
    answer_words = set(_clean(answer).split())

    if not answer_words:
        return 0.0

    grounded_words = answer_words.intersection(context_words)
    score = len(grounded_words) / len(answer_words)

    return round(score, 3)


def detect_hallucination(faithfulness: float, threshold: float = 0.55) -> bool:
    """
    If faithfulness is low → hallucination likely
    """
    return faithfulness < threshold


def evaluate_answer(question: str, context: str, answer: str) -> dict:
    """
    Full evaluation pipeline
    """
    context_score = context_match_score(context, answer)
    faithfulness = faithfulness_score(context, answer)
    hallucinated = detect_hallucination(faithfulness)

    confidence = round(
        (0.6 * faithfulness + 0.4 * context_score), 3
    )

    return {
        "context_match": context_score,
        "faithfulness": faithfulness,
        "hallucination": hallucinated,
        "confidence": confidence
    }
