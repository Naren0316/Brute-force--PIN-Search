# PIN Security Research Platform

A cybersecurity education and PIN-security-awareness platform: it analyzes
how predictable common 4-digit PINs are, simulates attack strategies
against **local, self-contained target values**, and models how lockout
policies defend against those attacks — with a full backend engine and a
SOC/terminal-styled dashboard.

> **Scope & disclaimer:** This project never connects to, targets, or
> interacts with any real device, account, or external authentication
> system. Every "vault" is a value you configure yourself, entirely
> in-process or in a local SQLite file. It exists to teach *why* certain
> PINs are dangerous and *why* lockout policies matter — not to unlock
> anything real.

## Build plan (5 days)

| Day | Focus | Deliverable |
|-----|-------|-------------|
| **1** | Pattern Intelligence Engine (this drop) | PIN pattern classifier, entropy/strength scorer, simulated vault, SQLite attempt logger, full test suite |
| 2 | Attack Simulation + Lockout Engine | Multi-strategy attack runner (priority-weighted → exhaustive) against the local vault; configurable lockout/backoff policy simulator |
| 3 | Statistics & Reporting Engine | Cross-run analytics, PIN strength batch analysis, exportable training-report generator |
| 4 | API Layer | FastAPI service exposing all engines (REST + WebSocket for live attack progress), OpenAPI docs, Dockerfile |
| 5 | Frontend | Dark, SOC-style dashboard: live attack visualizer, lockout simulator UI, stats dashboard, polish & deploy |

## Day 1 — what's in this drop

```
backend/
  pattern_engine.py   # Classifies any 4-digit PIN into a likelihood category + weight
  entropy.py           # Shannon entropy + pattern-penalty strength scoring (0-100, risk tier)
  vault.py              # SimulatedVault — local in-memory target, attempt counter, lock state
  attempt_log.py       # SQLite-backed logging of every simulated attempt
  config.py            # Central tunables (scoring weights, default lockout policy)
tests/                  # 20 unit tests covering all Day 1 modules
demo.py                 # Runs everything end-to-end against a local demo vault
```

### Run it

```bash
pip install -r requirements.txt
python demo.py
```

### Run the tests

```bash
pytest -q
```

## Design notes

- **Pattern engine**: PINs are classified into 11 categories (top verified
  common PINs, keypad geometric shapes, repeated digits, sequences,
  repeated pairs, palindromes, likely years, date-like, etc.), each with
  a relative likelihood weight. `build_priority_queue()` produces the
  full 10,000-PIN space ordered by descending guessability — this is the
  candidate order Day 2's attack engine will consume.
- **Strength scoring** deliberately weights pattern predictability (70%)
  over raw Shannon entropy (30%). A PIN like `1234` has *maximal* digit
  entropy (four unique digits) but is one of the most guessed PINs that
  exists — predictability, not digit variety, is what should drive the
  risk score.
- **SimulatedVault** never exposes its target PIN and only compares
  values passed to `try_pin()`. It supports a `lock()` state so Day 2's
  lockout-policy simulator can freeze it after N attempts.
- **Attempt logging** is SQLite-backed (`data/attempt_log.db`, gitignored)
  so Day 3's reporting engine can query full run history — timing,
  pattern category hit, and outcome per attempt.

## License

Educational / research use.
