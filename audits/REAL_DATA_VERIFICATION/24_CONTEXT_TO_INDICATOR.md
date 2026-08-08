# 24 — Context → Indicator (TASK-02)

## Transition
Context → Indicator (yakuniy indicator konteksti; Parallel Execution Rule).

## Input
`candles` (SSOT) va oraliq strukturaviy natijalar — `ContextEngine.build()`
ichida.
Evidence: `context_layer/context_engine/context_orchestrator/context_orchestrator.py:119-132`.

## Processing (file:line)
Indicator-ekvivalent hisob-kitoblar (Smart Money strukturaviy
"indikatorlari") `ContextEngine.build()` ichida ketma-ket yuritiladi:
- `_build_structure` — `context_layer/context_engine/context_orchestrator/context_orchestrator.py:169` (`detect_swing_points`, `classify_structure`).
- `_build_breaks` — `:185` (`detect_bos`, `detect_choch`).
- `_build_liquidity` — `:196` (`detect_equal_levels`, `detect_sweeps`).
- `_build_footprints` — `:211` (`detect_order_blocks`, `detect_fvg`).
- `_build_market_regime` — `:272` (`compute_market_regime`).

## Output
Har bir detector natijasi `ContextSnapshot`ning alohida maydoniga
yoziladi.
Evidence: `context_layer/context_engine/context_orchestrator/context_orchestrator.py:134-147`.

## Next Consumer
`signal` bosqichi (strategiyalar bu strukturaviy maydonlarni o'qiydi) —
`core_layer/pipeline/pipeline.py:405`.

## Ownership-rule check
Canonical qoida: "IndicatorService yakuniy indicator kontekstini
egallaydi; Parallel Execution Rule." Runtime holati:
- `indicator_layer/`ning barcha paketlari (`indicator_engine`,
  `indicator_service`, `market_structure_indicators`,
  `smart_money_indicators`, `trend_indicators`, `momentum_indicators`,
  `volatility_indicators`, `volume_indicators`, `custom_indicators`) —
  Foundation Freeze v1.0 skeletonlar (faqat `__init__.py` docstring).
  Evidence: `indicator_layer/indicator_service/__init__.py:1-13`,
  `indicator_layer/indicator_engine/__init__.py:1-13`.
- Live runtime'da indicator hisob-kitoblari `context_layer`ning detector
  modullarida joylashgan va `ContextEngine.build()` ichida bajariladi.
- Parallel Execution Rule: runtime'da detektorlar **ketma-ket** (linear)
  yuritiladi (`:121-132`), parallel emas — ContextEngine docstringi buni
  ataylab shunday deb belgilaydi ("holds no mutable state ... safe for
  repeated or concurrent use", `:94-97`) — ya'ni parallel-xavfsiz, lekin
  hozir ketma-ket. Bu Trading Safety'ga ta'sir qilmaydi (deterministik).

**Ownership eslatma (STOP emas):** `indicator_layer` skeleton bo'lgani va
indicator computatsiyasi `context_layer` ichida bo'lgani — bu
hujjatlashtirilgan Foundation Freeze / MIR-001 migration holati, canonical
arxitektura hujjatlariga zid RUNTIME CONFLICT emas. Layer chegarasi
buzilmagan (context o'z ichida ishlaydi, tashqi provider'ga chiqmaydi).

## Status
**PASS (runtime)** — indicator-ekvivalent kontekst real kod bilan
qurilyapti. Ownership: `IndicatorService` hozir skeleton (Foundation
Freeze), computatsiya `context_layer`da — hujjatlashtirilgan holat.
</content>
</invoke>
