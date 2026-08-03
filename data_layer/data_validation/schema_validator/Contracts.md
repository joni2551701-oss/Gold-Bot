# SchemaValidator Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat SchemaValidator modulining rasmiy Architecture Contract hujjati hisoblanadi.
SchemaValidator Data Validation Layer ichidagi barcha Schema tekshiruvlarini bajaruvchi yagona Canonical Schema Validator hisoblanadi.
---
# Module Responsibility
SchemaValidator quyidagilar uchun javobgar.
✓ Schema Validation
✓ Structure Validation
✓ Required Field Validation
✓ Optional Field Validation
✓ Data Type Validation
✓ Schema Version Validation
✓ Validation Result Generation
SchemaValidator bajarmaydi.
✗ Business Validation
✗ Data Quality Validation
✗ Data Integrity Validation
✗ Data Storage
✗ AI Analysis
---
# Module Boundary
DataValidator
↓
SchemaValidator
↓
QualityValidator
↓
Boundary End
---
# Input Contract
• Runtime Data
• Schema Definition
• Schema Metadata
• Validation Request
---
# Output Contract
• Schema Validation Result
• Schema Validation Status
• Validation Report
• Validated Data
• Validation Event
---
# Allowed Dependencies
✓ DataValidator
✓ QualityValidator
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
• Loading Schema
• Validating
• Passed
• Failed
---
# Runtime Contract
1. Har bir Data Schema bo'yicha tekshiriladi.
2. Required Field majburiy.
3. Schema Version mos bo'lishi kerak.
4. Invalid Schema keyingi Validator'ga uzatilmaydi.
5. Validation Result doimo yaratiladi.
6. Circular Validation qat'iyan taqiqlanadi.
---
# Architecture Rules
SchemaValidator:
✓ Schema tekshiradi.
✓ Structure tekshiradi.
✓ Required Field tekshiradi.
✓ Type tekshiradi.
✓ Validation Result yaratadi.
SchemaValidator:
✗ Data mazmunini baholamaydi.
✗ Quality tekshiruvini bajarmaydi.
✗ Integrity tekshiruvini bajarmaydi.
✗ Trading Logic bajarmaydi.
✗ AI ishlatmaydi.
---
# Acceptance Criteria
✓ Schema Validation ishlaydi.
✓ Structure Validation ishlaydi.
✓ Required Field Validation ishlaydi.
✓ Type Validation ishlaydi.
✓ Invalid Schema bloklanadi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
SchemaValidator Contract Data Validation Layer ichidagi Canonical Schema Validation komponentining rasmiy arxitektura shartnomasi hisoblanadi.
SchemaValidator Runtime Data'ning Schema, Structure va Data Type mosligini tekshiruvchi yagona ruxsat etilgan modul hisoblanadi.
