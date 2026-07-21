import pytest

from backend.pattern_engine import PatternCategory, category_breakdown, classify_pin


def test_top_verified_classified_correctly():
    assert classify_pin("1234").category == PatternCategory.TOP_VERIFIED
    assert classify_pin("0000").category == PatternCategory.TOP_VERIFIED


def test_sequential_ascending():
    assert classify_pin("2345").category == PatternCategory.SEQUENTIAL_ASC


def test_sequential_descending():
    assert classify_pin("9876").category == PatternCategory.SEQUENTIAL_DESC


def test_repeated_pair():
    assert classify_pin("2323").category == PatternCategory.REPEATED_PAIR


def test_year_pattern():
    assert classify_pin("1990").category == PatternCategory.YEAR


def test_random_pin_has_low_weight():
    result = classify_pin("8503")
    assert result.weight <= 40


def test_top_verified_outweighs_random():
    common = classify_pin("1234")
    rare = classify_pin("8503")
    assert common.weight > rare.weight


def test_invalid_pin_raises():
    with pytest.raises(ValueError):
        classify_pin("12a4")
    with pytest.raises(ValueError):
        classify_pin("123")


def test_full_space_breakdown_sums_to_10000():
    counts = category_breakdown()
    assert sum(counts.values()) == 10000
