from backend.entropy import analyze, shannon_entropy


def test_shannon_entropy_all_same_digit_is_zero():
    assert shannon_entropy("1111") == 0.0


def test_shannon_entropy_four_unique_digits_is_two():
    assert shannon_entropy("1234") == 2.0


def test_common_pin_scores_low_risk_high():
    report = analyze("1234")
    assert report.risk_tier in ("CRITICAL", "WEAK")


def test_less_common_pin_scores_higher_than_common_pin():
    common = analyze("0000")
    less_common = analyze("8503")
    assert less_common.strength_score > common.strength_score


def test_score_bounds():
    for pin in ["0000", "1234", "8503", "9317"]:
        report = analyze(pin)
        assert 0 <= report.strength_score <= 100
