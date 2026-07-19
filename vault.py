"""
vault.py
--------
SimulatedVault: an in-memory, self-contained stand-in for an authentication
target, used ONLY within this simulation. It never connects to, wraps, or
proxies any real device, account, or external service -- the "correct"
PIN is a value you configure directly for training/research purposes.
"""

import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class AttemptResult:
    pin_tried: str
    success: bool
    attempt_number: int
    elapsed_seconds: float


class SimulatedVault:
    """A local, in-memory simulated PIN target."""

    def __init__(self, correct_pin: str, vault_id: str = "demo-vault"):
        if not (len(correct_pin) == 4 and correct_pin.isdigit()):
            raise ValueError("correct_pin must be a 4-digit numeric string")
        self.vault_id = vault_id
        self._correct_pin = correct_pin
        self.attempts = 0
        self._start_time: Optional[float] = None
        self._locked = False

    def start(self) -> None:
        self._start_time = time.time()

    def is_locked(self) -> bool:
        return self._locked

    def lock(self) -> None:
        self._locked = True

    def try_pin(self, pin: str) -> AttemptResult:
        if self._start_time is None:
            self.start()
        if self._locked:
            raise PermissionError(f"Vault '{self.vault_id}' is locked.")

        self.attempts += 1
        success = pin == self._correct_pin
        elapsed = time.time() - self._start_time

        return AttemptResult(
            pin_tried=pin,
            success=success,
            attempt_number=self.attempts,
            elapsed_seconds=round(elapsed, 4),
        )
