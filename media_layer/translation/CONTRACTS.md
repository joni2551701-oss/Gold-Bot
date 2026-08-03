# Translation Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat Translation modulining rasmiy Architecture Contract hujjati hisoblanadi.

---

# Module Responsibility

Translation quyidagilar uchun javobgar.

✓ Qo'llab-quvvatlanadigan tillar ro'yxatini yuritadi

✓ Tarjima so'rovlarini qabul qiladi

✓ Tarjima natijasini standart Contract sifatida qaytaradi

✓ UI Catalog matnlarini tarjima qiladi

✓ Til kodlarini tekshiradi

Translation bajarmaydi.

✗ Market Analysis

✗ Signal Generation

✗ Trading Decision

✗ Risk Calculation

✗ AI Content Generation (AI_Content_Studio vazifasi)

---

# Module Boundary

Content / UI Text

↓

Translation

↓

Platform Layer / Media Layer

---

# Input Contract

• Translation Request

• Source Text

• Source Language

• Target Language

---

# Output Contract

• Translation Result

• Translated Text

• Translation Status

• Translation Metadata

---

# Allowed Dependencies

✓ AI_Content_Studio

✓ Content_Manager

---

# Forbidden Dependencies

✗ Signal Layer

✗ Decision Layer

✗ Risk Layer

✗ Execution Layer

✗ Database Layer

---

# Runtime Contract

1. Faqat ro'yxatga olingan tillar qabul qilinadi (UZ / RU / EN).

2. Tarjima muvaffaqiyatsiz bo'lsa, natija ochiq-oydin rad etilgan holda qaytariladi.

3. Tarjima hech qachon to'qib chiqarilmaydi — noma'lum matn qaytarilmaydi.

4. Translation Business Logic bajarmaydi.

5. Circular Dependency qat'iyan taqiqlanadi.

---

# Acceptance Criteria

✓ Translation Request qabul qilinadi.

✓ Til tekshiriladi.

✓ Translation Result yaratiladi.

✓ Architecture Boundary buzilmaydi.

---

# Summary

Translation Contract Translation Media Layer ichidagi Canonical tarjima moduli hisoblanadi. U GoldBot interfeysi va kontentini UZ / RU / EN tillari o'rtasida tarjima qiladi — hech qachon market tahlili yoki savdo qarori bilan shug'ullanmaydi.
