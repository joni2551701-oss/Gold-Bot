# Data Validation

Status: CANONICAL

---

# Purpose

Data Validation — Data Layer ichidagi barcha market ma'lumotlarining ishonchliligi va yaxlitligini (Integrity) ta'minlovchi bo'limdir.

Uning asosiy vazifasi Historical Data va Live Data'dan kelgan barcha ma'lumotlarni tekshirish, noto'g'ri yoki buzilgan ma'lumotlarni aniqlash va faqat tasdiqlangan (Validated) ma'lumotlarni Market Memory'ga uzatishdir.

Data Validation hech qachon marketni tahlil qilmaydi va savdo qarorini hisoblamaydi.

---

# Objective

Data Validation quyidagi vazifalarni bajaradi:

• Tick Validation

• Candle Validation

• Data Quality Control

• Data Integrity Check

• Duplicate Detection

• Missing Data Detection

• Invalid Data Rejection

• Validation Reporting

---

# Layer Position

Historical Data

+

Live Data

↓

Data Validation

↓

Market Memory

↓

GoldBot Core

---

# Internal Structure

Data_Validation/

├── README.md
│
├── DataValidation.md
├── TickValidation.md
├── CandleValidation.md
├── DataQuality.md
├── ValidationFlow.md
├── SequenceDiagram.md
└── ModuleMap.md

---

# Module Overview

## DataValidation

Validation jarayonining markaziy boshqaruvchisi.

Barcha Validation modullarini boshqaradi.

---

## TickValidation

Har bir Live Tick ma'lumotini tekshiradi.

Narx.

Timestamp.

Asset.

Duplicate Tick.

Sequence.

---

## CandleValidation

Har bir OHLC Candle ma'lumotini tekshiradi.

Open.

High.

Low.

Close.

Volume.

Timeframe.

---

## DataQuality

Market ma'lumotlari sifatini baholaydi.

Missing Data.

Corrupted Data.

Gap Detection.

Consistency Check.

Quality Score.

---

## ValidationFlow

Validation jarayonining to'liq oqimini tavsiflaydi.

---

## SequenceDiagram

Validation ishlash ketma-ketligini ko'rsatadi.

---

## ModuleMap

Validation modullari orasidagi bog'lanishni ko'rsatadi.

---

# Responsibilities

Data Validation:

✓ Validate Tick

✓ Validate Candle

✓ Check Data Integrity

✓ Detect Invalid Data

✓ Reject Corrupted Data

✓ Check Data Quality

✓ Protect Market Memory

✓ Generate Validation Result

---

# Not Responsible

Data Validation:

✗ Historical Download

✗ Live Streaming

✗ Candle Building

✗ Market Memory Storage

✗ Market Analysis

✗ Context Engine

✗ Strategy Engine

✗ Decision Engine

✗ Signal Generation

---

# Validation Flow

Historical Data

+

Live Data

↓

Data Validation

↓

Validation Result

↓

Market Memory

↓

GoldBot Core

---

# Golden Rules

1. Har bir ma'lumot Validation'dan o'tishi shart.

2. Validation'dan o'tmagan ma'lumot Market Memory'ga yozilmaydi.

3. Tick va Candle alohida tekshiriladi.

4. Duplicate ma'lumotlar rad etiladi.

5. Corrupted Data rad etiladi.

6. Missing Data aniqlanadi va qayd etiladi.

7. Validation biznes logikasini bajarmaydi.

8. Validation faqat ma'lumot sifatini tekshiradi.

9. Validation natijalari standart formatda qaytariladi.

10. Market Memory faqat tasdiqlangan ma'lumotlarni qabul qiladi.

---

# Repository Structure

Data_Validation/

├── README.md
├── DataValidation.md
├── TickValidation.md
├── CandleValidation.md
├── DataQuality.md
├── ValidationFlow.md
├── SequenceDiagram.md
└── ModuleMap.md

Har bir modul o'z specification hujjatiga ega bo'lishi kerak.

---

# Refactoring Rule

Repository Data Validation blueprint'iga moslashtiriladi.

Kod blueprint'ga mos kelishi shart.

Blueprint kodga moslashtirilmaydi.

---

# Summary

Data Validation — Data Layer ichidagi ma'lumot sifati va ishonchliligini nazorat qiluvchi bo'lim hisoblanadi.

Uning vazifasi:

• Historical va Live Data ma'lumotlarini tekshirish;

• Tick va Candle ma'lumotlarini validatsiya qilish;

• noto'g'ri va buzilgan ma'lumotlarni rad etish;

• Market Memory'ni faqat tasdiqlangan ma'lumotlar bilan to'ldirish.

Data Validation hech qachon marketni tahlil qilmaydi va savdo qarorini hisoblamaydi. Uning yagona vazifasi GoldBot ekotizimida ishlatiladigan barcha market ma'lumotlarining aniqligi, yaxlitligi va ishonchliligini ta'minlashdir.
