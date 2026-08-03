# STEP-14 — `ai/` Layer Architecture Specification

> **DOCUMENTATION ONLY.** Blueprint for the AI step. No code here.
> `ai/` is **advisory input to `decision/` only**. It must never approve/
> reject a trade, call the Risk Manager, or trigger a Telegram send or
> execution action (CLAUDE.md Trading Safety; `ai/interfaces.py`
> `AIAnalyzerInterface` contract). STEP-14 wires *reads*, never *actions*.

## 1. Purpose

Give the AI layer a defined, read-only view of the new pipeline outputs so a
future provider can produce a **richer advisory `AIResponse`** — grounded in
context + signals + decision + persisted history — that flows *into* the
decision blend. It changes what the AI can *see*, never what it can *do*.

**Does:** read context/signals/decision/database; return an advisory
`AIResponse` (`decision`/`confidence` are advisory only). **Does NOT:** call
risk, execution, or telegram; never the final say on a trade.

## 2. Position in the flow

```
context ─┐
signals ─┤  (read-only)
decision ┤ ──► ai/context/ (AIContext builder) ──► ai provider (AIAnalyzerInterface)
database ┘                                              │  AIResponse (advisory)
                                                        ▼
                                        decision_layer/decision_engine/decision_engine.py  (blend input, FROZEN)
                                              ▲  advisory only — AI never decides
                                              └─ AI cannot reach risk / execution / telegram
```

## 3. Input / Output

- **Input (read-only):** `MarketContext` (AI-facing subset of the context
  snapshot, `ai/interfaces.py`), the canonical signal, the `DecisionOutcome`,
  and persisted history via a database read.
- **Output:** `AIResponse` (`ai/interfaces.py`) — advisory `decision` +
  `confidence` + rationale. Consumed as *one weighted input* to the frozen
  decision blend; never as an approval.

## 4. File-by-file specification

| File | Role | Input | Output | Reads from | Passes to | New / Extend |
|---|---|---|---|---|---|---|
| `ai/interfaces.py` | provider contract (`MarketContext`/`UserContext`/`AIResponse`/`AIAnalyzerInterface`) | — | contract | — | providers | **reuse** (Phase 55, frozen shape) |
| `ai/ai_analyzer.py` | production analyzer wired into pipeline | context | `AIAnalysisResult` | context | decision | **reuse** (retrofitting to interface is out of scope) |
| `ai/context/` | AIContext builder (context→AI-facing view) | context/signals/decision | `AIContext` | context/signals/decision | provider | **extend** (add DecisionOutcome as a read-only input field) |
| `ai/providers/` | provider adapters (Gemini/OpenAI/…) | `AIContext` | `AIResponse` | context builder | decision blend | **reuse/extend** (no new action capability) |
| `ai/access/` | AI access control (who may use AI) | user/tier | allow/deny | access rules | runtime | **reuse** |
| `ai/audit/` | AI request/response audit | AI calls | audit rows | providers | monitoring | **reuse** |
| `ai/README.md` / `docs/ai/AI_ARCHITECTURE.md` | append STEP-14 read-map | — | — | — | — | **extend** |

### Existing files to EXTEND (reuse-first)
- `ai/context/` — add the `DecisionOutcome` (and a persisted-history read) as
  **read-only** inputs to the AIContext, so the advisory response is better
  grounded. No new top-level package.
- Everything else in `ai/` is reused as-is; STEP-14 adds no action surface.

## 5. The hard boundary (restated, non-negotiable)
- AI is **advisory input to `decision/` only**.
- AI **never**: calls `RiskManager.evaluate()`, builds/sends an
  `ExecutionIntent`, triggers a Telegram send, or writes to the trade path.
- The advisory `AIResponse.decision`/`confidence` are inputs to the FROZEN
  decision blend (`decision_layer/decision_engine/decision_engine.py`) — they do not *set* the
  verdict.
- Secrets (provider API keys) are read only via `config.py`/`core/secrets.py`
  and never logged (`ai/audit/` records metadata, not keys).

## 6. Detailed flow

```
context + signals + DecisionOutcome + db history
        │  read-only
        ▼
ai/context builder ──► AIContext ──► ai/providers (AIAnalyzerInterface.analyze)
                                            │  AIResponse (advisory)
                                            ▼
                          decision_layer/decision_engine/decision_engine.py blend  [FROZEN]  ── one weighted input
                                            ▲
                                            └── AI has NO path to risk / execution / telegram
```
