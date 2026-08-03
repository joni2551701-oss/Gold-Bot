# GoldBot Canonical Architecture

Status: CANONICAL — Foundation Freeze v1.0

> **Nom o'zgarishi (Phase A.5).** Ushbu arxitektura Foundation Freeze v1.0
> gacha `New_Map/` papkasida saqlanardi. Freeze'dan keyin u endi "yangi
> xarita" emas — u GoldBot v1'ning yagona rasmiy arxitekturasi, shuning uchun
> 17 ta Layer repository root'ga chiqarildi va `New_Map/` nomi bekor qilindi.
> Eski audit hujjatlarida (`docs/*.md`) uchraydigan `New_Map/` havolalari
> tarixiy yozuv sifatida saqlanadi — ular o'sha paytdagi holatni tasvirlaydi.

---

# Purpose

Ushbu hujjat GoldBot repository'ning yakuniy (Target Repository) strukturasini belgilaydi.

Bu papka GoldBot loyihasining barcha kodlari, papkalari va modullarining qayerda joylashishi kerakligini belgilaydi.

Bu hujjat implementatsiya emas.

Bu — repository uchun yagona Canonical Architecture hisoblanadi.

---

# Objective

Canonical Architecture'ning asosiy maqsadi:

- Repository strukturasini standartlashtirish.
- Kodlarni o'z qatlamiga joylashtirish.
- Modul chegaralarini aniq belgilash.
- Dublikat kodlarni yo'qotish.
- Repository'ni kelajakdagi rivojlanish uchun tayyorlash.

---

# Repository Philosophy

Repository yuqoridan pastga quyidagi qatlamlarda quriladi.

01. Data Layer

↓

02. GoldBot Core

↓

03. Application Services

↓

04. AI Layer

↓

05. Platform Layer

↓

06. User Experience

↓

07. Business Layer

↓

08. Learning Layer

↓

09. Media Layer

↓

10. Future Expansion

Har bir modul faqat o'z qatlamida yashashi kerak.

---

# Canonical Rule

Ushbu Canonical Architecture repository uchun yagona manba hisoblanadi.

Repository Canonical Architecture'ga moslashtiriladi.

Canonical Architecture repositoryga moslashtirilmaydi.

Agar repository va Canonical Architecture o'rtasida farq aniqlansa:

Repository refactor qilinadi.

---

# Refactoring Rules

Har bir refactor quyidagi tartibda bajariladi.

Audit

↓

Gap Analysis

↓

Move Files

↓

Rename Files

↓

Refactor Imports

↓

Run Tests

↓

Freeze

Kod hech qachon to'g'ridan-to'g'ri ko'chirilmaydi.

Har bir o'zgarish audit qilinadi.

---

# Layer Rules

Har bir kod faqat bitta qatlamga tegishli bo'lishi mumkin.

Cross-layer logic taqiqlanadi.

Qatlamlar orasidagi bog'lanish faqat ruxsat etilgan dependency orqali amalga oshiriladi.

---

# Module Rules

Har bir modul uchun:

• bitta papka

• bitta specification

• bitta implementation

• bitta javobgarlik

Single Responsibility majburiy.

---

# Documentation Rules

Har bir .py fayl uchun Canonical Architecture ichida specification mavjud bo'lishi kerak.

Specification tugamasdan repository refactor qilinmaydi.

---

# Worker Workflow

Worker quyidagi tartibda ishlaydi.

1. Canonical Architecture'ni o'qiydi.

2. Repository audit qiladi.

3. Farqlarni aniqlaydi.

4. Refactor rejasini tuzadi.

5. Repository'ni Canonical Architecture'ga moslashtiradi.

6. Testlarni ishga tushiradi.

7. Freeze qiladi.

---

# Development Workflow

New Module

↓

Canonical Architecture

↓

Specification

↓

Approval

↓

Implementation

↓

Testing

↓

Merge

Yangi modul birinchi repositoryda emas, Canonical Architecture hujjatlarida yaratiladi.

---

# Repository Status

Current Repository

↓

Target Repository (Canonical Architecture)

Repository doimo Target Repository tomon rivojlanadi.

---

# Governance

Worker/Director ish taqsimoti `Architecture_Audit_Plan.md`da rasmiylashtirilgan:

* **§11 — Worker Authority Registry (WAR-001 … WAR-007)** — Worker Director'siz nima qila oladi va nima Director Review talab qiladi.
* **§12 — Repository Structure (Director Order No. 003)** — repository root'ining canonical tarkibi, Freeze tarkibiga kirmaydigan fayllar, pre-freeze implementatsiya va loyiha infratuzilmasining maqomi.
* **§9b** — barcha Canonical Rule va ACR'lar (MIR-001, ICR-001, MVR-001, SMR-001, WDR-001, RAR-001 va boshqalar).

---
# Golden Principle

Architecture defines Repository.

Repository never defines Architecture.

---

End of Document
