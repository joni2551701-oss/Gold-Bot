# Historical Data

Status: CANONICAL

---

# Purpose

Historical Data — Data Layer'ning tarixiy bozor ma'lumotlarini boshqaruvchi bo'limidir.

Uning vazifasi providerlardan tarixiy ma'lumotlarni yuklash, tekshirish, saqlash va GoldBot Core foydalanishi uchun tayyor holatga keltirishdir.

Historical Data real vaqt (Live Data) bilan ishlamaydi.

---

# Objective

Historical Data quyidagi vazifalarni bajaradi:

• Historical Data Download

• Bootstrap

• Recovery

• Historical Data Validation

• Historical Data Storage

• Historical Data Synchronization

• Historical Data Integrity

---

# Layer Position

Providers

↓

Historical Data

↓

Data Validation

↓

Market Memory

↓

GoldBot Core

---

# Internal Structure

Historical_Data/

├── README.md
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
├── Layer_Contracts.md
│
├── HistoricalDataService/
├── Bootstrap/
├── Recovery/
├── HistoricalProviders/
├── HistoricalDatabase/
└── HistoricalDataFlow/

---

# Module Overview

## HistoricalDataService

Tarixiy ma'lumotlarni yuklash va boshqaruvchi asosiy servis.

---

## Bootstrap

Tizim ishga tushganda kerakli tarixiy ma'lumotlarni yuklaydi.

---

## Recovery

Uzilishlardan keyin yetishmayotgan tarixiy ma'lumotlarni tiklaydi.

---

## HistoricalProviders

Historical providerlar bilan ishlaydi.

Masalan:

• Twelve Data

• CSV

• Database Backup

---

## HistoricalDatabase

Tarixiy ma'lumotlarni saqlash va o'qish.

---

## HistoricalDataFlow

Historical Data ichidagi ma'lumot oqimini tavsiflaydi.

---

## SequenceDiagram

Historical Data ishlash ketma-ketligini ko'rsatadi.

---

## ModuleMap

Historical Data modullari orasidagi bog'lanishni ko'rsatadi.

---

# Responsibilities

Historical Data:

✓ Download Historical Data

✓ Bootstrap

✓ Recovery

✓ Store Historical Data

✓ Validate Historical Data

✓ Synchronize Historical Data

✓ Prepare Data For Market Memory

---

# Not Responsible

Historical Data:

✗ Live Streaming

✗ Current Price

✗ Candle Building

✗ Event Bus

✗ Market Analysis

✗ Trading Strategy

✗ Decision Engine

✗ Risk Engine

✗ Signal Engine

---

# Historical Flow

Historical Provider

↓

HistoricalDataService

↓

Bootstrap / Recovery

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

GoldBot Core

---

# Golden Rules

1. Historical Data faqat tarixiy ma'lumotlar bilan ishlaydi.

2. Live Data bilan aralashmaydi.

3. Providerlardan kelgan ma'lumot avval tekshiriladi.

4. Noto'g'ri ma'lumot Market Memory'ga yozilmaydi.

5. Bootstrap tizim ishga tushganda ishlaydi.

6. Recovery faqat yetishmayotgan ma'lumotlarni tiklaydi.

7. Historical Database yagona tarixiy manba hisoblanadi.

8. Historical Data GoldBot Core bilan to'g'ridan-to'g'ri ishlamaydi.

9. Barcha ma'lumotlar Data Validation orqali o'tadi.

10. Market Memory'ga faqat tozalangan va tekshirilgan ma'lumot yoziladi.

---

# Repository Structure

Historical_Data/

├── README.md
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
├── Layer_Contracts.md
│
├── HistoricalDataService/
├── Bootstrap/
├── Recovery/
├── HistoricalProviders/
├── HistoricalDatabase/
└── HistoricalDataFlow/

Har bir modul o'z README.md, Contracts.md, ModuleMap.md va SequenceDiagram.md hujjatlariga ega bo'lishi kerak.

---

# Refactoring Rule

Repository Historical Data blueprint'iga moslashtiriladi.

Kod blueprint'ga mos kelishi shart.

Blueprint kodga moslashtirilmaydi.

---

# Summary

Historical Data — Data Layer ichidagi tarixiy ma'lumotlarni boshqaruvchi bo'limdir.

Uning vazifasi:

• tarixiy ma'lumotlarni yuklash;

• bootstrap va recovery jarayonlarini boshqarish;

• ma'lumotlarni tekshirish va saqlash;

• Market Memory uchun ishonchli tarixiy ma'lumot tayyorlash.

Historical Data real vaqt ma'lumotlari bilan ishlamaydi va faqat tarixiy ma'lumotlar oqimi uchun javobgardir.
