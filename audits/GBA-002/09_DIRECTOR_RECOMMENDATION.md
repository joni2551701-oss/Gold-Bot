# GBA-002 — Director Recommendation (DRQ-001 formatida)

## Muammo tavsifi

`origin/main` (rasmiy "single authoritative production branch",
`production_deploy.yml`ga ko'ra) va `origin/goldbot-v1` (joriy
development branch) o'rtasida haqiqiy divergence mavjud: 5786 fayl,
+188132/-43351 qator farq, `goldbot-v1`da 396 ta noyob commit,
`main`da 144 ta noyob commit (barchasi hujjat-darajali, `.py`ga
tegmaydi). Fast-forward hech qaysi yo'nalishda mumkin emas. Bu
GBA-001'dan beri hal qilinmagan ochiq savol (`16_DIRECTOR_
RECOMMENDATIONS.md` Savol 2, `18_VPS_READINESS_VERDICT.md` Required
Fix #1) — endi to'liq Evidence bilan Director qaroriga taqdim
etiladi.

## Root Cause Analysis

`goldbot-v1` production kod bazasining haqiqiy rivojlanish maydoni
bo'lgan (17-Layer arxitekturasi, barcha Phase/Task ishlari shu yerda
amalga oshirilgan), `main` esa CI/CD konfiguratsiyasida "production"
deb belgilangan bo'lsada, amalda faqat qo'lda (GitHub veb-muharriri
orqali, "Gold Bot" hisobi bilan) hujjat fayllari qo'shilgan holda
qoldirilgan — hech qachon rasmiy ravishda `goldbot-v1`dagi rivojlanish
bilan sinxronlashtirilmagan.

## Ta'sir doirasi

Butun repozitoriy — qaysi kod haqiqatda VPS production'da ishlashi
kerakligini belgilaydigan strategik qaror. `production_deploy.yml`
CI/CD workflow'i, barcha kelajakdagi audit/deploy ishlari shu qarorga
bog'liq.

## Risk darajasi: **Yuqori (High)**

Sabab: agar hozirgi `production_deploy.yml` sozlamasi bo'yicha `main`
haqiqatan ham VPS'ni boshqarayotgan bo'lsa, production hozirda
`goldbot-v1`dagi 17-Layer arxitekturasidan sezilarli darajada orqada
qolgan (eski struktura, masalan `voice/` o'rniga `ai_layer/voice_ai/`
kabi). Bu vaziyat aniqlashtirilmasa, keyingi har qanday deploy/audit
ishi "qaysi kodga tegishli" degan noaniqlikda qoladi.

## Variantlar

### Variant A: `goldbot-v1 -> main -> Production`

**Tavsif:** `goldbot-v1`ni `main`ga promote qilish (merge yoki
tenglashtirish), so'ng shu yangilangan `main`dan deploy qilish.

- **Ijobiy:** `main` haqiqiy, joriy 17-Layer arxitekturasini aks
  ettiradigan holga keladi; `production_deploy.yml`ning "main —
  single authoritative production branch" bayonoti bilan mos keladi
  (o'zgarishsiz); kelajakda branch-chalkashligi tugaydi.
- **Salbiy:** `main`ning noyob 144 hujjat-commiti e'tiborsiz
  qoldirilishi yoki alohida saqlanishi kerak bo'ladi (yo'qotish
  xavfi, past darajada); katta hajmli bitta promote operatsiyasi
  (5786 fayl) — review qilish qiyin.
- **Xavf:** O'rta — texnik `.py` konflikt xavfi past (`08_MERGE_
  STRATEGY.md`), lekin operatsion hajm katta.

### Variant B: `main -> goldbot-v1`

**Tavsif:** `main`ning noyob 144 hujjat-commitini `goldbot-v1`ga olib
kirish, `goldbot-v1`ni davom ettirish, `main`ni hozircha
o'zgartirmaslik.

- **Ijobiy:** Eng past xavfli, kod bazasiga ta'sir yo'q, hech narsa
  yo'qolmaydi.
- **Salbiy:** Asosiy muammoni (production `main`dan ishlaydi, lekin
  `main` eski) **hal qilmaydi** — production hamon eski koddan
  ishlab turaveradi, agar `production_deploy.yml` o'zgartirilmasa.
  Bu — masalani kechiktirish, hal qilish emas.
- **Xavf:** Past texnik, lekin **Yuqori strategik** — production
  eskirganligicha qoladi, deploy muammosi yechilmaydi.

### Variant C: `Release Branch -> main`

**Tavsif:** `goldbot-v1`dan yangi `release/v1.0` branch kesib
olinadi, u yerda RC1 shartlari (`07_RELEASE_CANDIDATE_PLAN.md`)
bajariladi va stabilizatsiya o'tkaziladi, so'ng shu release branch
`main`ga merge qilinadi.

- **Ijobiy:** `RELEASE_MANAGEMENT_STANDARD.md`ning rasmiy Release
  Lifecycle (RC bosqichi)ga to'liq mos keladi; xato ehtimolini oraliq
  bosqichda ushlab qolish imkoni bor; `goldbot-v1`ning o'zi hech
  qachon to'g'ridan-to'g'ri `main`ga tegmaydi (development branch
  xavfsiz qoladi); Director Order No. 020'ning talab qilgan Release
  Checklist'i shu jarayonga tabiiy ravishda joylashadi.
- **Salbiy:** Eng ko'p vaqt talab qiladigan variant (qo'shimcha
  bosqich); yakuniy natija baribir Variant A bilan bir xil holatga
  olib keladi (`main` yangilanadi), faqat oraliq nazorat bilan.
- **Xavf:** Past — eng nazoratli yo'l, GDS/Release Management
  standartlariga to'liq mos.

## Worker tavsiyasi

**Variant C** tavsiya etiladi. Asos: (1) Director Order No. 020
(Release Management Standard) allaqachon aynan shu oqimni talab
qiladi — Worker Authority Release Candidate darajasida to'xtaydi,
Production Release Director tasdig'ini talab qiladi; Variant C bu
zanjirni tabiiy ravishda qondiradi. (2) `main`ning 396 commitlik
farqni bitta ulkan promote operatsiyasida yutib yuborishi (Variant A)
review imkoniyatini kamaytiradi; Release Branch orqali bosqichma-
bosqich stabilizatsiya bu xavfni kamaytiradi. (3) Variant B asosiy
muammoni (production qaysi koddan ishlaydi) hal qilmagani uchun
yetarli emas — faqat Variant A yoki C production'ni haqiqiy holatga
keltiradi.

**Ochiq savol Director qaroriga:** Variant A/B/C'dan qaysi biri
tanlanadi — va agar Variant C tanlansa, `release/v1.0` branch nomi va
RC1 muddati (Sprint rejasi) tasdiqlanishi kerak.
