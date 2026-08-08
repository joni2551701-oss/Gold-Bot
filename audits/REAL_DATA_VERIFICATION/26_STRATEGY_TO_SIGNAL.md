# 26 — Strategy → Signal (TASK-04)

## Transition
Strategy → Signal (SignalEngine orchestration, ConfluenceEngine,
SignalBuilder construction, SignalValidator, SignalScoring, SignalFormatter,
SignalService forwarding).

## Input
Strategiyalardan `List[SignalCandidate]`.
Evidence: `strategy_layer/strategy_manager/strategy_manager.py:23`.

## Processing (file:line)
- SignalEngine orchestration: `signal_layer/signal_engine/signal_engine.py:17-23`
  — StrategyManager natijasini SignalCandidate ro'yxati sifatida
  qaytaradi (AI/Decision uchun interfeys).
- SignalCandidate model: `signal_layer/signal_builder/models.py`.
- SignalScoring (runtime, advisory): `core_layer/pipeline/pipeline.py:421`
  `compute_signal_quality(candidate, context, htf_bias)` →
  `signal_layer/signal_scoring/signal_quality.py`.
- Explainability: `core_layer/pipeline/pipeline.py:439`
  → `signal_layer/signal_scoring/explainability.py`.
- SignalFormatter (Telegram uchun, faqat approve'langan winner uchun):
  `core_layer/pipeline/pipeline.py:568`
  → `platform_layer/telegram/signal_formatter.py`.

## Output
`signal_candidates` (pipeline `signals`), `quality_results`,
`explanations`, `features`, `signal_history`.
Evidence: `core_layer/pipeline/pipeline.py:640-645`.

## Next Consumer
`ai` bosqichi (`:476`) va `decision` bosqichi (`:487`).

## Ownership-rule check
- SignalEngine orchestratsiyani egallaydi (`signal_engine.py:7-23`) — PASS.
- ConfluenceEngine (`signal_layer/confluence_engine/`), SignalValidator
  (`signal_layer/signal_validator/validator.py`), SignalBuilder
  (`signal_layer/signal_builder/`), SignalFormatter
  (`signal_layer/signal_formatter/`), SignalService
  (`signal_layer/signal_service/manager.py`) — bularning ba'zilari
  **additive-parallel** yo'lda: `signal_layer/signal_service/manager.py`
  docstringi aniq belgilaydi: "The live signal_engine.py / SignalCandidate
  path is untouched and unimported" (`signal_layer/signal_service/manager.py:16-17`).
  Ya'ni live pipeline `signal_engine.py` yo'lidan foydalanadi;
  `SignalManager` (STEP-08) alohida canonical yo'l, live yo'lga
  ulanmagan.
- SignalService forwarding: live pipeline'da signal forwarding pipeline
  orchestratori orqali (`pipeline.py`), `SignalService` emas.

**Ownership eslatma (STOP emas):** ikki signal yo'li mavjud — live
(`signal_engine.py`) va additive-parallel canonical (`signal_service/
manager.py`). Bu ataylab hujjatlashtirilgan dizayn (STEP-08 reuse-first,
docstringda qayd etilgan), RUNTIME CONFLICT emas.

## Status
**PASS** — Strategy → Signal live `signal_engine.py` yo'li orqali
tasdiqlangan. Canonical `SignalService` additive-parallel (live yo'ldan
tashqarida, hujjatlashtirilgan).
</content>
