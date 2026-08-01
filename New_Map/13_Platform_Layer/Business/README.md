# Business Layer

Status: CANONICAL

---

# Purpose

Business Layer — Senior Trading AI ekotizimining biznes, foydalanuvchi va monetizatsiya jarayonlarini boshqaruvchi qatlamidir.

Uning asosiy vazifasi foydalanuvchilarni boshqarish, obunalarni nazorat qilish, to'lov tizimlari bilan ishlash va platformaning biznes logikasini yuritishdir.

Business Layer hech qachon marketni tahlil qilmaydi va savdo qarorini hisoblamaydi.

---

# Objective

Business Layer quyidagi vazifalarni bajaradi:

• Identity Management

• User Management

• Subscription Management

• Payment Management

• Wallet Management

• Billing

• Referral System

• License Management

• Access Control

• Business Analytics

---

# Layer Position

GoldBot Core

↓

Application Services

↓

Platform Layer

↓

User Experience Layer

↓

BUSINESS LAYER

↓

User

---

# Internal Structure

Business_Layer/

├── README.md
│
├── Identity/
│
├── User_Profile/
│
├── Subscription/
│
├── Payment/
│
├── Wallet/
│
├── Billing/
│
├── Referral/
│
├── License/
│
└── Access_Control/

---

# Module Overview

## Identity

Foydalanuvchi identifikatsiyasi.

Global User ID.

Authentication.

Authorization.

---

## User_Profile

Foydalanuvchi profili.

Settings.

Language.

Preferences.

Devices.

---

## Subscription

Subscription boshqaruvi.

Free.

Pro.

Elite.

Trial.

Expiration.

Renewal.

---

## Payment

To'lov tizimlari.

Payment Gateway.

Invoices.

Transaction History.

Refund.

---

## Wallet

Ichki balans.

Bonus.

Credit.

Reward.

Virtual Wallet.

---

## Billing

Hisob-kitob.

Invoices.

Subscription Billing.

Payment Status.

---

## Referral

Referal tizimi.

Affiliate.

Commission.

Bonus.

Partner Program.

---

## License

Product License.

Activation.

Validation.

Device Binding.

---

## Access_Control

Foydalanuvchi ruxsatlari.

Feature Access.

Role Management.

Permission System.

---

# Responsibilities

Business Layer:

✓ User Management

✓ Authentication

✓ Authorization

✓ Subscription

✓ Payment

✓ Wallet

✓ Billing

✓ Referral

✓ License

✓ Access Control

---

# Not Responsible

Business Layer:

✗ Historical Data

✗ Live Stream

✗ Market Memory

✗ Market Analysis

✗ Context Calculation

✗ Strategy

✗ Decision

✗ Risk Calculation

✗ Signal Generation

✗ Chart Rendering

✗ AI Decision

---

# Business Flow

User

↓

Authentication

↓

Identity

↓

Subscription

↓

Access Control

↓

Application Services

↓

Platform

↓

User

---

# Golden Rules

1. Business Layer faqat biznes logikasini boshqaradi.

2. Business Layer savdo qarorini hisoblamaydi.

3. Subscription faqat Business Layer tomonidan boshqariladi.

4. Payment faqat Business Layer orqali amalga oshiriladi.

5. Access Control yagona markazdan boshqariladi.

6. Identity barcha platformalar uchun yagona bo'ladi.

7. Wallet va Billing bir-biridan mustaqil modullar hisoblanadi.

8. Business Layer GoldBot Core logikasiga aralashmaydi.

9. Har bir biznes moduli Single Responsibility prinsipiga amal qiladi.

10. Business Layer platformaning monetizatsiya markazi hisoblanadi.

---

# Repository Structure

Business_Layer/

├── README.md
│
├── Identity/
├── User_Profile/
├── Subscription/
├── Payment/
├── Wallet/
├── Billing/
├── Referral/
├── License/
└── Access_Control/

Har bir papka o'z README.md fayliga ega bo'lishi kerak.

Har bir .py fayl uchun mos specification (.md) mavjud bo'lishi kerak.

---

# Refactoring Rule

Repository Business Layer blueprint'iga moslashtiriladi.

Kod blueprint'ga mos kelishi shart.

Blueprint kodga moslashtirilmaydi.

---

# Summary

Business Layer — Senior Trading AI ekotizimining biznes markazi hisoblanadi.

Uning vazifasi:

• foydalanuvchilarni boshqarish;

• obunalarni nazorat qilish;

• to'lov va billing tizimlarini yuritish;

• wallet va referral tizimlarini boshqarish;

• platformadagi barcha biznes jarayonlarini yagona markazdan boshqarish.

Business Layer hech qachon marketni tahlil qilmaydi va savdo qarorini hisoblamaydi. Uning vazifasi platformaning tijorat va foydalanuvchi boshqaruvi jarayonlarini ishonchli boshqarishdir.
```
