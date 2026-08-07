# GBA-001 — MAJOR ISSUES

## MAJOR-001: `ai_layer` -> `media_layer.telegram_broadcast` hujjatlashtirilmagan bog'liqlik

**Tavsif:** `ai_layer/ai_engine/intelligence_runtime.py` (53-54
satrlar), `ai_layer/vision_ai/content_adapter.py` (34-36 satrlar),
`ai_layer/ai_engine/trading_analyst/content_adapter.py` (29-31
satrlar), `ai_layer/voice_ai/adapter.py` (32-satr) —
`media_layer.telegram_broadcast.broadcast_adapter`,
`broadcast_manager`, `models`dan import qiladi.

**Nima uchun Major (Critical emas):** Funksional tekshiruv
(`grep -n "def broadcast_asset_from_content_and_media\|def send\|
requests\.\|bot\.send\|Bot(" media_layer/telegram_broadcast/*.py`)
shuni ko'rsatdiki, bu chaqirilgan funksiyalar faqat `BroadcastAsset`
ma'lumot ob'ektini yig'adi — real Telegram API chaqiruvi
(`bot.send`/`requests.*`) bu fayllarda YO'Q. Demak AI hech qachon
o'zi Telegram'ga signal yubormaydi (Trading Safety buzilmagan).
Ammo bu ARCHITECTURE.md'dagi rasmiy Layer diagrammasida aniq
ko'rsatilmagan qo'shimcha bog'liqlik yo'nalishi — kelajakda kimdir
(inson yoki AI agent) bu naqshni "AI Telegram'ga to'g'ridan-to'g'ri
yozishi mumkin ekan" deb noto'g'ri talqin qilib, xavfli kengaytirish
qilishi mumkin.

**Ta'sir doirasi:** `ai_layer` (4+ fayl), arxitektura hujjatlari
(`ARCHITECTURE.md`).

**Tavsiya:** `ARCHITECTURE.md`ga `ai_layer -> media_layer` chetini
(faqat data-assembly maqsadida, real send yo'q) aniq
hujjatlashtirish YOKI (agar Director buni chegara buzilishi deb
hisoblasa) `BroadcastAsset` yig'ish logikasini `media_layer`dan
`ai_layer`ning o'z hududiga ko'chirish — bu ikkinchisi kod
o'zgarishi talab qiladi, ushbu audit doirasida amalga
OSHIRILMAYDI, faqat Director Review uchun tavsiya sifatida qayd
etiladi (`16_DIRECTOR_RECOMMENDATIONS.md`da options bilan).

## MAJOR-002: `goldbot-v1` va `main` (production) branch farqi aniqlanmagan

**Tavsif:** `production_deploy.yml` faqat `main`dan deploy qiladi,
audit esa `goldbot-v1`da o'tkazilmoqda. Ushbu audit natijalari
`goldbot-v1`ning holatini aks ettiradi — agar `main` bilan farq katta
bo'lsa, bu audit production'dagi haqiqiy holatni to'liq aks
ettirmasligi mumkin.

**Ta'sir doirasi:** Butun audit natijasining production'ga
tegishliligi.

**Tavsiya:** Director `main` va `goldbot-v1` orasidagi farqni
tasdiqlashi yoki keyingi GBA auditni `main`da o'tkazishni buyurishi
kerak.

**Qo'shimcha dalil:** `git diff origin/main..origin/goldbot-v1
--stat` — **5768 fayl o'zgargan, 186912 qo'shilgan / 43351 o'chirilgan
qator**. Bu nihoyatda katta farq bo'lib, `origin/main`da eski
(pre-Layer-refactor, masalan top-level `voice/` papkasi) struktura
borligini ko'rsatadi. `production_deploy.yml`ning o'z izohi "main --
the single authoritative production branch" deb aytadi — demak
production hozirgi 17-Layer arxitekturasidan ancha orqada qolgan
bo'lishi ehtimoli bor. Bu ushbu MAJOR-002ni **yuqori ustuvorlikka**
ko'taradi va `18_VPS_READINESS_VERDICT.md`ga ta'sir qiladi.

## Boshqa Major darajadagi topilma yo'q

Qolgan barcha tekshirilgan sohalarda (Runtime, Test, CI, Security,
Dead Code) Major darajadagi muammo TOPILMADI.
