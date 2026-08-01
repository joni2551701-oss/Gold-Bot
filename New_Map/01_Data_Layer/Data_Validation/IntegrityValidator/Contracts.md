# IntegrityValidator Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat IntegrityValidator modulining rasmiy Architecture Contract hujjati hisoblanadi.
IntegrityValidator Data Validation Layer ichidagi barcha Integrity tekshiruvlarini bajaruvchi yagona Canonical Integrity Validator hisoblanadi.
---
# Module Responsibility
IntegrityValidator quyidagilar uchun javobgar.
✓ Duplicate Detection
✓ Timestamp Validation
✓ Sequence Validation
✓ Consistency Validation
✓ Cross Reference Validation
✓ Integrity Result Generation
✓ Validation Event Generation
IntegrityValidator bajarmaydi.
✗ Schema Validation
✗ Data Quality Validation
✗ Business Validation
✗ Data Storage
✗ AI Analysis
---
# Module Boundary
QualityValidator
↓
IntegrityValidator
↓
Validated Data
↓
Boundary End
---
# Input Contract
• Quality Validated Data
• Integrity Rules
• Runtime Data
• Validation Request
---
# Output Contract
• Integrity Validation Result
• Integrity Status
• Integrity Report
• Validation Event
• Fully Validated Data
---
# Allowed Dependencies
✓ QualityValidator
✓ ValidationService
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
• Passed
• Failed
---
# Runtime Contract
1. Har bir Quality Validated Data Integrity Validation'dan o'tishi shart.
2. Duplicate Data rad etiladi.
3. Timestamp va Sequence izchil bo'lishi kerak.
4. Validation Result doimo yaratiladi.
5. Data o'zgartirilmaydi.
6. Circular Validation qat'iyan taqiqlanadi.
---
# Architecture Rules
IntegrityValidator:
✓ Duplicate tekshiradi.
✓ Timestamp tekshiradi.
✓ Sequence tekshiradi.
✓ Consistency tekshiradi.
✓ Validation Result yaratadi.
IntegrityValidator:
✗ Schema tekshirmaydi.
✗ Quality tekshirmaydi.
✗ Business Logic bajarmaydi.
✗ Trading Logic bajarmaydi.
✗ AI ishlatmaydi.
---
# Acceptance Criteria
✓ Duplicate Detection ishlaydi.
✓ Timestamp Validation ishlaydi.
✓ Sequence Validation ishlaydi.
✓ Consistency Validation ishlaydi.
✓ Invalid Data bloklanadi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
IntegrityValidator Contract Data Validation Layer ichidagi Canonical Data Integrity Validation komponentining rasmiy arxitektura shartnomasi hisoblanadi.
IntegrityValidator Runtime Data yaxlitligini tekshiruvchi va faqat to'liq Integrity Validation'dan o'tgan ma'lumotlarni GoldBot'ning keyingi qatlamlariga uzatuvchi yagona ruxsat etilgan modul hisoblanadi.
