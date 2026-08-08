# 04 — Indicator → Strategy — REAL-DATA-009

## Transition

Indicator (context) → Strategy (StrategyManager → StrategyEngine →
StrategyLibrary; StrategyService boundary).

- **INPUT:** `context` (ContextSnapshot) — `pipeline.py:405`.
- **PROCESSING:** `self.signal_engine.generate_signals(context)` —
  `pipeline.py:405`. `SignalEngine.generate_signals()`
  (`signal_layer/signal_engine/signal_engine.py`) ichida
  `StrategyManager.run_all_strategies()` chaqiriladi
  (`strategy_layer/strategy_manager/strategy_manager.py`). Har bir
  strategy StrategyLibrary qoidalari orqali `context`ga qarshi
  ishlaydi. **Muhim:** StrategyManager pipeline'da alohida
  chaqirilMAYDI — aks holda har strategy ikki marta ishlar edi
  (pipeline izohi:400-402).
- **OUTPUT:** `signal_candidates: List[SignalCandidate]` —
  `pipeline.py:405`.
- **NEXT CONSUMER:** signal_quality (`pipeline.py:422`), ai
  (`pipeline.py:477`), decision (`pipeline.py:487`).

## Ownership

StrategyService — strategy boundary; SignalEngine orkestratsiya
qiladi, StrategyManager strategiyalarni yuritadi, StrategyLibrary
qoidalarni saqlaydi. Layer boundary: pipeline faqat SignalEngine'ni
chaqiradi.

## Real runtime dalil

Run `31240675527`: `Generated 1 signal candidate(s)` — `FVG_STRATEGY,
BUY` real data bilan.

## Status: PASS
</content>
