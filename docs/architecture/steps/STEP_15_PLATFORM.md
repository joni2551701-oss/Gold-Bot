# STEP-15 — `platform/` Layer Architecture Specification

> **DOCUMENTATION ONLY.** Blueprint for the platform step. No code here.
> `platform/` **does not exist yet** — it would be a **new top-level
> package**, the highest-cost option under the Module Reuse Principle. This
> spec exists so the design is agreed *before* any code; creating the package
> requires **explicit Director approval** on its own TASK-CORE spec.

## 1. Purpose

A thin **platform-abstraction / dispatch** layer so one risk-approved,
formatted outcome can reach *many* front-ends — Telegram today, mobile /
mini-app / desktop later — without the trade path knowing which. It is a
**fan-out contract**, not a second Telegram implementation.

**Does:** turn a `RiskOutcome` + presentation into a neutral
`PlatformMessage` and hand it to whichever platform adapter(s) are enabled.
**Does NOT:** compute anything (risk/decision already did), format
platform-specific markup (each adapter does that), or bypass the notification-
eligibility filter.

## 2. Why a new package (Module Reuse Principle answer)

1. **Does it already exist?** — No. `telegram/` is one platform's transport;
   there is no platform-neutral dispatch point today.
2. **Can an existing module be extended?** — Partially: `signal_layer/signal_service/router.py`
   and `decision_layer/decision_service/decision_router.py` already emit *consumer route metadata*
   (which layers care), but neither *dispatches* to multiple front-ends.
   Extending `telegram/` would couple the fan-out to one platform — the exact
   thing this layer must avoid.
3. **Therefore a new package** — justified only because a genuinely new,
   platform-neutral responsibility exists. It stays **thin**: one model, one
   dispatcher, one adapter interface, and Telegram wired through the existing
   `telegram/` layer (reuse, not reimplement).

> Until approved, treat `platform/` as a **proposal**. The alternative
> (defer it and let `telegram/` remain the sole front-end via STEP-13) is a
> valid v0.x choice — flag this decision to the Director explicitly.

## 3. Position in the flow

```
risk (STEP-10)  RiskOutcome(approved) + SignalPresentation (from signals/formatter)
        │
        ▼
platform/platform_message.py   (neutral PlatformMessage)
        │
        ▼
platform/platform_dispatcher.py  ── reads enabled adapters, fan-out
        ├─► platform/adapters/telegram_adapter.py ──► telegram/notification_service (REUSE)
        ├─► platform/adapters/mobile_adapter.py    (future, stub)
        └─► platform/adapters/miniapp_adapter.py   (future, stub)
```

## 4. Input / Output

- **Input:** a `RiskOutcome` (approved) + a `SignalPresentation` (the neutral
  title/summary/reason already produced by `signal_layer/signal_formatter/formatter.py`), plus the
  audience (owner / subscriber tier).
- **Output:** a neutral `PlatformMessage` dispatched to each enabled adapter;
  each adapter returns a delivery status.

## 5. File-by-file specification

| File | Role | Input | Output | Reads from | Passes to | New / Extend |
|---|---|---|---|---|---|---|
| `platform/platform_message.py` | neutral `PlatformMessage` model (`to_dict`) | risk + presentation | `PlatformMessage` | risk/signals presentation | dispatcher | **new** |
| `platform/platform_status.py` | delivery-status vocab `QUEUED/SENT/SKIPPED/FAILED` | adapter result | `PlatformStatus` | adapters | dispatcher/db | **new** |
| `platform/adapter_contract.py` | `PlatformAdapter` ABC (`deliver(PlatformMessage)->PlatformStatus`) | — | contract | — | adapters | **new** (mirrors `ai_layer/ai_service/interfaces.py` style) |
| `platform/platform_dispatcher.py` | fan-out to enabled adapters; honour eligibility | `PlatformMessage` | statuses | adapter_contract | adapters/db | **new** |
| `platform/platform_router.py` | which adapters an outcome targets (owner/tier) | outcome | adapter list | platform_message | dispatcher | **new** (mirrors `decision_router.py`) |
| `platform/adapters/telegram_adapter.py` | implement contract by delegating to `telegram/notification_service` | `PlatformMessage` | `PlatformStatus` | telegram service | telegram | **new** (thin; REUSES telegram/, no new send logic) |
| `platform/adapters/mobile_adapter.py` | future front-end stub | `PlatformMessage` | `PlatformStatus` (not-impl) | — | — | **new stub** (inert, like execution/) |
| `platform/adapters/miniapp_adapter.py` | future front-end stub | `PlatformMessage` | `PlatformStatus` (not-impl) | — | — | **new stub** |
| `platform/README.md` | package doc + boundary | — | — | — | — | **new** |

### Reuse-first constraints (mandatory)
- The Telegram adapter **delegates to the existing `telegram/notification_
  service.py`** — it re-implements no send logic and re-uses the existing
  eligibility gate. `platform/` never imports aiogram directly.
- `platform/` imports the *presentation* value objects from `signals/` and
  the `RiskOutcome` from `risk/` — read only, one-directional. `signals/`,
  `risk/`, `decision/` never import `platform/`.
- Mobile/mini-app/desktop adapters ship **inert** (like `execution/`), so the
  package is real but only Telegram is live.

## 6. Boundary & safety
- No decision/risk/analysis in `platform/` — pure dispatch.
- The notification-eligibility filter (REJECT/BLOCKED never reach a user) is
  enforced *before* dispatch and re-checked in the Telegram adapter — never
  weakened.
- Owner-only content stays owner-only; tiering decided by `platform_router.py`
  reading existing subscription state via a service, never new DB access from
  an adapter.

## 7. Detailed flow

```
RiskOutcome(approved) + SignalPresentation ──► platform_message.build(...)
        │
        ▼
platform_router.route(outcome, audience) ──► [telegram_adapter (+ future stubs)]
        │
        ▼
platform_dispatcher.dispatch(PlatformMessage)
        ├─ eligibility re-check
        └─► telegram_adapter.deliver() ──► telegram/notification_service.send()  [REUSE]
                                                   │
                                                   ▼  PlatformStatus(SENT/SKIPPED/FAILED)
                                             database (STEP-12: record delivery)
```
