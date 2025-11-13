# app/services/analysis.py

from collections import Counter
import re
from typing import Dict, Any

def rule_based_analyze(text: str) -> Dict[str, Any]:
    # --- 0) 기본 통계 ---
    paragraphs = [p for p in text.split("\n") if p.strip()]
    num_paragraphs = len(paragraphs)

    sentences = re.split(r"[.?!…]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    num_sentences = len(sentences)

    total_chars = sum(len(s) for s in sentences)
    avg_sentence_len = total_chars / num_sentences if num_sentences else 0

    quote_chars = sum(ch == "“" or ch == "”" or ch == '"' for ch in text)
    quote_ratio = quote_chars / total_chars if total_chars else 0

    stats = {
        "num_paragraphs": num_paragraphs,
        "num_sentences": num_sentences,
        "avg_sentence_len": avg_sentence_len,
        "quote_ratio": quote_ratio,
    }

    # --- 1) 장르 점수(대충 예시용) ---
    # 키워드 몇 개로 장르 추정 (AI 없이 간이 버전)
    lower = text.lower()
    genre_label = "미분류"
    if any(k in lower for k in ["황제", "공작", "기사", "마법"]):
        genre_label = "판타지(추정)"
    if any(k in lower for k in ["왕자", "사랑", "키스", "데이트"]):
        genre_label = "로맨스(추정)"

    genre_score = 75.0  # 일단 고정값 / 나중에 AI가 바꾸게 함

    # --- 2) 스타일 점수 ---
    # 문장이 너무 길면 감점, 너무 짧아도 감점하는 식의 간단 규칙
    style_score = 80.0
    if avg_sentence_len > 40:
        style_score -= 5
    if avg_sentence_len > 60:
        style_score -= 5
    if quote_ratio < 0.01:
        style_score -= 5

    # --- 3) 캐릭터성 / 시장성 / 개연성 점수 (지금은 하드코딩 + 약간만 규칙) ---
    character_score = 70.0 + quote_ratio * 20  # 대사 비율을 캐릭터성에 조금 반영
    if character_score > 90:
        character_score = 90.0

    marketability_score = 68.0  # 우선은 고정값
    plausibility_score = 65.0   # 우선은 고정값

    # --- 4) 장점/단점/문체 특징 문구 (임시 문장) ---
    strengths = []
    improvements = []
    style_traits = []

    # 장점 예시
    if num_paragraphs >= 3:
        strengths.append("문단이 적절히 나뉘어 있어 가독성이 좋습니다.")
    if quote_ratio > 0.03:
        strengths.append("대사 비율이 있어서 캐릭터의 감정이 잘 드러납니다.")

    # 단점 예시
    if avg_sentence_len > 50:
        improvements.append("문장 길이가 다소 길어 숨을 고르기 어렵습니다. 몇 문장을 쪼개 보세요.")
    if quote_ratio < 0.01:
        improvements.append("대사가 적어 인물의 개성이 약하게 느껴집니다.")

    # 문체 특징 예시
    if avg_sentence_len >= 40:
        style_traits.append("긴 문장을 선호하는 편으로, 서정적인 느낌을 줄 수 있습니다.")
    else:
        style_traits.append("짧은 문장이 많아 템포감 있는 전개를 보여줍니다.")

    if num_paragraphs > 10:
        style_traits.append("문단이 자주 나뉘어, 호흡이 빠른 편입니다.")

    # --- 5) 총점 (지금은 단순 평균) ---
    total_score = (genre_score + style_score +
                   character_score + marketability_score +
                   plausibility_score) / 5.0

    return {
        "stats": stats,
        "scores": {
            "total": total_score,
            "genre": genre_score,
            "style": style_score,
            "character": character_score,
            "marketability": marketability_score,
            "plausibility": plausibility_score,
        },
        "genre_label": genre_label,
        "style_traits": style_traits,
        "strengths": strengths,
        "improvements": improvements,
    }
