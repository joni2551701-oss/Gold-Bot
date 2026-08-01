# Application Services

Status: CANONICAL

---

# Purpose

Application Services — GoldBot Core va tashqi platformalar orasidagi xizmat (Service) qatlamidir.

Bu qatlam GoldBot Core tomonidan yaratilgan natijalarni standart servislar orqali Telegram, Mobile, Desktop, Web va boshqa platformalarga taqdim etadi.

Application Services hech qanday market tahlili yoki savdo qarorini hisoblamaydi.

---

# Objective

Application Services quyidagi vazifalarni bajaradi:

• GoldBot Core xizmatlarini tashqi tizimlarga taqdim etish

• Platformalar uchun yagona Service API yaratish

• Business Layer bilan integratsiya qilish

• Platformalardan kelgan so'rovlarni boshqarish

• Core natijalarini standart formatga o'tkazish

---

# Layer Position

GoldBot Core

↓

APPLICATION SERVICES

↓

AI Layer

↓

Platform Layer

↓

User

---

# Internal Structure

Application_Services/

├── README.md
│
├── Signal_Service/
│
├── Chart_Service/
│
├── AI_Service/
│
├── Notification_Service/
│
├── Replay_Service/
│
├── Analytics_Service/
│
├── User_Service/
│
└── Portfolio_Service/

---

# Module Overview

## Signal_Service

GoldBot Core signalini platformalar uchun tayyorlaydi.

---

## Chart_Service

Chart ma'lumotlarini tayyorlaydi va platformalarga uzatadi.

---

## AI_Service

Senior AI va Seniorita AI uchun kerakli ma'lumotlarni tayyorlaydi.

---

## Notification_Service

Signal, ogohlantirish va tizim xabarlarini yuborishni boshqaradi.

---

## Replay_Service

Trade Replay va tarixiy sessiyalarni taqdim etadi.

---

## Analytics_Service

Statistika va analitik ma'lumotlarni tayyorlaydi.

---

## User_Service

Foydalanuvchi bilan bog'liq servislarni boshqaradi.

---

## Portfolio_Service

Portfolio va hisob statistikalarini boshqaradi.

---

# Responsibilities

Application Services:

✓ Service API

✓ Request Handling

✓ Response Formatting

✓ Platform Integration

✓ User Services

✓ Notification Services

✓ Analytics Services

✓ Replay Services

---

# Not Responsible

Application Services:

✗ Historical Download

✗ Live Stream

✗ Data Validation

✗ Market Memory

✗ Market Analysis

✗ Context Calculation

✗ Strategy

✗ Decision

✗ Risk Calculation

✗ Signal Calculation

✗ User Interface Rendering

✗ AI Decision

---

# Service Flow

GoldBot Core

↓

Application Services

↓

Platform Layer

↓

Telegram

↓

Mobile

↓

Desktop

↓

Web

---

# Golden Rules

1. Application Services hech qachon marketni hisoblamaydi.

2. Application Services Core o'rniga qaror chiqarmaydi.

3. Barcha platformalar faqat Application Services orqali ishlaydi.

4. Core bilan to'g'ridan-to'g'ri faqat Service API ishlaydi.

5. Platformalar Core'ni bevosita chaqirmaydi.

6. Servislar stateless bo'lishi tavsiya etiladi.

7. Har bir Service bitta vazifaga ega.

8. Servislar platformaga bog'liq bo'lmasligi kerak.

9. Response formatlari standart bo'lishi kerak.

10. Application Services — Core va Platform o'rtasidagi yagona ko'prik.

---

# Repository Structure

Application_Services/

├── README.md
│
├── Signal_Service/
├── Chart_Service/
├── AI_Service/
├── Notification_Service/
├── Replay_Service/
├── Analytics_Service/
├── User_Service/
└── Portfolio_Service/

Har bir papka o'z README.md fayliga ega bo'lishi kerak.

Har bir .py fayl uchun mos specification (.md) mavjud bo'lishi kerak.

---

# Refactoring Rule

Repository Application Services blueprint'iga moslashtiriladi.

Kod blueprint'ga mos kelishi shart.

Blueprint kodga moslashtirilmaydi.

---

# Summary

Application Services — GoldBot Core va tashqi platformalar o'rtasidagi servis qatlamidir.

Uning vazifasi:

• Core xizmatlarini standart servis sifatida taqdim etish;

• platformalar bilan integratsiyani boshqarish;

• foydalanuvchi va biznes servislarini birlashtirish.

Application Services hech qachon marketni tahlil qilmaydi va savdo qarorini hisoblamaydi. Barcha platformalar GoldBot Core imkoniyatlaridan faqat shu qatlam orqali foydalanadi.
