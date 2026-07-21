import uuid

from backend import attempt_log


def test_log_and_retrieve_attempt(tmp_path, monkeypatch):
    # Redirect the DB to a temp file so tests never touch real data/
    test_db = tmp_path / "test_attempts.db"
    monkeypatch.setattr(attempt_log, "DB_PATH", test_db)

    attempt_log.init_db()
    run_id = str(uuid.uuid4())[:8]

    attempt_log.log_attempt(
        run_id=run_id,
        vault_id="test-vault",
        pin_tried="1234",
        pattern_category="Top Verified Common PINs",
        success=False,
        attempt_number=1,
        elapsed_seconds=0.01,
    )

    rows = attempt_log.get_run_attempts(run_id)
    assert len(rows) == 1
    assert rows[0][3] == "1234"  # pin_tried column
