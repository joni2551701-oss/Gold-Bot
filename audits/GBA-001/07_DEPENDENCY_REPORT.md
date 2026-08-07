# GBA-001 — DEPENDENCY REPORT

## Tashqi paketlar

`requirements.txt` va `requirements-freeze.txt` repo ildizida mavjud
(`ls` orqali tasdiqlangan). CI (`ci.yml`) `pip install -r
requirements.txt` (yoki freeze fayl) orqali o'rnatadi (satr 38
atrofida `Install dependencies` step).

## Qatlamlararo bog'liqlik (dependency direction)

`02_ARCHITECTURE_REPORT.md`da keltirilgan `grep`-asosli tekshiruvlar
CLAUDE.md'dagi "no direct database access from Telegram handlers",
"ai/ doesn't import database/" kabi qoidalarga mos kelishini
tasdiqladi:

- `grep -rln "^import database\|^from database" ai_layer/` — 0 ta
  natija (ai_layer database_layer'ni import qilmaydi).
- `decision_layer/decision_engine/decision_engine.py` RiskManager'ni
  to'g'ridan-to'g'ri chaqirmaydi (faqat docstring matnida eslatilgan).
- `execution_layer` hech qanday tashqi (MT5/HTTP) bog'liqlikka ega
  emas — bu ataylab shunday (Trading Safety, "by design").

## E'tiborga molik topilma — ai_layer -> media_layer

`ai_layer/ai_engine/intelligence_runtime.py`,
`ai_layer/vision_ai/content_adapter.py`,
`ai_layer/ai_engine/trading_analyst/content_adapter.py`,
`ai_layer/voice_ai/adapter.py` — bularning barchasi
`media_layer.telegram_broadcast.*`dan import qiladi. Bu
ARCHITECTURE.md'dagi rasmiy Layer diagrammasida aniq
hujjatlashtirilmagan qo'shimcha bog'liqlik yo'nalishi (ai_layer ->
media_layer). Funksional tekshiruv shuni ko'rsatdiki, bu import
faqat ma'lumot ob'ektlari (`BroadcastAsset`) yig'ish uchun, real
Telegram API chaqiruvi (`bot.send`, `requests.*`) bu fayllarda
TOPILMADI. Xavfsizlik nuqtai nazaridan zararsiz, lekin arxitektura
hujjatlashtirish nuqtai nazaridan aniqlik kiritish talab etiladi —
batafsil `14_MAJOR_ISSUES.md`/`15_MINOR_ISSUES.md`da.

## Circular dependency

To'liq avtomatlashtirilgan circular-import grafigi (masalan
`pydeps`/`pyan` kabi vosita bilan) ushbu audit vaqt oynasida
QURILMADI — bu **qisman ko'rib chiqilgan** qism. Buning o'rniga
`python main.py` va `python -m pytest tests/` ikkalasi ham
muvaffaqiyatli bajarildi (xato yo'q, jumladan `ImportError`/circular
import xatosi ham chiqmadi) — bu circular dependency yo'qligining
bilvosita, ammo kuchli amaliy dalili: Python circular import odatda
import vaqtida `ImportError` yoki `AttributeError` bilan yorilib
chiqadi, va bu ikkala real ishga tushirishda ham sodir bo'lmadi.

## Xulosa

Aniqlangan qatlamlararo bog'liqlik yo'nalishlari, bir dona minor
aniqlik masalasidan (`ai_layer -> media_layer.telegram_broadcast`)
tashqari, CLAUDE.md'dagi Layer Isolation qoidalariga mos.
