# 25 — Indicator → Strategy (TASK-03)

## Transition
Indicator → Strategy (StrategyManager discovery/selection, StrategyEngine
runtime, StrategyLibrary rules-only-not-owner, StrategyService boundary).

## Input
`ContextSnapshot` (indicator-ekvivalent strukturaviy maydonlarni o'z ichiga
oladi).
Evidence: `core_layer/pipeline/pipeline.py:405`
`signal_candidates = self.signal_engine.generate_signals(context)`.

## Processing (file:line)
- SignalEngine strategiyaga yo'naltiradi: `signal_layer/signal_engine/signal_engine.py:17`
  `generate_signals()` → `:23` `self.strategy_manager.run_all_strategies(context)`.
- StrategyManager discovery/selection: `strategy_layer/strategy_manager/strategy_manager.py:16-21`
  ro'yxatga olingan strategiyalar (`LiquidityStrategy`, `FVGStrategy`,
  `AMDStrategy`).
- Runtime ijro: `strategy_layer/strategy_manager/strategy_manager.py:23-34`
  `run_all_strategies()` — har bir `strategy.analyze(context)` ni ketma-ket
  chaqiradi va natijalarni birlashtiradi (`:30-32`).
- StrategyEngine base kontrakt: `strategy_layer/strategy_engine/base.py`.
- StrategyLibrary (rules-only): `strategy_layer/strategy_library/liquidity_strategy.py`,
  `fvg_strategy.py`, `amd_strategy.py`.

## Output
`List[SignalCandidate]` — barcha strategiyalardan birlashtirilgan
nomzodlar.
Evidence: `strategy_layer/strategy_manager/strategy_manager.py:28-34`.

## Next Consumer
SignalEngine → pipeline `signal` bosqichi natijasi
(`core_layer/pipeline/pipeline.py:405`, keyin `signal_quality` `:421`).

## Ownership-rule check
- StrategyManager discovery/selection'ni egallaydi (`:16-34`) — PASS.
- StrategyLibrary faqat qoidalarni (strategy.analyze mantiqini) saqlaydi,
  egasi emas — strategiyalar SignalCandidate qaytaradi, o'zlari signalni
  boshqa layer'ga yubormaydi. PASS.
- `StrategyService` (`strategy_layer/strategy_service/__init__.py:1-13`)
  Foundation Freeze skeleton — live yo'lda emas. Ownership eslatma: boundary
  service skeleton, orchestratsiya StrategyManager'da.
- Trading Safety: strategy mantiqiga TEGILMADI (read-only audit).

## Status
**PASS** — Indicator (context) → Strategy real kod bilan tasdiqlangan.
Runtime'da 3 strategiya `run_all_strategies` orqali yuritiladi.
`StrategyService` skeleton (Foundation Freeze).
</content>
