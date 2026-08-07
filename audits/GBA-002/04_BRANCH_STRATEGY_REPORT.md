# GBA-002 — TASK-02: Branch Strategy Report

## Barcha Branch'lar ro'yxati

**Local branch'lar:**
- `claude/code-analysis-optimization-pwfo3q`
- `claude/collaboration`
- `claude/goldbot-data-layer-architecture-f8dx8j`
- `goldbot-v1` (joriy checkout, `HEAD == origin/goldbot-v1`, 0 ahead/0 behind)

**Remote (`origin/`) branch'lar:**
- `origin/main`
- `origin/goldbot-v1`
- `origin/claude/code-analysis-optimization-pwfo3q`
- `origin/claude/collaboration`
- `origin/claude/goldbot-data-layer-architecture-f8dx8j`
- `origin/Arxiv/main`
- `origin/Arxiv/claude/code-analysis-optimization-pwfo3q`
- `origin/Arxiv/claude/collaboration`
- `origin/Arxiv/claude/goldbot-data-layer-architecture-f8dx8j`

Jami: 2 asosiy branch (`main`, `goldbot-v1`) + 3 `claude/*` ish
branch'i + ularning 4 ta `Arxiv/` arxiv nusxasi (jami 9 ta remote ref).

## Har bir branch bo'yicha holat

| Branch | Oxirgi commit sanasi | Muallif | Ahead/Behind vs `main` | Ahead/Behind vs `goldbot-v1` | Holat |
|---|---|---|---|---|---|
| `origin/main` | 2026-08-01 22:32:24 +0300 | Gold Bot | — | 144 ahead / 396 behind | Faol (production reference), lekin kod jihatidan eski |
| `origin/goldbot-v1` | 2026-08-07 20:25:45 +0000 | Claude | 396 ahead / 144 behind | — | Faol, joriy development branch |
| `origin/claude/code-analysis-optimization-pwfo3q` | 2026-07-30 21:58:08 +0000 | Claude | 0 ahead / 145 behind | 0 ahead / 397 behind | To'liq `goldbot-v1`ga merge qilingan (ancestor) — **stale/dead, xavfsiz o'chirish nomzodi** |
| `origin/claude/collaboration` | 2026-08-03 10:52:24 +0000 | Claude | 256 ahead / 144 behind | 0 ahead / 140 behind | To'liq `goldbot-v1`ga merge qilingan (ancestor) — **stale/dead, xavfsiz o'chirish nomzodi** |
| `origin/claude/goldbot-data-layer-architecture-f8dx8j` | 2026-07-31 20:07:00 +0000 | Claude | 4 ahead / 145 behind | 0 ahead / 393 behind | To'liq `goldbot-v1`ga merge qilingan (ancestor) — **stale/dead, xavfsiz o'chirish nomzodi** |
| `origin/Arxiv/main` | 2026-08-01 22:32:24 +0300 | Gold Bot | 0 ahead / 0 behind (== `main`) | 144 ahead / 396 behind | `main`ning aniq nusxasi — arxiv snapshot, allaqachon arxivlangan holatda |
| `origin/Arxiv/claude/code-analysis-optimization-pwfo3q` | 2026-07-30 21:58:08 +0000 | Claude | == mos `claude/*` branch | == mos `claude/*` branch | Arxiv nusxasi, allaqachon arxivlangan |
| `origin/Arxiv/claude/collaboration` | 2026-08-03 10:52:24 +0000 | Claude | == mos `claude/*` branch | == mos `claude/*` branch | Arxiv nusxasi, allaqachon arxivlangan |
| `origin/Arxiv/claude/goldbot-data-layer-architecture-f8dx8j` | 2026-07-31 20:07:00 +0000 | Claude | == mos `claude/*` branch | == mos `claude/*` branch | Arxiv nusxasi, allaqachon arxivlangan |

