# GBA-001 — DIRECTOR RECOMMENDATIONS (DRQ-001 formatida)

## Savol 1: `ai_layer -> media_layer.telegram_broadcast` bog'liqligi qonuniylashtirilsinmi?

**Muammo:** `ai_layer`ning 4+ moduli `media_layer.telegram_broadcast`dan
import qiladi, bu ARCHITECTURE.md'da hujjatlashtirilmagan chegara.

**Ildiz sababi (root cause):** `BroadcastAsset` yaratish logikasi
`media_layer`da joylashgan, lekin AI kontent generatsiya qilgandan
keyin uni broadcast-ga tayyor formatga o'rashi kerak — bu ehtiyoj
qondirilganda arxitektura hujjati yangilanmagan (dokumentatsiya
qarzi).

**Ta'sir doirasi:** `ai_layer` (4 fayl), `ARCHITECTURE.md`.

**Xavf darajasi:** Past-o'rta (Low-Medium) — funksional xavf yo'q
(real send chaqiruvi yo'q), lekin kelajakdagi kengaytirish uchun
noto'g'ri naqsh namunasi bo'lishi mumkin.

**Variantlar:**
1. **ARCHITECTURE.md'ni yangilash** — `ai_layer -> media_layer`
   chetini rasmiy diagrammaga, "faqat data-assembly, execution/send
   emas" izohi bilan qo'shish.
   - Ijobiy: minimal, kod o'zgarmaydi, tezkor.
   - Salbiy: chegara "yumshoq" bo'lib qoladi, kelajakda kimdir shu
     yo'ldan haqiqiy `send` chaqiruvini qo'shishi mumkin.
2. **`BroadcastAsset` yig'ish logikasini `ai_layer`ning o'z ichiga
   ko'chirish**, `media_layer`ni faqat haqiqiy yuborish (delivery)
   uchun qoldirish.
   - Ijobiy: chegara yanada qattiqroq bo'ladi.
   - Salbiy: kod o'zgarishi talab qiladi (Module Reuse Principle va
     Trading Safety qoidalariga ko'ra Director tasdig'i kerak),
     mavjud testlarni yangilashni talab qilishi mumkin.
3. **Hozirgi holatni o'zgarishsiz qoldirish**, faqat kelgusi
   auditlarda kuzatib borish.
   - Ijobiy: hech qanday xatar yo'q.
   - Salbiy: dokumentatsiya-kod mos kelmasligi davom etadi.

**Worker tavsiyasi:** Variant 1 (ARCHITECTURE.md yangilash) —
tezkor, past xatarli, va joriy xavfsiz xatti-harakatni aniq
hujjatlashtiradi. Variant 2 faqat agar Director bu chegarani
strategik jihatdan muhim deb hisoblasa ko'rib chiqilsin.

## Savol 2: `goldbot-v1` va `main` branch farqi

**Muammo:** Production deploy faqat `main`dan ishlaydi
(`production_deploy.yml`), audit `goldbot-v1`da o'tkazildi.

**Ildiz sababi:** Order aniq `goldbot-v1`da qolishni talab qildi;
bu branch bilan `main` orasidagi munosabat (masalan, `goldbot-v1`
kelgusi release branch'imi yoki `main`dan orqada qolganmi) audit
doirasida aniqlashtirilmadi.

**Ta'sir doirasi:** Butun audit natijasining production'ga
tegishliligi.

**Xavf darajasi:** O'rta (Medium) — agar `main` bilan katta farq bo'lsa,
bu audit "eskirgan" bo'lishi mumkin.

**Variantlar:**
1. Director `goldbot-v1` va `main` munosabatini tasdiqlasin
   (masalan: "`goldbot-v1` — keyingi release, `main`ga hali merge
   qilinmagan").
2. Keyingi GBA audit siklini `main`da takrorlash.
3. Ikkala branch'ni `git diff main..goldbot-v1 --stat` bilan
   solishtirib, farq hajmini hujjatlashtirish (Worker read-only
   qila oladi, kod o'zgartirmaydi).

**Worker tavsiyasi:** Variant 3 — tezkor va past xatarli, keyingi
qadam uchun aniq ma'lumot beradi, Director qaroriga asos bo'ladi.

**Qo'shimcha dalil (Variant 3 bajarildi):**
```
$ git diff origin/main..origin/goldbot-v1 --stat
5768 files changed, 186912 insertions(+), 43351 deletions(-)
```
Bu **juda katta farq** — `origin/main`da hali eski, pre-refactor
struktura (masalan top-level `voice/` papkasi, hozirgi
`ai_layer/voice_ai/`ning o'rniga) mavjud ko'rinadi. Bu
`production_deploy.yml`ning "main -- the single authoritative
production branch" bayonoti bilan ziddiyatga o'xshaydi: agar
`origin/main` haqiqatan ham hozirgi production'ni boshqarayotgan
bo'lsa, u holda **production hozirda ushbu auditda ko'rilgan
17-Layer arxitekturasidan sezilarli darajada orqada qolgan** bo'lishi
mumkin. Bu topilma Critical emas (chunki u kodning o'zidagi
buzilish emas, balki branch-sinxronizatsiya holati haqida savol),
lekin **darhol Director tasdig'ini talab qiladigan yuqori
ustuvorlikdagi ochiq savol** sifatida qayd etiladi.

## Savol 3: Test coverage foizi va importtime profiling

**Muammo:** Aniq coverage foizi va import-vaqti breakdown ushbu
audit doirasida o'lchanmadi.

**Ildiz sababi:** Vaqt cheklovi — bu ikkinchi darajali metrikalar
sifatida ustuvorlik past qo'yildi.

**Ta'sir doirasi:** Performance va Test hujjatlarining to'liqligi.

**Xavf darajasi:** Past (Low).

**Variantlar:**
1. Keyingi Sprintda alohida "Performance & Coverage Deep-Dive"
   vazifasi sifatida rejalashtirish.
2. Hozircha e'tiborsiz qoldirish (past ustuvorlik).

**Worker tavsiyasi:** Variant 1, past ustuvorlik bilan backlog'ga
qo'shilsin (Worker o'z Backlog Management vakolati doirasida
CLAUDE.md Order No. 016 asosida buni mustaqil bajarishi mumkin).
