# GBA-001 — MINOR ISSUES

## MINOR-001: `future_expansion/` Layer deyarli bo'sh

Faqat 1 ta `.py` fayl. Bu ataylab shunday ko'rinadi (nomi va
kontekstidan), lekin hech qanday README/CONTRACTS hujjati ushbu
audit doirasida uning maqsadini tasdiqlamadi (namunaviy
tekshiruvda qamrab olinmadi). Tavsiya: bu papka uchun ham boshqa
Layer'lar kabi standart README/WORK_LOG borligini tasdiqlash.

## MINOR-002: Test coverage foizi hujjatlashtirilmagan

`ci.yml`da `--cov=. --cov-report=term-missing` ishlatiladi, lekin
ushbu audit mahalliy ishga tushirishda coverage report
generatsiya qilmadi (vaqt tejash). Aniq foiz raqami GitHub Actions
loglaridan olinishi kerak.

## MINOR-003: Import-vaqti (`importtime`) profiling yo'q

`main.py`ning ~5.8 soniyalik startup vaqtining qancha qismi import
yuklanishiga, qancha qismi database schema initsializatsiyasiga
ketishi aniq ajratilmagan. `python -X importtime main.py` bilan
keyingi Sprintda profiling tavsiya etiladi (Performance Optimization
— CLAUDE.md Worker Authority ostida ruxsat etilgan ish turi).

## MINOR-004: Circular-import grafigi avtomatlashtirilmagan

`08_IMPORT_GRAPH_REPORT.md`da qayd etilgan — hozircha faqat
bilvosita dalil (importlar muvaffaqiyatli, xatosiz) mavjud, rasmiy
vosita-asosidagi grafik yo'q.

## MINOR-005: `.env*` fayllarning to'liq git tarixi tekshirilmagan

Joriy holat toza, lekin tarixiy commitlarda tasodifiy sir sizib
chiqqan-chiqmaganligi bo'yicha maxsus secret-scanning (masalan
`gh secret-scanning` yoki `trufflehog`) ishlatilmadi.

## Xulosa

Minor darajadagi topilmalar barchasi "keyinroq yaxshilash mumkin"
toifasida — hech biri production deploy'ga to'siq emas.
