# STEP-16 — `monitoring/` Layer Architecture Specification

> **DOCUMENTATION ONLY.** Blueprint for the monitoring step. No code here.
> `monitoring/` is an **observer-only** layer (Phase B.0): it reads
> counters/events and never writes back into the trade path. STEP-16
> **extends existing monitors**; no new top-level package.

## 1. Purpose

Give the operator visibility into the new STEP-10..15 stages — decision
outcomes, risk verdicts, execution intents, platform deliveries — by
extending the existing monitors and the owner snapshot. It observes; it never
gates, decides, or sends a trade.

**Does:** count/record verdicts and delivery outcomes; surface them via the
existing owner snapshot and `/status`/`/performance` commands. **Does NOT:**
approve/reject anything, alter the pipeline, or reach into risk/decision.

## 2. Position in the flow (observer, side-channel)

```
decision (STEP-09) ─┐
risk     (STEP-10) ─┤   emit counters/events (read-only)
execution(STEP-11) ─┤
platform (STEP-15) ─┘
        │
        ▼
decision_layer/decision_logger/decision_logger.py · risk_monitor.py · signal_monitor.py · health_monitor.py
        │  aggregate (pure counters, no writes to trade path)
        ▼
core_layer/health_monitor/system_monitor.py  ──►  owner snapshot / /status / /performance
```

## 3. Input / Output

- **Input (read-only):** verdict/counter events from decision/risk/execution/
  platform (each stage already logs; STEP-16 adds observers for the new
  outcome types).
- **Output:** aggregated counters and health rollups consumed by the owner
  snapshot (`monitoring/snapshot_collector.py`) and owner commands — never fed
  back into the pipeline.

## 4. File-by-file specification

| File | Role | Input | Output | Reads from | Passes to | New / Extend |
|---|---|---|---|---|---|---|
| `decision_layer/decision_logger/decision_logger.py` | per-stage decision timing/verdict log | decision events | log rows | decision | system_monitor | **extend** (add DecisionOutcome status counts APPROVE/REJECT/HOLD/EXPIRE) |
| `core_layer/health_monitor/risk_monitor.py` | risk checks/reject/drawdown/pause counters | risk events | counters | risk | system_monitor | **extend** (add RiskOutcome status APPROVED/REJECTED/PAUSED/BLOCKED) |
| `core_layer/health_monitor/signal_monitor.py` | signal counters | signal events | counters | signals | system_monitor | **reuse** (already covers signal side) |
| `core_layer/health_monitor/health_monitor.py` | OK/WARNING/CRITICAL rollup | monitors | health | all monitors | snapshot | **reuse/extend** (fold new counters into health) |
| `core_layer/health_monitor/performance_collector.py` | pure per-stage counters | events | counters | stages | performance | **extend** (add platform-delivery counters SENT/SKIPPED/FAILED) |
| `core_layer/health_monitor/system_monitor.py` | system rollup | all monitors | snapshot fields | monitors | owner snapshot | **extend** |
| `monitoring/snapshot_collector.py` (owner snapshot) | assemble owner snapshot | monitors | `OwnerSnapshot` | monitors | telegram owner | **extend** (surface new sections; honest, no fabricated stats) |
| `docs/architecture/MONITORING.md` | append STEP-16 section | — | — | — | — | **extend** |

### Existing files to EXTEND (reuse-first)
- All observers already exist (Phase B.0 / v1.1). STEP-16 adds new *counters*
  and *snapshot fields* to them — **no new monitoring module, no new package**.
- Owner-facing surfacing reuses the existing `/status`, `/performance`, and
  the 15-minute owner-snapshot pipeline (`monitoring/run_snapshot.py` →
  `telegram/owner/snapshot_*`).

## 5. Boundary & safety
- **Observer-only:** monitoring imports from the layers it watches (read),
  never the reverse; it never calls risk/decision/execution/platform to *act*.
- **Honesty rule** (v1.1): no fabricated metrics — a counter with no data
  reads as `0`/`n/a`, never an invented value.
- No secret is read or logged; the snapshot layer already enforces this.

## 6. Detailed flow

```
DecisionOutcome / RiskOutcome / ExecutionIntent / PlatformStatus  (events)
        │  read-only
        ▼
decision_logger + risk_monitor + performance_collector  (increment counters)
        │
        ▼
health_monitor (OK/WARNING/CRITICAL) ──► system_monitor ──► snapshot_collector
                                                                │
                                                                ▼
                                          owner snapshot (15-min) + /status + /performance
```
