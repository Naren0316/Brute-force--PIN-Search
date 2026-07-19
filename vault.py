"""
attempt_log.py
---------------
SQLite-backed attempt logging for simulated attack runs. Stores every
attempt made against a SimulatedVault so later modules (Day 2 attack
engine, Day 3 statistics/reporting) can query and analyze run history.
"""

import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, List, Tuple

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "attempt_log.db"


def _ensure_db_dir() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    _ensure_db_dir()
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT NOT NULL,
                vault_id TEXT NOT NULL,
                pin_tried TEXT NOT NULL,
                pattern_category TEXT,
                success INTEGER NOT NULL,
                attempt_number INTEGER NOT NULL,
                elapsed_seconds REAL NOT NULL,
                logged_at REAL NOT NULL
            )
            """
        )


def log_attempt(
    run_id: str,
    vault_id: str,
    pin_tried: str,
    pattern_category: str,
    success: bool,
    attempt_number: int,
    elapsed_seconds: float,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO attempts
               (run_id, vault_id, pin_tried, pattern_category, success,
                attempt_number, elapsed_seconds, logged_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                run_id,
                vault_id,
                pin_tried,
                pattern_category,
                int(success),
                attempt_number,
                elapsed_seconds,
                time.time(),
            ),
        )


def get_run_attempts(run_id: str) -> List[Tuple]:
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT * FROM attempts WHERE run_id = ? ORDER BY attempt_number",
            (run_id,),
        )
        return cursor.fetchall()


def get_all_run_ids() -> List[str]:
    with get_connection() as conn:
        cursor = conn.execute("SELECT DISTINCT run_id FROM attempts")
        return [row[0] for row in cursor.fetchall()]
