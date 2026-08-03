# Integrity Validator
Status: CANONICAL
---
# Purpose
IntegrityValidator — Data Validation Layer ichidagi Data Integrity Validation komponentidir.
Uning asosiy vazifasi Quality Validation'dan muvaffaqiyatli o'tgan Runtime Data'ning yaxlitligi (Integrity), izchilligi (Consistency) va ishonchliligini tekshirishdir.
IntegrityValidator Data sifatini baholamaydi.
IntegrityValidator Schema'ni tekshirmaydi.
U faqat Data Integrity'ni tekshiradi.
---
# Objective
IntegrityValidator quyidagi vazifalarni bajaradi:
• Data Integrity Validation
• Duplicate Detection
• Timestamp Validation
• Sequence Validation
• Consistency Validation
• Cross Reference Validation
• Integrity Result Generation
• Validation Event Generation
---
# Layer Position
```text
QualityValidator
↓
IntegrityValidator
↓
Validated Data
```
---
# Responsibilities
IntegrityValidator:
✓ Integrity Validation
✓ Duplicate Detection
✓ Timestamp Validation
✓ Sequence Validation
✓ Consistency Validation
✓ Cross Reference Validation
✓ Integrity Result Generation
---
# Not Responsible
IntegrityValidator:
✗ Schema Validation
✗ Data Quality Validation
✗ Business Validation
✗ Data Storage
✗ Strategy
✗ Decision
✗ AI Analysis
---
# Input
IntegrityValidator qabul qiladi:
• Quality Validated Data
• Integrity Rules
• Runtime Data
• Validation Request
---
# Output
IntegrityValidator yaratadi:
• Integrity Validation Result
• Integrity Status
• Integrity Report
• Validation Event
• Fully Validated Data
---
# Managed Objects
IntegrityValidator quyidagilar bilan ishlaydi:
• Runtime Data
• Integrity Rules
• Validation Metadata
• Duplicate Index
• Timestamp Metadata
• Sequence Metadata
---
# Workflow
```text
Receive Data
↓
Validate Duplicate
↓
Validate Timestamp
↓
Validate Sequence
↓
Validate Consistency
↓
Generate Result
↓
Validated Data
```
---
# Golden Rules
1. Faqat Quality Validation'dan o'tgan Data qabul qilinadi.
2. Duplicate Data rad etiladi.
3. Timestamp izchil bo'lishi kerak.
4. Sequence buzilmasligi kerak.
5. Validation Result doimo yaratiladi.
6. Data o'zgartirilmaydi.
7. Business Logic bajarilmaydi.
8. Circular Validation taqiqlanadi.
---
# Related Documents
```text
IntegrityValidator/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
IntegrityValidator Data Validation Layer ichidagi Canonical Data Integrity Validation komponentidir.
Uning vazifasi Runtime Data yaxlitligini tekshirish, Duplicate va Consistency muammolarini aniqlash hamda faqat to'liq valid ma'lumotlarni keyingi Layer'ga uzatishdan iborat.
