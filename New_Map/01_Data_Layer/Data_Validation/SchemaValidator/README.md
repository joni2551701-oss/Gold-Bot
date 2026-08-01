# Schema Validator
Status: CANONICAL
---
# Purpose
SchemaValidator — Data Validation Layer ichidagi Data Schema Validation komponentidir.
Uning asosiy vazifasi kiruvchi Runtime Data oldindan belgilangan Schema'ga mos kelishini tekshirishdir.
SchemaValidator Data mazmunini baholamaydi.
SchemaValidator Data sifatini baholamaydi.
U faqat Schema mosligini tekshiradi.
---
# Objective
SchemaValidator quyidagi vazifalarni bajaradi:
• Schema Validation
• Structure Validation
• Required Field Validation
• Optional Field Validation
• Data Type Validation
• Field Constraint Validation
• Schema Version Validation
• Validation Result Generation
---
# Layer Position
```text
DataValidator
↓
SchemaValidator
↓
QualityValidator
```
---
# Responsibilities
SchemaValidator:
✓ Schema Validation
✓ Structure Validation
✓ Required Fields
✓ Optional Fields
✓ Data Type Validation
✓ Schema Version Validation
✓ Validation Result
---
# Not Responsible
SchemaValidator:
✗ Business Validation
✗ Data Quality
✗ Data Integrity
✗ Data Storage
✗ Strategy
✗ Decision
✗ AI Analysis
---
# Input
SchemaValidator qabul qiladi:
• Validated Input Data
• Schema Definition
• Validation Request
• Schema Metadata
---
# Output
SchemaValidator yaratadi:
• Schema Validation Result
• Schema Validation Status
• Schema Validation Report
• Validated Schema Data
• Schema Events
---
# Managed Objects
SchemaValidator quyidagilar bilan ishlaydi:
• Schema
• Schema Version
• Required Fields
• Optional Fields
• Field Types
• Validation Metadata
---
# Workflow
```text
Receive Data
↓
Load Schema
↓
Validate Structure
↓
Validate Fields
↓
Validate Types
↓
Generate Result
↓
QualityValidator
```
---
# Golden Rules
1. Har bir Data Schema bo'yicha tekshiriladi.
2. Required Field majburiy.
3. Schema mos kelmasa Validation Failed.
4. Data mazmuni o'zgartirilmaydi.
5. Validation Result doimo yaratiladi.
6. Schema Version tekshiriladi.
7. Business Logic bajarilmaydi.
8. Circular Validation taqiqlanadi.
---
# Related Documents
```text
SchemaValidator/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
SchemaValidator Data Validation Layer ichidagi Canonical Schema Validation komponentidir.
Uning vazifasi Runtime Data'ning Schema, Structure va Data Type mosligini tekshirish hamda faqat Schema'dan o'tgan ma'lumotlarni QualityValidator moduliga uzatishdir.
