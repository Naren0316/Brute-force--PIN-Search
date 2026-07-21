import pytest

from backend.vault import SimulatedVault


def test_correct_pin_succeeds():
    vault = SimulatedVault(correct_pin="4321")
    result = vault.try_pin("4321")
    assert result.success is True
    assert result.attempt_number == 1


def test_incorrect_pin_fails():
    vault = SimulatedVault(correct_pin="4321")
    result = vault.try_pin("0000")
    assert result.success is False


def test_attempt_counter_increments():
    vault = SimulatedVault(correct_pin="4321")
    vault.try_pin("0000")
    vault.try_pin("1111")
    result = vault.try_pin("4321")
    assert result.attempt_number == 3


def test_locked_vault_raises():
    vault = SimulatedVault(correct_pin="4321")
    vault.lock()
    with pytest.raises(PermissionError):
        vault.try_pin("4321")


def test_invalid_correct_pin_raises():
    with pytest.raises(ValueError):
        SimulatedVault(correct_pin="12a4")
