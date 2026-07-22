"""
demo.py
-------
Day 1 demo: exercises the pattern engine, entropy scorer, simulated vault,
and attempt logger together. Run this to see everything Day 1 built,
working end-to-end, entirely against a local simulated target.

Usage:
    python demo.py
"""

import uuid

from backend import config
from backend.attempt_log import get_run_attempts, init_db, log_attempt
from backend.entropy import analyze
from backend.pattern_engine import category_breakdown, classify_pin
from backend.vault import SimulatedVault


def print_header(title: str) -> None:
    print("\n" + "=" * 62)
    print(f" {title}")
    print("=" * 62)


def demo_pattern_engine() -> None:
    print_header("PATTERN ENGINE — sample classifications")
    samples = ["1234", "0000", "2580", "1997", "7392", "2323"]
    for pin in samples:
        m = classify_pin(pin)
        print(f"  {pin} -> {m.category.value:<32} weight={m.weight:>5.1f}")

    print("\n  Full 10,000-PIN space breakdown:")
    for category, count in category_breakdown().items():
        print(f"    {category.value:<32} {count:>5} PINs")


def demo_entropy() -> None:
    print_header("STRENGTH SCORER — entropy + pattern analysis")
    samples = ["1234", "7392", "0000", "8503"]
    for pin in samples:
        r = analyze(pin)
        print(
            f"  {pin}: entropy={r.shannon_entropy_bits} bits | "
            f"pattern={r.pattern_category.value} | "
            f"score={r.strength_score}/100 | risk={r.risk_tier}"
        )


def demo_vault_and_logging() -> None:
    print_header("SIMULATED VAULT + ATTEMPT LOGGING")
    init_db()

    vault = SimulatedVault(correct_pin="8503", vault_id="training-vault-01")
    run_id = str(uuid.uuid4())[:8]

    test_pins = ["1234", "0000", "2580", "8503"]
    for pin in test_pins:
        result = vault.try_pin(pin)
        category = classify_pin(pin).category.value
        log_attempt(
            run_id=run_id,
            vault_id=vault.vault_id,
            pin_tried=result.pin_tried,
            pattern_category=category,
            success=result.success,
            attempt_number=result.attempt_number,
            elapsed_seconds=result.elapsed_seconds,
        )
        status = "SUCCESS" if result.success else "fail"
        print(f"  attempt {result.attempt_number}: {pin} -> {status}")
        if result.success:
            break

    print(f"\n  Logged run_id={run_id}. Stored attempts:")
    for row in get_run_attempts(run_id):
        print(f"    {row}")


if __name__ == "__main__":
    print(f"{config.APP_NAME} v{config.VERSION}")
    demo_pattern_engine()
    demo_entropy()
    demo_vault_and_logging()
