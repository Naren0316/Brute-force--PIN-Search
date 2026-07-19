"""
entropy.py
----------
PIN strength scoring: combines Shannon entropy of the digit sequence with
a pattern-class penalty from pattern_engine.classify_pin, producing a
single 0-100 strength score and a human-readable risk tier.
"""

import math
from dataclasses import dataclass

from .pattern_engine import PatternCategory, classify_pin
from . import config


@dataclass
class StrengthReport:
    pin: str
    shannon_entropy_bits: float
    pattern_category: PatternCategory
    pattern_weight: float
    strength_score: float  # 0 (worst) - 100 (best)
    risk_tier: str


def shannon_entropy(pin: str) -> float:
    """Shannon entropy (bits) of the digit distribution within the PIN."""
    freq: dict = {}
    for ch in pin:
        freq[ch] = freq.get(ch, 0) + 1
    n = len(pin)
    entropy = -sum((count / n) * math.log2(count / n) for count in freq.values())
    return round(entropy, 4)


def _risk_tier(score: float) -> str:
    if score < 20:
        return "CRITICAL"
    if score < 45:
        return "WEAK"
    if score < 70:
        return "MODERATE"
    return "STRONG"


def analyze(pin: str) -> StrengthReport:
    """Produce a full strength report for a single 4-digit PIN."""
    match = classify_pin(pin)
    ent = shannon_entropy(pin)

    entropy_component = (ent / config.MAX_SHANNON_ENTROPY_BITS) * config.ENTROPY_SCORE_WEIGHT
    pattern_penalty = (match.weight / 100.0) * config.PATTERN_SCORE_WEIGHT
    pattern_component = config.PATTERN_SCORE_WEIGHT - pattern_penalty

    score = max(0.0, min(100.0, entropy_component + pattern_component))

    return StrengthReport(
        pin=pin,
        shannon_entropy_bits=ent,
        pattern_category=match.category,
        pattern_weight=match.weight,
        strength_score=round(score, 2),
        risk_tier=_risk_tier(score),
    )
