# GBA-002 — Merge Strategy (Variant A/B/C uchun texnik asos)

Bu hujjat `09_DIRECTOR_RECOMMENDATION.md`dagi uchta variant uchun
texnik amalga oshirish yo'lini tasvirlaydi — hech biri bu auditda
bajarilmadi (read-only cheklov).

## Umumiy texnik dalillar (barcha variantlar uchun asos)

- Umumiy ajdod (`merge-base`): `ed6a5e995d3d07febf8e6fd4a130fcd3750649fc`.
- `goldbot-v1`ning noyob 396 commiti — asosiy kod rivojlanishi (`.py`
  fayllarning katta qismi).
- `main`ning noyob 144 commiti — sof hujjat (`.md`) fayllari, `.py`ga
  tegmaydi.
- Fast-forward hech qanday yo'nalishda mumkin emas.

## Variant A — `goldbot-v1 -> main -> Production`

**Texnik yo'l:** `main`ni `goldbot-v1`ning holatiga yangilash — amalda
`git checkout main && git merge goldbot-v1` (yoki tenglashtirish
uchun `git reset --hard goldbot-v1` + force-push, agar tarixni
tozalash xohlansa) orqali. `main`ning noyob 144 hujjat-commiti
(`.py`ga tegmagani uchun) merge paytida yo'qolib ketishi mumkin, agar
ular `goldbot-v1`dagi tegishli fayllar bilan avtomatik birlashtirilmasa
— bu holatda ularni alohida cherry-pick qilish yoki `docs/`
arxivlash orqali saqlab qolish tavsiya etiladi.

**Risk:** Past-o'rta — `.py` konflikt xavfi past (main faylga
tegmagan), lekin `main`ning 144 hujjat commiti e'tiborsiz qoldirilishi
mumkin (mazmunan eskirgan bo'lsa ham, tarixiy yo'qotish sifatida
hisoblanadi).

## Variant B — `main -> goldbot-v1`

**Texnik yo'l:** `goldbot-v1`ga `main`ning noyob 144 commitini olib
kirish — `git checkout goldbot-v1 && git merge main`. Bu commit'lar
sof hujjat bo'lgani uchun, `.py` konflikt xavfi yo'q, lekin `.md`
fayl yo'llari (`New_Map/` uslubidagi eski struktura) `goldbot-v1`dagi
joriy 17-Layer hujjat strukturasiga mos kelmasligi mumkin — natijada
ikki xil, parallel hujjat tuzilishi paydo bo'ladi (eski `New_Map/`
qatlami + joriy `docs/`/har-modul README tuzilishi), bu chalkashlik
keltirib chiqarishi mumkin.

**Risk:** Past — `goldbot-v1`ning `.py` kodiga hech qanday ta'sir
yo'q, faqat hujjat qatlamiga eski/keraksiz fayllar qo'shilishi mumkin.

## Variant C — `Release Branch -> main`

**Texnik yo'l:** `goldbot-v1`dan yangi `release/v1.0` (yoki mos nom)
branch'i kesib olinadi (`git checkout -b release/v1.0 goldbot-v1`),
u yerda stabilizatsiya (RC tayyorlash, `07_RELEASE_CANDIDATE_PLAN.md`
shartlari) bajariladi, so'ng shu release branch `main`ga merge
qilinadi (Variant A bilan bir xil texnik oqim, lekin oraliq
stabilizatsiya bosqichi bilan).

**Risk:** Eng past — `goldbot-v1`ning o'zi hech qachon to'g'ridan-
to'g'ri `main`ga tegmaydi, oraliq branch xatolarni ushlab qolish
imkonini beradi, `RELEASE_MANAGEMENT_STANDARD.md`ning RC bosqichi
bilan tabiiy mos keladi.

## Umumiy texnik tavsiya (Merge Strategy nuqtai nazaridan, faqat texnik, Director qarori emas)

`.py`/`.md` konflikt xavfi past bo'lgani uchun, texnik jihatdan
barcha uch variant amalga oshirilishi mumkin. Farq — jarayon
qattiqligi va risk boshqaruvida, Variant C eng xavfsiz oraliq bosqich
beradi. To'liq pros/cons/risk tahlili — `09_DIRECTOR_RECOMMENDATION.md`.
