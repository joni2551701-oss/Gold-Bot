# GBA-001 — ARCHITECTURE AUDIT REPORT

## 1. Layer Direction va Foundation Freeze muvofiqligi

`ARCHITECTURE.md` va `CLAUDE.md`da belgilangan qatlam yo'nalishi:
`data_layer -> context_layer -> core_layer(pipeline) -> strategy_layer
-> signal_layer -> ai_layer -> decision_layer -> risk_layer ->
execution_layer -> trade_monitoring_layer -> database_layer ->
platform_layer`.

Kod bazasidagi fayl soni har bir Layer bo'yicha (`find <layer> -name
'*.py' | wc -l` orqali tasdiqlangan):

| Layer | .py fayllar soni |
|---|---|
| data_layer | 232 |
| ai_layer | 273 |
| core_layer | 111 |
| platform_layer | 65 |
| database_layer | 44 |
| context_layer | 41 |
| strategy_layer | 40 |
| backtesting_layer | 38 |
| signal_layer | 26 |
| chart_layer | 21 |
| media_layer | 20 |
| execution_layer | 16 |
| decision_layer | 15 |
| trade_monitoring_layer | 14 |
| risk_layer | 12 |
| indicator_layer | 10 |
| future_expansion | 1 |

Barcha 17 Layer jismoniy papka sifatida mavjud (`ls` bilan
tasdiqlangan repo ildizida). `future_expansion` faqat 1 ta `.py`
faylga ega — bu qatlam kelajak uchun rezervlangan, hozircha deyarli
bo'sh (real defect emas, chunki nomi ham shuni anglatadi).

## 2. Trading Safety chegaralari — kodda tasdiqlangan

**AI -> Decision -> Risk -> Execution zanjiri.**
`ai_layer/*/interfaces.py`dagi `AIAnalyzerInterface` docstringi (fayl:
`ai_layer/ai_engine/interfaces.py` atrofida, aniq satr 67-80) aniq
belgilaydi: AI provayder hech qachon o'zi trade approve/reject
qilmaydi, `RiskManager`ni chaqirmaydi, Telegram yuborishni
ishga tushirmaydi. Buni tasdiqlash uchun:

```
grep -n "RiskManager\|risk_manager\|telegram" decision_layer/decision_engine/decision_engine.py
```
natijasi faqat docstring ichida `risk.risk_manager.RiskResult`ga
matn shaklidagi izoh, real chaqiruv yo'q — ya'ni DecisionEngine
o'zi RiskManager'ni chaqirmaydi (bu ataylab: Risk Manager
DecisionEngine'dan KEYIN, pipeline darajasida chaqiriladi, pastga
qarang).

**RiskManager joylashuvi:** `risk_layer/risk_engine/risk_manager.py`
(fayl mavjudligi tasdiqlangan). `core_layer/pipeline/pipeline.py`
orkestratori har bir signalni Risk bosqichidan o'tkazadi — `python
main.py` smoke-run logida `stage=risk` bosqichi haqiqatda ishlaydi
(03_RUNTIME_REPORT.md'ga qarang).

**Execution Layer — ataylab inert.** `execution_layer/execution_engine/execution_engine.py`:

```python
class ExecutionEngine:
    """
    Execution Layer — signal dispatch contract only.
    No MT5, no Telegram, no HTTP, no Database, no Logger,
    no async/threading/queue. No knowledge of message formatting
    or delivery mechanics.
    """
    def dispatch(self, risk_result: RiskResult) -> ExecutionResult:
        """
        Entry point for Execution Layer. Currently unimplemented --
        orchestration and delivery mechanics will be wired in a
        future phase.
        """
```

`grep -rln "mt5\|MetaTrader\|order_send" -i execution_layer/`
natijasida real MT5 chaqiruvi TOPILMADI — faqat docstringda "No
MT5" degan inkor jumla bor. Xulosa: bu **by design** holat, CLAUDE.md
"Execution rules — execution/ is intentionally inert" qoidasiga mos
keladi. Defect emas.

## 3. Cross-layer import kuzatuvi — bitta e'tiborga molik topilma

`ai_layer/` bir nechta modulda (`ai_layer/vision_ai/content_adapter.py`,
`ai_layer/ai_engine/trading_analyst/content_adapter.py`,
`ai_layer/ai_engine/intelligence_runtime.py`, `ai_layer/voice_ai/adapter.py`)
`media_layer.telegram_broadcast.*`dan import qiladi:

```
ai_layer/ai_engine/intelligence_runtime.py:53:from media_layer.telegram_broadcast.broadcast_adapter import broadcast_asset_from_content_and_media
ai_layer/ai_engine/intelligence_runtime.py:54:from media_layer.telegram_broadcast.broadcast_manager import BroadcastManager
```

Tekshiruv: `media_layer/telegram_broadcast/broadcast_adapter.py`da
`bot.send`, `requests.`, `Bot(` kabi haqiqiy yuborish chaqiruvi
TOPILMADI — funksiya faqat `BroadcastAsset` ma'lumot obyektini
yig'adi (data assembly), real Telegram API chaqiruvi qilmaydi. Demak
bu AI qatlamining "Telegram yuborishni ishga tushirmasligi" qoidasini
buzmaydi.

Ammo bu **CLAUDE.md "Keep modules isolated: ai/ doesn't import
database/, etc."** qoidasi nuqtai nazaridan arxitektura tozaligi
bo'yicha kichik og'ish hisoblanadi — `ai_layer` `media_layer`ga
to'g'ridan-to'g'ri bog'liq, holbuki ARCHITECTURE.md'dagi rasmiy oqim
buni ko'rsatmaydi (media_layer alohida branch sifatida
ko'rsatilgan). Bu **Major emas, Minor** darajadagi topilma — chunki
faktik xatti-harakat xavfsiz (send chaqirilmaydi), lekin qatlam
chegarasi rasmiy diagrammada hujjatlashtirilmagan. Batafsil —
`14_MAJOR_ISSUES.md` va `15_MINOR_ISSUES.md`.

## 4. Duplicate/legacy papkalar

`database/` (faqat `goldbot.db` runtime SQLite fayli, `.py` fayl yo'q)
va `database_layer/` (44 ta `.py` fayl, to'liq Repository/Service
struktura) — bular DUPLIKAT EMAS: `database/` shunchaki runtime
ma'lumotlar bazasi fayli saqlanadigan joy, kod moduli emas.

## 5. Qisman ko'rib chiqilgan qismlar

Import graph va circular dependency uchun to'liq avtomatik grafik
qurish vaqt cheklovi tufayli amalga oshirilmadi — buning o'rniga
maqsadli `grep` orqali Trading Safety qatlamlari (ai_layer, decision_layer,
risk_layer, execution_layer) chegaralari qo'lda tekshirildi (yuqorida).
Qolgan 13 Layer orasidagi to'liq import grafigi namunaviy tarzda
`08_IMPORT_GRAPH_REPORT.md`da berilgan, exhaustive emas.