**Muhim aniqlik:** Uch (3) ta `claude/*` ish branch'i (`code-analysis-
optimization-pwfo3q`, `collaboration`, `goldbot-data-layer-
architecture-f8dx8j`) `git merge-base --is-ancestor <branch>
origin/goldbot-v1` bo'yicha barchasi **True** natija berdi — ya'ni
ularning har biri to'liq `goldbot-v1` tarixiga singib ketgan (merge
qilingan yoki ularning ustiga qurilib davom ettirilgan). Ularning
ustidagi ish yo'qolmagan — `goldbot-v1` ichida allaqachon mavjud.

`Arxiv/` prefiksli 4 branch — nomlanishidan ko'rinib turibdiki, bular
allaqachon Director/Worker tomonidan qo'lda "arxivlangan" nusxalar
(`main`ning arxiv snapshoti va uch ish branch'ining arxiv nusxalari).
Ular yangi ish uchun ishlatilmaydi, faqat tarixiy referens sifatida
saqlanadi.

## Commit tarixi shakli (linear yoki merge-heavy)

- `origin/main`: 312 ta commit, jumladan 33 ta merge commit.
- `origin/goldbot-v1`: 564 ta commit, jumladan 35 ta merge commit.
- Ikkala branch ham **bir xil umumiy ajdod (`merge-base`)**dan
  boshlangan: commit `ed6a5e995d3d07febf8e6fd4a130fcd3750649fc`.
- `goldbot-v1` chiziqli-emas (35 merge commit) — Claude tomonidan
  ko'plab Phase/Task branch'lari ustida ishlangan, keyin asosiy
  chiziqqa qaytarilgan (odatiy feature-branch->goldbot-v1 ish oqimi
  ko'rinishida).
- `main` ham chiziqli emas (33 merge commit), lekin uning noyob
  (faqat mainda mavjud) 144 ta commiti **0 ta `.py` faylga tegmaydi**
  — barchasi hujjat (`README.md`, `Contracts.md`, `ModuleMap.md`,
  `SequenceDiagram.md`, va shunga o'xshash `New_Map/`-uslubidagi
  fayllar) yaratish/o'chirish/nomini o'zgartirish commit'lari, hammasi
  bitta muallif — "Gold Bot" — tomonidan, ehtimol GitHub veb-
  muharriri orqali to'g'ridan-to'g'ri `main`ga qilingan (batafsil
  dalil `05_GIT_DIVERGENCE_REPORT.md`da).

## Fast-forward imkoniyati

- `git merge-base --is-ancestor origin/main origin/goldbot-v1` ->
  **NO**.
- `git merge-base --is-ancestor origin/goldbot-v1 origin/main` ->
  **NO**.

Xulosa: **hech qanday yo'nalishda fast-forward mumkin emas** — ikkala
branch ham umumiy ajdoddan keyin mustaqil commit qo'shgan (haqiqiy
divergence, faqat "goldbot-v1 mainning davomi" degan sodda holat
emas). Bu GBA-001'ning original topilmasini **to'g'rilaydi**: u faqat
"goldbot-v1 main'dan qancha oldinda" deb hisoblagan, lekin main'ning
o'z tomonidan ham 144 ta noyob commit borligini aniqlamagan edi.

## Merge-conflict xavfi (real merge urinishisiz, diff shaklidan xulosa)

Amaliy merge urinishi bu auditda bajarilmadi (Order konstitutsiyasiga
ko'ra xavfsizroq yo'l — commit graph shaklidan xulosa chiqarish
tanlandi). Xulosa asoslari:

- `main`ning noyob 144 commiti faqat hujjat fayllariga tegadi, va bu
  fayllarning aksariyati (`New_Map/` papkasi ostidagi struktura)
  `goldbot-v1`da **butunlay boshqa yo'lda/tuzilishda** joylashgan
  bo'lishi katta ehtimol (chunki `goldbot-v1`da 17-Layer arxitekturasi
  allaqachon amalga oshirilgan, `main`dagi eski tuzilish emas).
  Demak, ushbu commit'lar orasida **fayl darajasidagi to'qnashuv
  ehtimoli past** (turli yo'llar), lekin **semantik eskirish darajasi
  yuqori** (main'dagi hujjatlar `goldbot-v1`dagi haqiqiy arxitekturani
  aks ettirmaydi).
- `goldbot-v1`ning noyob 396 commiti asosiy kod bazasining deyarli
  butun rivojlanishini o'z ichiga oladi (`.py` fayllarning aksariyati)
  — bu katta hajm birlashtirishda avtomatik/mexanik konflikt emas,
  balki **"qaysi versiya canonical" degan strategik savol**ni
  keltirib chiqaradi (5786 fayl farqi haqiqiy struktura farqi, oddiy
  bir nechta qatorlik konflikt emas).
- Umumiy xulosa: **texnik merge-conflict xavfi past-o'rta** (fayl
  yo'llari asosan mos kelmaydi), lekin **strategik/semantik xavf
  yuqori** (main'ni to'g'ridan-to'g'ri merge qilish 396 ta katta
  commit'ni bitta ulkan merge'ga siqishga majbur qiladi, review qilib
  bo'lmaydigan hajmda).

Batafsil raqamlar — `05_GIT_DIVERGENCE_REPORT.md`.
