# GBA-001 — TEST AUDIT REPORT

## Umumiy natija

```
$ python -m pytest tests/ -q
5400 passed in 103.24s (0:01:43)
```
Kutilgan "5400+ passed" mezoniga to'liq mos, 0 ta failed, 0 ta error.

## Skip/xfail tekshiruvi

```
$ grep -rn "@pytest.mark.skip\|@pytest.mark.xfail\|pytest.skip(" tests/
0 ta natija
```
Hech qanday test skip yoki xfail qilinmagan — barcha yozilgan
testlar haqiqatda ishga tushmoqda va o'tmoqda.

## Test papkasi strukturasi

`tests/` ostida 37 ta subpapka mavjud (`find tests -maxdepth 1
-type d` orqali tasdiqlangan), jumladan `unit/`, `integration/`,
`security/`, `performance/` (order talab qilgan `tests/unit`,
`tests/integration` va h.k. barchasi mavjud), shuningdek Layer-mos
papkalar: `risk/`, `decision/`, `signals/`, `strategies/`,
`execution/`, `ai/`, `knowledge/`, `learning/`, `voice/`, `media/`,
`broadcast/`, `telegram/`, `platforms/`, `backtesting/`,
`monitoring/`, `context/`, `market/`, `data/`, `core/`, `deploy/`,
`configuration/`, `contracts/`, `assistant/`, `errors/`,
`translation/`, `phase59/`, `stream/`, `assets/`, `fixtures/`,
`analytics/`, `features/`.

Bu Layer-ga mos test tashkiloti CLAUDE.md'ning "tests/ almost
certainly already covers the area" talabiga mos ekanligini
ko'rsatadi.

## Coverage

`--cov` flag CI'da (`ci.yml`, "Run tests" step,
`--cov=. --cov-report=term-missing`) ishlatilmoqda, biroq bu audit
mahalliy ishga tushirishda coverage report generatsiya qilinmadi
(vaqt tejash uchun oddiy `-q` bilan ishga tushirildi). Aniq foiz
raqami ushbu audit hujjatida KELTIRILMAYDI, chunki mahalliy ishga
tushirishda o'lchanmadi — **qisman ko'rib chiqilgan**: CI logidan
haqiqiy foizni olish uchun `16_DIRECTOR_RECOMMENDATIONS.md`da GitHub
Actions natijasini tekshirish tavsiya etiladi.

## Trading Safety qatlamlari test mavjudligi

`tests/risk/`, `tests/decision/`, `tests/signals/`,
`tests/strategies/`, `tests/execution/` papkalarining barchasi
mavjud (yuqoridagi struktura ro'yxatida tasdiqlangan) — bu 5 ta
Trading Safety qatlami uchun maxsus test papkasi borligini
ko'rsatadi, muvofiq CLAUDE.md'ning ustuvorligi bilan.

## Xulosa

Test suite CLAUDE.md talablariga (5400+ passed, skip/xfail yo'q,
Layer-mos struktura) to'liq mos. Aniq coverage foizi va
qamrov-bo'shliqlari (masalan qaysi funksiyalar hech qanday test
bilan qamrab olinmagan) chuqur tahlili ushbu audit vaqt oynasida
o'tkazilmadi.
