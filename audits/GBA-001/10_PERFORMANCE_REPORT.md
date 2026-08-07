# GBA-001 — PERFORMANCE AUDIT REPORT

## Startup vaqti

```
$ time (timeout 60 python main.py)
real  0m5.773s
user  0m5.156s
sys   0m0.591s
exit=0
```
`main.py` to'liq bir marta ishga tushib (konfiguratsiya yuklash,
database schema init, TelegramBot init urinishi, to'liq pipeline
tsikli — 15 stage) tugashi jami ~5.8 soniya oldi. Pipeline'ning
o'z ichki `duration` log yozuvi (`pipeline_finished duration=0.003s`)
shuni ko'rsatadiki, asosiy vaqt sarfi Python interpretatori/import
yuklanishida (moduli ~840 ta `.py` fayl, `ai_layer` yolg'iz 273 ta),
database schema initsializatsiyasida ketmoqda, pipeline'ning o'zi
(tashqi API javobisiz, "quruq" holatda) millisoniyalarda tugaydi.

## Test suite ishlash vaqti

```
$ python -m pytest tests/ -q
5400 passed in 103.24s (0:01:43)
```
5400 ta test ~103 soniyada (rebase'dan oldingi birinchi o'lchov), ya'ni o'rtacha test boshiga ~19ms.

## Lazy loading / import strukturasi

Chuqur profiling (masalan `cProfile`/`py-spy`) ushbu audit doirasida
BAJARILMADI — vaqt cheklovi tufayli **qisman ko'rib chiqilgan**.
Buning o'rniga bilvosita ko'rsatkich sifatida import hajmi
kuzatildi: `ai_layer` (273 fayl) va `data_layer` (232 fayl) repo'ning
eng katta ikkita qatlami — bu `main.py` startup vaqtining sezilarli
qismini import bosqichi egallashi mumkinligini ko'rsatadi, biroq
buni raqamli tasdiqlash uchun `python -X importtime main.py` kabi
maxsus profiling keyingi Sprintga tavsiya etiladi.

## Xotira/CPU

Konteyner ichida to'g'ridan-to'g'ri xotira/CPU monitoring vositasi
(masalan `/usr/bin/time -v`) ishlatilmadi — bu ham qisman ko'rib
chiqilgan qism. `time` buyrug'ining `user`/`sys` ustunlari (5.156s /
0.591s) CPU sarfi haqida qo'pol taxmin beradi, lekin peak-memory
o'lchovi yo'q.

## Xulosa

Berilgan sinov muhitida (tashqi API kalitlarisiz) startup va bitta
pipeline tsikli tezkor (~6s, asosan import/init sarfi). Chuqur
profiling (import vaqti breakdown, xotira peak) keyingi Sprint uchun
tavsiya etilgan backlog elementi — hozircha performance muammosi
yoki og'ir "bottleneck" TOPILMADI, lekin buni rad etuvchi to'liq
profiling ham o'tkazilmadi.
