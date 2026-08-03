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

Runtime Data

↓

Data Validation Layer

↓

Validated Data

---

# Internal Structure

Data_Validation/

├── README.md
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
├── Layer_Contracts.md
│
├── ValidationService/
├── DataValidator/
├── SchemaValidator/
├── QualityValidator/
├── IntegrityValidator/
└── ValidationLifecycle/

---

# Module Overview

## ValidationService

Data Validation Layer'ning markaziy Orchestrator'i.

---

## DataValidator

Birinchi (Primary) Validation bosqichi.

---

## SchemaValidator

Data strukturasi va Schema'sini tekshiradi.

---

## QualityValidator

Data sifatini tekshiradi.

---

## IntegrityValidator

Data yaxlitligini tekshiradi.

---

## ValidationLifecycle

Barcha Validation jarayonlarining Lifecycle'ini kuzatadi.

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

Runtime Data

↓

ValidationService

↓

DataValidator

↓

SchemaValidator

↓

QualityValidator

↓

IntegrityValidator

↓

ValidationLifecycle

↓

Validated Data

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
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
├── Layer_Contracts.md
│
├── ValidationService/
├── DataValidator/
├── SchemaValidator/
├── QualityValidator/
├── IntegrityValidator/
└── ValidationLifecycle/

Har bir modul o'z README.md, Contracts.md, ModuleMap.md va SequenceDiagram.md hujjatlariga ega bo'lishi kerak.

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
