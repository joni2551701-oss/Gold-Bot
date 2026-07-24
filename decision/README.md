# decision/

## Purpose
Blends signal confidence, HTF bias, (inverted) AI risk score, and AI
confidence into one final trade verdict: APPROVE, REJECT, or
NO_TRADE. As of Phase A3 ("Decision Engine v2"), this is a weighted
four-input formula, replacing the pre-A3 flat two-input average.

## Flow
```
Signal Candidate + AI Analysis + (optional) HTF Bias Result
      |
      v
Decision Engine   -- DecisionInput -> weighted score -> threshold logic
      |
      v
Risk Manager
```

## Decision v2: Input flow

`DecisionEngine.evaluate(signal, ai_analysis, htf_bias=None)` builds
a `DecisionInput` (`_build_decision_input()`) from the three objects
it already receives — no new fetch, no new pipeline stage:

| `DecisionInput` field | Sourced from | Notes |
|---|---|---|
| `signal_confidence` | `SignalCandidate.confidence` | Unchanged from pre-A3. |
| `htf_bias` | `HTFBiasResult.bias` (or `HTFBias.UNKNOWN` if `htf_bias=None`) | `context/htf_bias.py`, Phase A2. |
| `htf_quality_score` | `HTFBiasResult.quality_score` (or `0.0` if `htf_bias=None`) | Drives Step-5 quality dampening — see below. |
| `risk_score` | `1.0 - AIAnalysisResult.risk_score` | **Inverted** — `AIAnalysisResult.risk_score` is `0.0`=no risk .. `1.0`=max risk (`ai/ai_analyzer.py`); `DecisionInput.risk_score` is flipped so "higher is always better," matching the other three inputs. Note this is *not* `risk.risk_manager.RiskResult` — that object doesn't exist yet at Decision Engine time (Risk runs *after* Decision in the pipeline). |
| `ai_score` | `AIAnalysisResult.confidence` | Unchanged from pre-A3. |

A caller that omits `htf_bias` (any pre-Phase-A2/A3 call site) still
works unchanged — see "Backward compatibility" below.

## Weight system

`DecisionWeights` (a frozen dataclass, injectable into
`DecisionEngine.__init__` exactly like `DecisionConfig` already was)
holds the four weights as named constants — never hardcoded inline in
`evaluate()`:

| Component | Weight |
|---|---|
| Signal Confidence | 40% |
| HTF Bias | 25% |
| Risk (inverted AI risk score) | 20% |
| AI Confidence | 15% |

```
final_confidence = 0.40*signal_score + 0.25*htf_score
                  + 0.20*risk_score  + 0.15*ai_score
```

All four component scores and `final_confidence` stay on the existing
0.0–1.0 scale — the same scale `DecisionConfig.min_confidence`/
`approve_confidence`, `SignalCandidate.confidence`, and
`AIAnalysisResult.confidence` already used before Phase A3, so no
existing threshold or downstream consumer needed to change scale.

## HTF integration

`HTF_BIAS_SCORE_MAP` (module-level constant in `decision_engine.py`)
maps `HTFBias` to a base score, adapted from the Phase A3 brief's 0–100
example onto GoldBot's existing 0.0–1.0 confidence scale:

| `HTFBias` | Base score |
|---|---|
| `BULLISH` | `1.0` |
| `NEUTRAL` | `0.5` |
| `BEARISH` | `0.0` |
| `UNKNOWN` | `0.5` (same as `NEUTRAL` — an unresolved HTF read must never push the outcome either direction) |

**Quality handling** (poor HTF data quality dampens the contribution
toward neutral — it never causes an automatic rejection):

```
htf_score = base_score * htf_quality_score + 0.5 * (1 - htf_quality_score)
```

`quality_score=1.0` (100%) → full weight (the base score passes
through unchanged). `quality_score=0.0` (0%) → the base score is
completely replaced by the neutral midpoint `0.5`, regardless of what
the underlying bias was. Anything in between is a linear blend.

## Explainability

`TradeDecision` (Phase A3) exposes every component the formula used,
in addition to the pre-existing `action`/`confidence`/`reason`/
`signal`/`ai_analysis` fields:

| Field | Meaning |
|---|---|
| `signal_score` | `DecisionInput.signal_confidence`, unweighted. |
| `htf_score` | The quality-dampened HTF contribution (see above). |
| `risk_score` | `DecisionInput.risk_score` (inverted AI risk score), unweighted. |
| `ai_score` | `DecisionInput.ai_score`, unweighted. |
| `final_score` | The full weighted blend — always equal to `confidence`; a separate named field only because it's one of the formula's five components, not because it carries different information. |

This is data exposure only — no UI/Telegram change was made to
surface it (`telegram/signal_formatter.py` is untouched).

## Backward compatibility

- `DecisionEngine.evaluate(signal, ai_analysis)` — no third argument —
  still works exactly as before: `htf_bias` defaults to `None`, which
  `_build_decision_input()` treats as `HTFBias.UNKNOWN` with
  `htf_quality_score=0.0`, which the quality formula above always
  resolves to exactly `0.5` — the same neutral contribution as an
  explicit `UNKNOWN` result, never an error.
- `DecisionEngine()` — no arguments — still works: both `config` and
  the new `weights` default to their standard values.
- The three-branch APPROVE/REJECT/NO_TRADE threshold logic against
  `DecisionConfig.min_confidence`/`approve_confidence`, and the
  AI-approval hard gate (`if not ai_analysis.approved: REJECT`,
  checked before any threshold), are byte-for-byte unchanged — only
  what feeds into `final_confidence` changed.
- `TradeDecision`'s five new fields all default to `0.0`, so any
  hypothetical caller constructing one directly (none exist in this
  codebase today — `DecisionEngine.evaluate()` is the sole
  construction site) would not break either.

**What did change, deliberately**: the exact numeric value of
`confidence` for a given `(signal, ai_analysis)` pair, since the
formula itself was replaced (per Phase A3's explicit brief) — this is
why `tests/unit/test_decision_engine.py`'s two formula-dependent
assertions were updated to the new formula's real output, while every
behavioral guarantee (AI-reject always REJECTs, threshold crossings
still produce the right action, `TradeDecision` still carries the
original signal/AI analysis) was re-verified, not merely assumed, to
still hold.

## Input
`SignalCandidate` (from `signals/`) + `AIAnalysisResult` (from `ai/`)
+ optionally `HTFBiasResult` (from `context/`, Phase A2).

## Output
`TradeDecision` (`action`, `confidence`, `reason`, `signal`,
`ai_analysis`, plus the five explainability fields above).

## Dependencies
`ai/` (for `AIAnalysisResult`) and `signals/` (for `SignalCandidate`)
— both still `TYPE_CHECKING`-only, unchanged from pre-A3. `context/`
(for `HTFBias`, a real runtime import — the enum is used as
`HTF_BIAS_SCORE_MAP`'s dict keys at module load time; `HTFBiasResult`
itself stays `TYPE_CHECKING`-only). Still no dependency on
`database/`, `telegram/`, or `risk/`.

## Future Expansion
Confidence-threshold values (`DecisionConfig`) and the weight values
(`DecisionWeights`) are both named explicitly in `CLAUDE.md`'s Trading
Safety rules as requiring approval before any further change — Phase
A3 itself was one such explicitly-approved change. Natural future
inputs to the same weighted-formula shape (not implemented in this
phase): Signal Quality Score, Market Regime, Session Intelligence —
see `docs/v0.3.5_SPECIFICATION.md` and `docs/FOUNDATION_GAP_ANALYSIS.md`.
