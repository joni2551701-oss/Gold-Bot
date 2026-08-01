# GoldBot Core

Status: CANONICAL

---

# Purpose

GoldBot Core — Senior Trading AI ekotizimining yuragi hisoblanadi.

Uning yagona vazifasi Data Layer'dan kelgan market ma'lumotlarini tahlil qilish, barcha hisob-kitoblarni bajarish va yakuniy savdo qarorini ishlab chiqishdir.

GoldBot Core tashqi providerlar bilan ishlamaydi va foydalanuvchi interfeysini boshqarmaydi.

---

# Objective

GoldBot Core quyidagi vazifalarni bajaradi:

• Market Structure hisoblash

• Market Context yaratish

• Technical Analysis bajarish

• Trading Strategy ishlatish

• Confluence hisoblash

• Decision chiqarish

• Risk hisoblash

• Signal yaratish

• Monitoring

• Simulation

---

# Layer Position

Data Layer

↓

GOLDBOT CORE

↓

Application Services

↓

Platform Layer

↓

User

---

# Internal Structure

GoldBot_Core/

├── README.md
│
├── Market_Engine/
│
├── Context_Engine/
│
├── Analysis_Engine/
│
├── Strategy_Engine/
│
├── Confluence_Engine/
│
├── Decision_Engine/
│
├── Risk_Engine/
│
├── Signal_Engine/
│
├── Monitoring/
│
└── Simulation/

---

# Module Overview

## Market_Engine

Bozorning asosiy holatini hisoblaydi.

---

## Context_Engine

Market Context yaratadi.

Trend, Liquidity, Session va boshqa omillarni aniqlaydi.

---

## Analysis_Engine

Texnik analizlarni bajaradi.

SMC, ICT, Wyckoff, AMD va boshqa analiz modullari shu yerda joylashadi.

---

## Strategy_Engine

Trading strategiyalarini boshqaradi.

Strategiyalarni ishga tushiradi va natijalarini tayyorlaydi.

---

## Confluence_Engine

Turli analiz va strategiya natijalarini birlashtirib yagona baho hosil qiladi.

---

## Decision_Engine

BUY

SELL

NONE

yakuniy qarorni ishlab chiqadi.

---

## Risk_Engine

Risk Management.

Lot Size.

Position Size.

Risk/Reward.

Capital Protection.

---

## Signal_Engine

Yakuniy signal obyektini yaratadi.

Signal hali foydalanuvchiga yuborilmaydi.

---

## Monitoring

Ichki monitoring.

Performance.

Health.

Diagnostics.

---

## Simulation

Backtesting.

Replay.

Simulation.

Strategy Testing.

---

# Responsibilities

GoldBot Core:

✓ Market Analysis

✓ Context Calculation

✓ Technical Analysis

✓ Strategy Execution

✓ Confluence

✓ Decision

✓ Risk Calculation

✓ Signal Generation

✓ Monitoring

✓ Simulation

---

# Not Responsible

GoldBot Core:

✗ Historical Download

✗ Live Stream

✗ Provider Connection

✗ Data Validation

✗ Market Memory

✗ Telegram

✗ Mobile

✗ Desktop

✗ Web

✗ AI Chat

✗ User Interface

✗ Payment

✗ Subscription

---

# Core Flow

Data Layer

↓

Market Engine

↓

Context Engine

↓

Analysis Engine

↓

Strategy Engine

↓

Confluence Engine

↓

Decision Engine

↓

Risk Engine

↓

Signal Engine

↓

GoldBot Core API

---

# Golden Rules

1. Core faqat hisoblaydi.

2. Core providerlar bilan ishlamaydi.

3. Core UI haqida bilmaydi.

4. Core Telegram haqida bilmaydi.

5. Core AI bilan bog'lanmaydi.

6. Core faqat Data Layer ma'lumotlarini ishlatadi.

7. Har bir Engine faqat bitta vazifaga ega.

8. Decision faqat Decision Engine tomonidan chiqariladi.

9. Risk faqat Risk Engine tomonidan hisoblanadi.

10. Signal faqat Signal Engine tomonidan yaratiladi.

---

# Repository Structure

GoldBot_Core/

├── README.md
│
├── Market_Engine/
├── Context_Engine/
├── Analysis_Engine/
├── Strategy_Engine/
├── Confluence_Engine/
├── Decision_Engine/
├── Risk_Engine/
├── Signal_Engine/
├── Monitoring/
└── Simulation/

Har bir papka o'z README.md fayliga ega bo'lishi kerak.

Har bir .py fayl uchun mos specification (.md) mavjud bo'lishi kerak.

---

# Refactoring Rule

Repository GoldBot Core blueprint'iga moslashtiriladi.

Kod blueprint'ga mos kelishi shart.

Blueprint kodga moslashtirilmaydi.

---

# Summary

GoldBot Core — GoldBot tizimining hisoblash markazi hisoblanadi.

Uning vazifasi:

• marketni tahlil qilish;

• context yaratish;

• strategiyalarni bajarish;

• riskni hisoblash;

• yakuniy signalni ishlab chiqish.

GoldBot Core tashqi providerlar, platformalar va foydalanuvchi interfeysi bilan ishlamaydi. Uning yagona vazifasi ishonchli va mustaqil hisob-kitoblarni bajarishdir.
