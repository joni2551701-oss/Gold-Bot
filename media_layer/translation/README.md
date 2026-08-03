# Translation

Status: CANONICAL

---

# Purpose

Translation — Media Layer ichidagi Canonical tarjima moduli hisoblanadi.

Uning asosiy vazifasi GoldBot interfeysi va kontentini qo'llab-quvvatlanadigan tillar (UZ / RU / EN) o'rtasida tarjima qilishdir.

Translation hech qachon marketni tahlil qilmaydi va savdo qarorini hisoblamaydi.

---

# Objective

Translation quyidagi vazifalarni bajaradi.

• Language Registry (UZ / RU / EN)

• Translation Request Handling

• Translation Result Contract

• UI Catalog Translation

• Language Validation

• Multi Platform Language Support

---

# Layer Position

Content / UI Text

↓

Translation

↓

Platform Layer / Media Layer

---

# Responsibilities

Translation

✓ Qo'llab-quvvatlanadigan tillar ro'yxatini yuritadi

✓ Tarjima so'rovlarini qabul qiladi

✓ Tarjima natijasini standart Contract sifatida qaytaradi

✓ UI Catalog matnlarini tarjima qiladi

✓ Til kodlarini tekshiradi

---

# Not Responsible

Translation

✗ Market Analysis

✗ Signal Generation

✗ Trading Decision

✗ Risk Calculation

✗ AI Content Generation (AI_Content_Studio vazifasi)

---

# Input

Translation qabul qiladi.

• Translation Request

• Source Text

• Source Language

• Target Language

---

# Output

Translation yaratadi.

• Translation Result

• Translated Text

• Translation Status

• Translation Metadata

---

# Workflow

Content / UI Text

↓

Translation

↓

Platform Layer / Media Layer

---

# Internal Modules (Planned — implementatsiya bosqichida to'ldiriladi)

Translation

├── TranslationManager

├── LanguageRegistry

└── UICatalog

---

# Golden Rules

1. Faqat ro'yxatga olingan tillar qabul qilinadi (UZ / RU / EN).

2. Tarjima muvaffaqiyatsiz bo'lsa, natija ochiq-oydin rad etilgan holda qaytariladi.

3. Tarjima hech qachon to'qib chiqarilmaydi — noma'lum matn qaytarilmaydi.

4. Translation Business Logic bajarmaydi.

5. Circular Dependency qat'iyan taqiqlanadi.

---

# Related Documents

Translation/

├── README.md

├── Contracts.md

├── ModuleMap.md

└── SequenceDiagram.md

---

# Summary

Translation Media Layer ichidagi Canonical tarjima moduli hisoblanadi. U GoldBot interfeysi va kontentini UZ / RU / EN tillari o'rtasida tarjima qiladi — hech qachon market tahlili yoki savdo qarori bilan shug'ullanmaydi.
