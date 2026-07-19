"""
pattern_engine.py
------------------
Core pattern-intelligence engine for the PIN Security Research Platform.

Categorizes and scores 4-digit PIN patterns based on publicly documented
research into real-world PIN-selection behavior (repeated digits, birth
years, keypad shapes, sequences, etc.). This module only ever operates on
data supplied to it in-process -- it never contacts, targets, or interacts
with any real device, account, or authentication system.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class PatternCategory(str, Enum):
    TOP_VERIFIED = "Top Verified Common PINs"
    KEYPAD_PATTERN = "Keypad Geometric Pattern"
    REPEATED_DIGIT = "Repeated Single Digit (e.g. 1111)"
    SEQUENTIAL_ASC = "Ascending Sequence (e.g. 1234)"
    SEQUENTIAL_DESC = "Descending Sequence (e.g. 4321)"
    REPEATED_PAIR = "Repeated Pair (XYXY, e.g. 1212)"
    PALINDROME = "Palindrome (e.g. 1221)"
    EXTENDED_COMMON = "Extended Documented Common"
    YEAR = "Likely Year (1940-2029)"
    DATE_MMDD = "Date-like (MMDD)"
    RANDOM = "Uncategorized / Low-Frequency"


@dataclass
class PatternMatch:
    pin: str
    category: PatternCategory
    weight: float  # relative likelihood weight: higher = more commonly chosen


# Relative likelihood weights (0-100), calibrated so the most commonly
# chosen categories (per widely cited leaked-PIN frequency analyses)
# score highest. These are relative research-informed weights, not
# claims of exact real-world probability.
_CATEGORY_BASE_WEIGHT: Dict[PatternCategory, float] = {
    PatternCategory.TOP_VERIFIED: 100.0,
    PatternCategory.REPEATED_DIGIT: 85.0,
    PatternCategory.SEQUENTIAL_ASC: 80.0,
    PatternCategory.YEAR: 70.0,
    PatternCategory.SEQUENTIAL_DESC: 55.0,
    PatternCategory.REPEATED_PAIR: 50.0,
    PatternCategory.DATE_MMDD: 45.0,
    PatternCategory.KEYPAD_PATTERN: 40.0,
    PatternCategory.PALINDROME: 35.0,
    PatternCategory.EXTENDED_COMMON: 30.0,
    PatternCategory.RANDOM: 1.0,
}

TOP_VERIFIED_PINS = [
    "1234", "1111", "0000", "1212", "7777", "1004", "2000", "4444",
    "2222", "6969", "9999", "3333", "5555", "6666", "1122", "1313",
    "8888", "4321", "2001", "1010",
]

EXTENDED_COMMON_PINS = [
    "2580", "0007", "0070", "1984", "1999", "1919", "1972", "2020",
    "2021", "2323", "6789", "2468", "1357", "1230", "5201", "0101",
    "0808", "1231", "0704",
]

# Common phone-keypad geometric shapes: straight lines, columns, box corners
KEYPAD_PATTERNS = [
    "1470", "2580", "3690", "1256", "4569", "7896", "2589", "1590", "7539",
]


def _consecutive_diffs(pin: str) -> List[int]:
    return [(int(pin[i + 1]) - int(pin[i])) % 10 for i in range(3)]


def _is_sequential_asc(pin: str) -> bool:
    return _consecutive_diffs(pin) == [1, 1, 1]


def _is_sequential_desc(pin: str) -> bool:
    return _consecutive_diffs(pin) == [9, 9, 9]  # equivalent to -1 mod 10


def _is_repeated_digit(pin: str) -> bool:
    return len(set(pin)) == 1


def _is_repeated_pair(pin: str) -> bool:
    return pin[0] == pin[2] and pin[1] == pin[3] and pin[0] != pin[1]


def _is_palindrome(pin: str) -> bool:
    return pin == pin[::-1] and len(set(pin)) > 1


def _is_year(pin: str) -> bool:
    return 1940 <= int(pin) <= 2029


def _is_date_like(pin: str) -> bool:
    mm, dd = int(pin[:2]), int(pin[2:])
    return 1 <= mm <= 12 and 1 <= dd <= 31


def classify_pin(pin: str) -> PatternMatch:
    """Classify a single 4-digit PIN into its most likely selection pattern."""
    if not (len(pin) == 4 and pin.isdigit()):
        raise ValueError("PIN must be a 4-digit numeric string")

    if pin in TOP_VERIFIED_PINS:
        category = PatternCategory.TOP_VERIFIED
    elif pin in KEYPAD_PATTERNS:
        category = PatternCategory.KEYPAD_PATTERN
    elif _is_repeated_digit(pin):
        category = PatternCategory.REPEATED_DIGIT
    elif _is_sequential_asc(pin):
        category = PatternCategory.SEQUENTIAL_ASC
    elif _is_sequential_desc(pin):
        category = PatternCategory.SEQUENTIAL_DESC
    elif _is_repeated_pair(pin):
        category = PatternCategory.REPEATED_PAIR
    elif _is_palindrome(pin):
        category = PatternCategory.PALINDROME
    elif pin in EXTENDED_COMMON_PINS:
        category = PatternCategory.EXTENDED_COMMON
    elif _is_year(pin):
        category = PatternCategory.YEAR
    elif _is_date_like(pin):
        category = PatternCategory.DATE_MMDD
    else:
        category = PatternCategory.RANDOM

    return PatternMatch(pin=pin, category=category, weight=_CATEGORY_BASE_WEIGHT[category])


def build_priority_queue() -> List[PatternMatch]:
    """
    Classify the full 0000-9999 PIN space and sort by descending
    likelihood weight. This ordered candidate list is what the Day 2
    attack-simulation engine will consume, against a *local* simulated
    vault only.
    """
    all_pins = [f"{i:04d}" for i in range(10000)]
    matches = [classify_pin(p) for p in all_pins]
    matches.sort(key=lambda m: (-m.weight, m.pin))
    return matches


def category_breakdown() -> Dict[PatternCategory, int]:
    """Count how many PINs in the full 10,000-PIN space fall into each category."""
    counts: Dict[PatternCategory, int] = {c: 0 for c in PatternCategory}
    for i in range(10000):
        match = classify_pin(f"{i:04d}")
        counts[match.category] += 1
    return counts
