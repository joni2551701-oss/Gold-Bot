# QualityValidator Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat QualityValidator modulining rasmiy Architecture Contract hujjati hisoblanadi.
QualityValidator Data Validation Layer ichidagi barcha Data Quality tekshiruvlarini bajaruvchi yagona Canonical Quality Validator hisoblanadi.
---
# Module Responsibility
QualityValidator quyidagilar uchun javobgar.
✓ Data Quality Validation
✓ Completeness Validation
✓ Value Range Validation
✓ Freshness Validation
✓ Quality Score Generation
✓ Validation Result Generation
✓ Validation Events
QualityValidator bajarmaydi.
✗ Schema Validation
✗ Integrity Validation
✗ Business Validation
✗ Data Storage
✗ AI Analysis
---
# Module Boundary
SchemaValidator
↓
QualityValidator
↓
IntegrityValidator
↓
Boundary End
---
# Input Contract
• Schema Validated Data
• Quality Rules
• Runtime Data
• Validation Request
---
# Output Contract
• Quality Validation Result
• Quality Score
• Validation Report
• Validation Event
• Validated Data
---
# Allowed Dependencies
✓ SchemaValidator
✓ IntegrityValidator
✓ Configuration Layer
✓ Event System
---
# Forbidden Dependencies
✗ Strategy Layer
✗ Decision Layer
✗ Risk Layer
✗ AI Layer
✗ Business Layer
---
# State Contract
• Initializing
• Ready
• Receiving
• Validating
• Scoring
• Passed
• Failed
---
# Runtime Contract
1. Har bir Schema Validated Data Quality Validation'dan o'tishi shart.
2. Quality Score majburiy yaratiladi.
3. Past sifatli Data keyingi Layer'ga uzatilmaydi.
4. Validation Result doimo yaratiladi.
5. Data o'zgartirilmaydi.
6. Circular Validation qat'iyan taqiqlanadi.
---
# Architecture Rules
QualityValidator:
✓ Data sifatini baholaydi.
✓ Quality Score hisoblaydi.
✓ Validation Result yaratadi.
✓ Validation Event yaratadi.
QualityValidator:
✗ Schema tekshirmaydi.
✗ Integrity tekshirmaydi.
✗ Business Logic bajarmaydi.
✗ Trading Logic bajarmaydi.
✗ AI ishlatmaydi.
---
# Acceptance Criteria
✓ Completeness Validation ishlaydi.
✓ Value Range Validation ishlaydi.
✓ Freshness Validation ishlaydi.
✓ Quality Score yaratiladi.
✓ Invalid Quality Data bloklanadi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
QualityValidator Contract Data Validation Layer ichidagi Canonical Data Quality Validation komponentining rasmiy arxitektura shartnomasi hisoblanadi.
QualityValidator Runtime Data sifatini baholovchi va faqat sifat talablariga javob beradigan ma'lumotlarni IntegrityValidator moduliga uzatuvchi yagona ruxsat etilgan modul hisoblanadi.
