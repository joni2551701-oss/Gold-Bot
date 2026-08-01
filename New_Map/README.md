# New_Map

Status: CANONICAL REPOSITORY BLUEPRINT

---

# Purpose

New_Map — GoldBot repository'ning yakuniy (Target Repository) strukturasidir.

Bu papka GoldBot loyihasining barcha kodlari, papkalari va modullarining qayerda joylashishi kerakligini belgilaydi.

New_Map implementatsiya emas.

New_Map — repository uchun yagona blueprint hisoblanadi.

---

# Objective

New_Map ning asosiy maqsadi:

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

New_Map repository uchun yagona canonical blueprint hisoblanadi.

Repository New_Map ga moslashtiriladi.

New_Map repositoryga moslashtirilmaydi.

Agar repository va New_Map o'rtasida farq aniqlansa:

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

Har bir .py fayl uchun New_Map ichida specification mavjud bo'lishi kerak.

Specification tugamasdan repository refactor qilinmaydi.

---

# Worker Workflow

Worker quyidagi tartibda ishlaydi.

1. New_Map ni o'qiydi.

2. Repository audit qiladi.

3. Farqlarni aniqlaydi.

4. Refactor rejasini tuzadi.

5. Repository'ni New_Map ga moslashtiradi.

6. Testlarni ishga tushiradi.

7. Freeze qiladi.

---

# Development Workflow

New Module

↓

New_Map

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

Yangi modul birinchi repositoryda emas, New_Map da yaratiladi.

---

# Repository Status

Current Repository

↓

Target Repository (New_Map)

Repository doimo Target Repository tomon rivojlanadi.

---

# Golden Principle

Architecture defines Repository.

Repository never defines Architecture.

---

End of Document
