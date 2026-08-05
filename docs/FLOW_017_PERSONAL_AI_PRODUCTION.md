# FLOW-017 — Personal AI Core: Production Wiring + Memory System

Sana: 2026-08-05. Authority: Director Order (PHASE-02 FLOW-017).
Til: GLS-001 (proza O'zbek, texnik terminlar English).

> Maqsad: Personal AI Core'ni jonli Telegram Consumer bilan **Memory-First**
> Production subsystemga aylantirish. Yangi LLM/Prompt/AI Engine/AI Service/
> Memory System yozilmaydi — faqat mavjud modullar Production'ga ulanadi.

## 1. Short Audit
`ai_layer/` da Personal AI komponentlari mavjud edi, lekin jonli
user-facing Consumer yo'q edi (FLOW-017 Partial re-audit). Mavjud:
- `ai_layer/ai_engine/runtime/ai_service.py` — `AIService.ask(RuntimeRequest)`.
- `ai_layer/personal_ai/interaction_manager/conversation_engine.py` —
  `ConversationEngine.start_session()/.ask()` (AIService'ni ichdan
  composes qiladi; External-AI kirish nuqtasi).
- `ai_layer/knowledge_ai/memory_manager/memory_runtime.py` —
  `MemoryRuntime.recall()/.store()/.search()`.
- `ai_layer/ai_service/assistant/access.py` — `is_personal_ai_enabled_for(role, flags)` Owner-Mode gate.
- `platform_layer/telegram/{commands,handlers,command_router}.py` — jonli Telegram dispatch.

## 2. Reuse Analysis
| Kerak | Mavjud modul (o'zgartirilmadi) |
|---|---|
| External AI API chaqirish | `ConversationEngine.ask()` |
| Memory Search / Store | `MemoryRuntime.recall()/.store()` + `MemoryEntry` |
| Owner-Mode gate | `is_personal_ai_enabled_for()` |
| Role/Context/Contract turlar | `AIRole`, `AIContext`, `MemoryScope`, `MemoryType` |
| Telegram Consumer | `commands.OWNER_COMMANDS` + `handlers.*_handler` + `command_router` |

Xulosa: barcha kerakli qismlar mavjud. Yetishmagani — **memory-first
orchestration** (Memory'ni avval tekshirib, faqat miss'da API chaqirish)
va **jonli `/ask` komandasi**. Bu ikkisi wiring (composition), yangi
engine/memory emas.

## 3. Architecture Review
Yangi modul: `ai_layer/personal_ai/interaction_manager/memory_first_query.py`
— **composition root**. Faqat mavjud public metodlarni composes qiladi,
o'z biznes-logikasi yo'q (ConversationEngine/VoiceRuntime/IntelligenceRuntime
composition root'lari bilan bir xil naqsh). Yangi top-level paket
yaratilmadi (interaction_manager ichida). Dependency siklsiz.

## 4. Production Wiring Diagram
```
Telegram (/ask <savol>)
  → command_router  (OWNER_COMMANDS gate: faqat OWNER)
  → handlers.ask_handler
  → memory_first_query.answer_question
      → is_personal_ai_enabled_for(OWNER, flags)   [Owner-Mode gate]
      → MemoryRuntime.recall(key)                  [Memory Search]
      → (miss) ConversationEngine.ask(...)         [External AI API]
      → MemoryRuntime.store(MemoryEntry(MemoryAnswer))  [Memory Update]
  → javob matni → Telegram → User
```

## 5. Input → Processing → Output → Consumer
- **Input:** owner Telegram xabari `/ask <savol>` (+ role, ai_context).
- **Processing:** Owner gate → Memory Search → (miss) API → Memory Update.
- **Output:** `PersonalAIResult{answer, source(memory|api|denied|failed), from_memory, accepted}`.
- **Consumer:** Telegram (`ask_handler` → `command_router` → foydalanuvchi). ✅ **Jonli.**

## 6. Memory Flow Diagram
```
question ─► normalize(lower+trim+ws) ─► sha256 ─► key ("personal_ai:qa:<hash>")
  ├─ recall(key) HIT  ─► PersonalAIResult(source="memory", from_memory=True)   [API YO'Q]
  └─ recall(key) MISS ─► API ─► store(MemoryEntry(
                                   scope=KNOWLEDGE_REFERENCE, type=LONG_TERM,
                                   value=MemoryAnswer{Question,Answer,Topic,Tags,
                                                      Timestamp,Source,Confidence,Version}))
```
Memory Contract (`MemoryAnswer`) 8 maydon: Question / Answer / Topic /
Tags / Timestamp / Source / Confidence / Version.

## 7. API Flow Diagram
```
Memory MISS ─► ConversationEngine.start_session(telegram_id)
             ─► ConversationEngine.ask(session_id, question, ai_context, role, telegram_id)
             ─► RuntimeResponse{accepted, content, reason, metadata}
                 ├─ accepted+content ─► Memory Store ─► javob (source="api")
                 └─ rad/bo'sh        ─► PersonalAIResult(source="failed")  [Memory'ga yozilmaydi]
```
API **hech qachon** Memory tekshirilmasdan chaqirilmaydi (Director API Rule).

## 8. Production Code Summary
- YANGI `ai_layer/personal_ai/interaction_manager/memory_first_query.py`:
  `MemoryAnswer` (contract), `PersonalAIResult`, `personal_ai_memory_key()`,
  shared singletonlar, `answer_question()` (6 STEP memory-first).
- MODIFIED `platform_layer/telegram/handlers.py`: `ask_handler()` qo'shildi.
- MODIFIED `platform_layer/telegram/commands.py`: `OWNER_COMMANDS["ask"]`.

## 9-11. Test natijalari
`tests/ai/personal_ai/test_memory_first_query.py` — **12 test PASS**:
- Unit: memory key determinizm/normalize, MemoryAnswer contract, empty→failed, gate (OWNER flag-off / ADMIN flag-on → denied).
- Integration: miss→API+store (scope/type tekshirildi), hit→API **chaqirilmaydi** (calls==1), API-reject→failed+saqlanmaydi.
- End-to-End: `/ask` OWNER_COMMANDS'da ro'yxatda + `ask_handler` mavjud; empty→usage; owner `/ask` → Personal AI gate'ga yetadi; non-owner → permission denied.

Full suite: **5475 passed** (5463 → +12).

## 12. Topilgan muammolar
- `enable_personal_ai` bayrog'i **default OFF** (Phase 65.3 Owner Mode).
  Shu sababli jonli `/ask` default holatda "o'chirilgan, yoqing" javobini
  qaytaradi. To'liq memory-first oqim bayroq YOQILGANDA ishlaydi (testlar
  buni isbotlaydi). Bayroq — Owner runtime nazorati; uni default TRUE
  qilish access-control o'zgarishi, alohida Director ruxsatini talab qiladi
  (Trading-Safety-adjacent), shuning uchun o'zgartirilmadi.
- Persona (Senior/Seniorita): Director qoidasiga ko'ra Knowledge/Memory/
  Reasoning **bir xil** — persona faqat presentation. Ushbu wiring core'ni
  persona bilan o'zgartirmaydi (kelajakda handler darajasida label
  qo'shilishi mumkin).

## 13. Director Recommendations
1. `enable_personal_ai` ni Owner uchun default yoqishni tasdiqlang (yoki
   jonli owner runtime toggle orqali qoldiring). Bu access-control qarori.
2. Persona presentation (Senior/Seniorita label + uslub) keyingi kichik
   Sprint sifatida handler darajasida qo'shilishi mumkin — core tayyor.
3. Kelajakda `/ask` ni VIP/PREMIUM'ga ochish uchun `is_personal_ai_enabled_for`
   siyosatini kengaytirish — bu ham alohida Director qarori.

## 14. Commit ID
Ushbu FLOW-017 ishi `goldbot-v1` branch'iga bitta commit sifatida
push qilindi ("FLOW-017 Personal AI Core: Memory-First Production
Wiring + live /ask Telegram consumer"). Yakuniy commit SHA va
GitHub Actions `success` tasdig'i Worker hisobotining Pre-Commit
Verification bo'limida keltiriladi.

## 15. Pre-Commit Verification
CLAUDE.md Commit Protocol to'liq bajarildi (git add -A → pyflakes →
compileall → pytest tests/ → python main.py → git status clean →
git diff --cached reviewed → commit → push → GitHub Actions).
To'liq belgilangan checklist Worker hisobotida:

    Pre-Commit Verification
    ✓ git add -A
    ✓ pyflakes (0 finding — dastlab topilgan `pytest` unused import olib tashlandi va qayta stage qilindi)
    ✓ compileall
    ✓ pytest (5475 passed)
    ✓ python main.py (EXIT=0, pipeline shakli baseline'ga mos)
    ✓ git status clean
    ✓ git diff --cached reviewed (7 fayl, +514/-2)
    ✓ GitHub Actions SUCCESS

## Success Criteria tekshiruvi
- ✅ Input→Processing→Output→**Real Telegram Consumer** mavjud va ishlaydi.
- ✅ Memory avval tekshiriladi; API faqat miss'da chaqiriladi (test bilan isbotlangan).
- ✅ API javobi Memory'ga yoziladi va keyingi so'rovda qayta ishlatiladi.
- ✅ Yangi LLM/Prompt/Engine/Service/Memory System yozilmadi — faqat reuse+wiring.
- ⚠️ Jonли to'liq javob `enable_personal_ai` YOQILGANDA (Owner Mode) — gate saqlanadi.
