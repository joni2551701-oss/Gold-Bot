# STEP-12 — `database/` Layer Architecture Specification

> **DOCUMENTATION ONLY.** Blueprint for the database step. No code here.
> `database/` is a mature layer with a strict, established convention:
> **`<x>_models.py` + `<x>_repository.py`** per aggregate; repositories own
> SQL only, services own business logic (CLAUDE.md Architecture Rules).

## 1. Purpose

Persist the two new outcomes STEP-09/STEP-10 introduce — `DecisionOutcome`
and `RiskOutcome` — plus the STEP-11 `ExecutionIntent`, so every verdict is
recorded whether or not it reaches the user. STEP-12 adds **new repositories
on the existing convention**; it does not restructure `database/`.

**Does:** define tables + SQL CRUD for the new outcome records. **Does NOT:**
compute a verdict, contain any trading business rule (that stays in
risk/decision), or read secrets.

## 2. Position in the flow

```
decision (STEP-09) ─ DecisionOutcome ─┐
risk     (STEP-10) ─ RiskOutcome ─────┤
execution(STEP-11) ─ ExecutionIntent ─┤
                                      ▼
              database/*_repository.py  (write via a service, never from a handler)
                                      │  SQL only
                                      ▼
                               database/database.py  (connection)  → goldbot.db
```

## 3. Input / Output

- **Input:** `DecisionOutcome.to_dict()`, `RiskOutcome.to_dict()`,
  `ExecutionIntent.to_dict()` — passed in by a *service* caller, never by a
  Telegram handler directly.
- **Output:** persisted rows; read-back query methods returning plain dicts /
  record dataclasses for analytics and the owner snapshot.

## 4. File-by-file specification

| File | Role | Input | Output | Reads from | Passes to | New / Extend |
|---|---|---|---|---|---|---|
| `database/database.py` | connection/schema init | — | connection | — | repositories | **reuse** (register new tables via its init, as existing repos do) |
| `database/decision_outcome_models.py` | table def + row dataclass for `DecisionOutcome` | dict | row | decision_model | repository | **new** (mirrors `risk_decision_models.py`) |
| `database/decision_outcome_repository.py` | SQL CRUD for decision outcomes | dict | rows | models | analytics/snapshot | **new** |
| `database/risk_outcome_models.py` | table def + row dataclass for `RiskOutcome` | dict | row | risk_model | repository | **new** |
| `database/risk_outcome_repository.py` | SQL CRUD for risk outcomes | dict | rows | models | analytics/snapshot | **new** |
| `database/execution_intent_models.py` | table def for `ExecutionIntent` | dict | row | execution_status | repository | **new** (optional; only if STEP-11 record kept in DB) |
| `database/execution_intent_repository.py` | SQL CRUD for execution intents | dict | rows | models | analytics | **new** (optional) |
| `database/migrations/` | additive migration for the new tables | — | schema | — | database.py | **extend** (new isolated migration file; never alters existing tables) |
| `database/README.md` | append STEP-12 section | — | — | — | — | **extend** |

### Existing files to EXTEND (reuse-first)
- `database/database.py` — new tables register through the same init path
  every existing repository already uses (`signal_repository`,
  `risk_decision_repository`, …). **No new connection layer.**
- `database/migrations/` — one new, **additive** migration (new tables only;
  existing tables untouched — the same discipline as the Phase 59.3 raw-
  market-storage migration).
- Reuse audit first: `risk_decision_repository.py` /
  `risk_state_repository.py` already persist risk decisions — confirm whether
  a new `risk_outcome_*` is genuinely needed or whether extending the
  existing risk repo satisfies STEP-10, before creating new files.

## 5. Convention & boundary guarantees
- Repositories are **SQL only** — no business rule (CLAUDE.md: no new
  business logic in `database/*_repository.py`).
- **No direct DB access from Telegram handlers** — a service calls the
  repository; the repository calls the DB.
- Migrations are additive and isolated; no existing table/column is altered
  or dropped.

## 6. Detailed flow

```
service caller ──► decision_outcome_repository.insert(outcome.to_dict())
                              │  SQL INSERT
                              ▼
                       database.py connection ──► goldbot.db (decision_outcomes table)

analytics / owner snapshot ──► decision_outcome_repository.query(...) ──► rows (read-only)
```
