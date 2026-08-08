# 23 — Core → Context (TASK-01)

## Transition
Core → Context (ContextService Market Context'ni egallaydi; ContextEngine
faqat orchestrate qiladi).

## Input
`candles` — market_data bosqichi Market Memory SSOT'dan qaytargan candle
seriyasi (REAL-DATA-003 isbotlagan), plus `htf_bias`.
Evidence: `core_layer/pipeline/pipeline.py:325` (`get_candles`, SSOT),
`core_layer/pipeline/pipeline.py:358` (`htf_bias`).

## Processing (file:line)
- Pipeline chaqiruvi: `core_layer/pipeline/pipeline.py:369`
  `context = build_context_snapshot(candles, htf_bias)`.
- Funksional entry point: `context_layer/context_engine/context_orchestrator/context_orchestrator.py:289`
  `build_context_snapshot(...)` → `ContextEngine(ContextConfig()).build(...)`.
- Orchestratsiya: `context_layer/context_engine/context_orchestrator/context_orchestrator.py:107`
  `ContextEngine.build()` — barcha detektorlarni ketma-ket chaqiradi
  (`:121-132`).

## Output
`ContextSnapshot` (frozen dataclass) — to'liq Smart Money konteksti.
Evidence: `context_layer/context_engine/context_orchestrator/context_orchestrator.py:35-72`,
qurish: `:134-147`.

## Next Consumer
- `market_phase` bosqichi — `core_layer/pipeline/pipeline.py:381`.
- `signal` bosqichi (SignalEngine) — `core_layer/pipeline/pipeline.py:405`.

## Ownership-rule check
Canonical qoida: "ContextService Market Context'ni egallaydi; ContextEngine
faqat orchestrate qiladi." Runtime holati:
- Live runtime'da Market Context'ni `ContextEngine` (context_orchestrator)
  quradi va orchestrate qiladi — u faqat detektorlarga delegatsiya qiladi,
  yangi detection mantiqini o'zi hisoblamaydi (`_build_*` metodlari
  mavjud modullarni chaqiradi, `:169-286`). Bu "faqat orchestrate qiladi"
  qoidasiga mos.
- `ContextService` paketi (`context_layer/context_service/__init__.py:1-13`)
  Foundation Freeze v1.0 skeleton (faqat docstring) — live pipeline yo'lida
  emas.

**Ownership eslatma (STOP emas):** runtime'da alohida live `ContextService`
Market Context egasi sifatida ishtirok etmaydi; egalik `ContextEngine`da.
Bu hujjatlashtirilgan Foundation Freeze / MIR-001 migration holati (skeleton
paket, live behavior engine'da), canonical arxitekturaga zid RUNTIME
CONFLICT emas. Layer chegarasi buzilmagan.

## Status
**PASS** — Core → Context real kod bilan tasdiqlangan. `build_context_snapshot`
SSOT candle'larni iste'mol qiladi va `ContextSnapshot` chiqaradi.
Ownership: orchestratsiya `ContextEngine`da; `ContextService` skeleton
(Foundation Freeze).
</content>
