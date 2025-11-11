# app/services/analysis.py
import re

_SENT_SPLIT = re.compile(r"[.!?…]+[\s\n]+")
_QUOTE = re.compile(r"[\"“”‘’]")

def rule_based_analyze(text: str):
    paragraphs = [p for p in text.splitlines() if p.strip()]
    sentences = [s for s in _SENT_SPLIT.split(text) if s.strip()]
    num_chars = len(text)
    num_paragraphs = len(paragraphs)
    num_sentences = len(sentences) or 1
    avg_sentence_len = sum(len(s) for s in sentences) / num_sentences
    quote_ratio = len(_QUOTE.findall(text)) / max(num_chars, 1)

    style_score = max(0, 100 - abs(avg_sentence_len - 40))
    genre_score = min(100, quote_ratio * 400)
    total = round((style_score * 0.5 + genre_score * 0.5), 1)

    strengths = []
    improvements = []
    if quote_ratio > 0.02: strengths.append("대사 비중이 적절함")
    else: improvements.append("대사 비중이 낮아 리듬이 단조로움")
    if avg_sentence_len < 30: strengths.append("짧은 문장 중심의 속도감")
    elif avg_sentence_len > 60: improvements.append("문장 길이가 길어 가독성 저하 가능")

    return {
        "stats": {
            "num_chars": num_chars,
            "num_paragraphs": num_paragraphs,
            "num_sentences": num_sentences,
            "avg_sentence_len": round(avg_sentence_len, 2),
            "quote_ratio": round(quote_ratio, 4),
        },
        "scores": {
            "style": round(style_score, 1),
            "genre": round(genre_score, 1),
            "total": total,
        },
        "strengths": strengths,
        "improvements": improvements,
    }
