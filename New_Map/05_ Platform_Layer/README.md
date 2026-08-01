# Platform Layer

Status: CANONICAL

---

# Purpose

Platform Layer — Senior Trading AI ekotizimining barcha platformalarini birlashtiruvchi qatlamdir.

Uning asosiy vazifasi GoldBot xizmatlarini turli platformalar orqali foydalanuvchilarga taqdim etishdir.

Platform Layer hech qanday market tahlili yoki savdo qarorini hisoblamaydi.

---

# Objective

Platform Layer quyidagi vazifalarni bajaradi:

• Telegram Platform

• Mobile Application

• Desktop Application

• Web Platform

• Public API

• Authentication

• User Session

• Request Routing

• Platform Integration

---

# Layer Position

GoldBot Core

↓

Application Services

↓

AI Layer

↓

PLATFORM LAYER

↓

User

---

# Internal Structure

Platform_Layer/

├── README.md
│
├── Telegram/
│
├── Mobile/
│
├── Desktop/
│
├── Web/
│
└── Public_API/

---

# Module Overview

## Telegram

Telegram Bot.

Telegram Mini App.

Telegram Commands.

Telegram Notifications.

---

## Mobile

Android.

iOS.

Push Notifications.

Offline Cache.

---

## Desktop

Windows.

macOS.

Linux.

Desktop Client.

---

## Web

Web Dashboard.

Trading Panel.

Analytics Dashboard.

Administration Panel.

---

## Public_API

REST API.

WebSocket API.

SDK Integration.

Third-party Integration.

---

# Responsibilities

Platform Layer:

✓ User Interface

✓ User Requests

✓ Authentication

✓ Authorization

✓ Session Management

✓ API Routing

✓ Platform Communication

✓ Push Notifications

✓ Device Integration

---

# Not Responsible

Platform Layer:

✗ Historical Download

✗ Live Stream

✗ Market Memory

✗ Market Analysis

✗ Context Calculation

✗ Strategy

✗ Confluence

✗ Decision

✗ Risk Calculation

✗ Signal Calculation

✗ AI Decision

---

# Platform Flow

User

↓

Platform

↓

Platform Layer

↓

Application Services

↓

GoldBot Core

↓

Application Services

↓

Platform Layer

↓

User

---

# Golden Rules

1. Platform Layer hech qachon Core bilan to'g'ridan-to'g'ri ishlamaydi.

2. Platform Layer faqat Application Services orqali ishlaydi.

3. Platform Layer hisob-kitob qilmaydi.

4. Platform Layer Decision chiqarmaydi.

5. Platform Layer Risk hisoblamaydi.

6. Platform Layer Signal yaratmaydi.

7. Platform Layer AI o'rniga javob bermaydi.

8. Har bir platforma mustaqil rivojlantirilishi mumkin.

9. Barcha platformalar yagona API standartidan foydalanadi.

10. Platform Layer faqat foydalanuvchi va tizim o'rtasidagi aloqa qatlamidir.

---

# Repository Structure

Platform_Layer/

├── README.md
│
├── Telegram/
├── Mobile/
├── Desktop/
├── Web/
└── Public_API/

Har bir platforma o'z README.md fayliga ega bo'lishi kerak.

Har bir .py fayl uchun mos specification (.md) mavjud bo'lishi kerak.

---

# Refactoring Rule

Repository Platform Layer blueprint'iga moslashtiriladi.

Kod blueprint'ga mos kelishi shart.

Blueprint kodga moslashtirilmaydi.

---

# Summary

Platform Layer — foydalanuvchi ishlatadigan barcha platformalarni birlashtiruvchi qatlamdir.

Uning vazifasi:

• GoldBot xizmatlarini platformalarga yetkazish;

• foydalanuvchi so'rovlarini qabul qilish;

• autentifikatsiya va sessiyalarni boshqarish;

• yagona API orqali barcha platformalarni ishlatish.

Platform Layer hech qachon marketni tahlil qilmaydi, savdo qarorini hisoblamaydi yoki signal yaratmaydi. U faqat Application Services orqali GoldBot imkoniyatlarini foydalanuvchiga taqdim etadi.
