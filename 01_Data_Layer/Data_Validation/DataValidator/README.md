# Data Validator
Status: CANONICAL
---
# Purpose
DataValidator — Data Validation Layer ichidagi asosiy Validation komponentidir.
Uning asosiy vazifasi GoldBot Runtime davomida barcha kiruvchi Market Data obyektlarini tekshirish va faqat valid ma'lumotlarning keyingi Layer'larga uzatilishini ta'minlashdir.
DataValidator Business Logic bajarmaydi.
DataValidator Data'ni o'zgartirmaydi.
U faqat Data'ni tekshiradi.
---
# Objective
DataValidator quyidagi vazifalarni bajaradi:
• Runtime Data Validation
• Input Validation
• Output Validation
• Required Field Validation
• Data Type Validation
• Validation Result Generation
• Validation Event Generation
• Runtime Validation Monitoring
---
# Layer Position
```text
Data Source
↓
DataValidator
↓
SchemaValidator
↓
QualityValidator
↓
IntegrityValidator
↓
Validated Data
```
---
# Responsibilities
DataValidator:
✓ Runtime Data Validation
✓ Input Validation
✓ Required Field Validation
✓ Data Type Validation
✓ Validation Result Generation
✓ Validation Event Generation
✓ Validation Status Reporting
---
# Not Responsible
DataValidator:
✗ Data Storage
✗ Data Transformation
✗ Business Rules
✗ Strategy
✗ Decision
✗ AI Analysis
✗ Market Analysis
---
# Input
DataValidator qabul qiladi:
• Market Data
• Runtime Data
• Candle Data
• Price Data
• Validation Request
---
# Output
DataValidator yaratadi:
• Validation Result
• Validation Status
• Validation Event
• Validation Report
• Validated Data
---
# Managed Objects
DataValidator quyidagilar bilan ishlaydi:
• Runtime Data
• Validation Rules
• Validation Metadata
• Validation Status
---
# Workflow
```text
Receive Data
↓
Validate Required Fields
↓
Validate Data Types
↓
Generate Validation Result
↓
SchemaValidator
```
---
# Golden Rules
1. Har bir Data obyekti validatsiyadan o'tishi shart.
2. Invalid Data keyingi Layer'ga uzatilmaydi.
3. Validation Data'ni o'zgartirmaydi.
4. Validation natijasi doimo qaytariladi.
5. Validation Event yaratiladi.
6. Business Logic bajarilmaydi.
7. Runtime Validation doimiy ishlaydi.
8. Circular Validation taqiqlanadi.
---
# Related Documents
```text
DataValidator/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
DataValidator Data Validation Layer ichidagi yagona Canonical Primary Validator hisoblanadi.
Uning vazifasi:
• Runtime Data'ni tekshirish;
• Invalid Data'ni bloklash;
• Validation Result yaratish;
• Keyingi Validator'lar uchun valid ma'lumot tayyorlash.
