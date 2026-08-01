# User Experience Layer

Status: CANONICAL

---

# Purpose

User Experience Layer (UX Layer) — foydalanuvchi GoldBot bilan bevosita ishlaydigan barcha interfeys va tajriba (User Experience) komponentlarini o'z ichiga oladi.

Bu qatlam foydalanuvchiga qulay, tushunarli va interaktiv tajriba yaratish uchun javobgardir.

User Experience Layer hech qanday market tahlili yoki savdo qarorini hisoblamaydi.

---

# Objective

User Experience Layer quyidagi vazifalarni bajaradi:

• Professional Trading Chart

• Trade Journal

• Trade Replay

• Portfolio Dashboard

• Performance Analytics

• Smart Notifications

• Multi Timeframe View

• Drawing Tools

• Trading History

• User Personalization

---

# Layer Position

GoldBot Core

↓

Application Services

↓

Platform Layer

↓

USER EXPERIENCE LAYER

↓

User

---

# Internal Structure

User_Experience/

├── README.md
│
├── Chart_Engine/
│
├── Trade_Journal/
│
├── Replay/
│
├── Analytics/
│
├── Portfolio/
│
├── Notifications/
│
└── Personalization/

---

# Module Overview

## Chart_Engine

Professional trading chart.

Multi Timeframe.

Drawing Tools.

Indicators.

SMC Visualization.

---

## Trade_Journal

Trade tarixini saqlash.

Trade izohlari.

AI Notes.

Screenshot.

Performance Review.

---

## Replay

Trade Replay.

Market Replay.

Historical Session Replay.

Learning Replay.

---

## Analytics

Trading statistikasi.

Win Rate.

RR Analysis.

Equity Curve.

Performance Dashboard.

---

## Portfolio

Hisob statistikasi.

Capital Overview.

Open Positions.

Closed Positions.

Trading History.

---

## Notifications

Push Notifications.

Telegram Notifications.

Email Notifications.

Market Alerts.

Signal Alerts.

---

## Personalization

Theme.

Language.

Layout.

Favorites.

User Preferences.

---

# Responsibilities

User Experience Layer:

✓ Professional Chart

✓ Journal

✓ Replay

✓ Analytics

✓ Portfolio

✓ Notifications

✓ Personalization

✓ User Dashboard

---

# Not Responsible

User Experience Layer:

✗ Historical Download

✗ Live Stream

✗ Market Memory

✗ Market Analysis

✗ Strategy

✗ Decision

✗ Risk Calculation

✗ Signal Generation

✗ AI Decision

✗ Provider Management

---

# User Flow

User

↓

Platform Layer

↓

User Experience

↓

Application Services

↓

GoldBot Core

↓

Application Services

↓

User Experience

↓

Platform Layer

↓

User

---

# Golden Rules

1. UX Layer faqat foydalanuvchi tajribasi uchun javobgar.

2. UX Layer hisob-kitob qilmaydi.

3. UX Layer Core natijalarini o'zgartirmaydi.

4. UX Layer faqat Application Services orqali ishlaydi.

5. Har bir modul foydalanuvchiga qiymat yaratishi kerak.

6. UI va Business Logic ajratilgan bo'lishi kerak.

7. Chart faqat ko'rsatadi, hisoblamaydi.

8. Journal faqat saqlaydi va ko'rsatadi.

9. Replay faqat mavjud ma'lumotlarni qayta ijro etadi.

10. UX Layer foydalanuvchi tajribasini yaxshilash uchun xizmat qiladi.

---

# Repository Structure

User_Experience/

├── README.md
│
├── Chart_Engine/
├── Trade_Journal/
├── Replay/
├── Analytics/
├── Portfolio/
├── Notifications/
└── Personalization/

Har bir papka o'z README.md fayliga ega bo'lishi kerak.

Har bir .py fayl uchun mos specification (.md) mavjud bo'lishi kerak.

---

# Refactoring Rule

Repository User Experience Layer blueprint'iga moslashtiriladi.

Kod blueprint'ga mos kelishi shart.

Blueprint kodga moslashtirilmaydi.

---

# Summary

User Experience Layer — foydalanuvchi GoldBot bilan ishlaydigan barcha interfeys va tajriba komponentlarini boshqaradi.

Uning vazifasi:

• professional chartlarni taqdim etish;

• trading jurnalini yuritish;

• replay va analytics xizmatlarini ko'rsatish;

• portfolio va notification tizimini boshqarish;

• foydalanuvchiga qulay va yagona tajriba yaratish.

User Experience Layer hech qachon marketni tahlil qilmaydi va savdo qarorini hisoblamaydi. U faqat GoldBot Core natijalarini foydalanuvchiga qulay ko'rinishda taqdim etadi.
