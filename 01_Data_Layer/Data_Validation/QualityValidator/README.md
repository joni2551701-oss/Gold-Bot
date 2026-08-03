# Quality Validator
Status: CANONICAL
---
# Purpose
QualityValidator — Data Validation Layer ichidagi Data Quality Validation komponentidir.
Uning asosiy vazifasi Schema Validation'dan muvaffaqiyatli o'tgan Runtime Data sifatini baholash va faqat yuqori sifatli ma'lumotlarning keyingi Layer'ga uzatilishini ta'minlashdir.
QualityValidator Data strukturasini tekshirmaydi.
QualityValidator Data Integrity'ni tekshirmaydi.
U faqat Data sifatini baholaydi.
---
# Objective
QualityValidator quyidagi vazifalarni bajaradi:
• Data Quality Validation
• Completeness Validation
• Accuracy Validation
• Value Range Validation
• Freshness Validation
• Duplicate Quality Detection
• Quality Score Generation
• Validation Result Generation
---
# Layer Position
```text
SchemaValidator
↓
QualityValidator
↓
IntegrityValidator
```
---
# Responsibilities
QualityValidator:
✓ Data Quality Validation
✓ Completeness Validation
✓ Value Range Validation
✓ Freshness Validation
✓ Quality Score
✓ Validation Result
✓ Validation Events
---
# Not Responsible
QualityValidator:
✗ Schema Validation
✗ Integrity Validation
✗ Data Storage
✗ Business Logic
✗ Strategy
✗ Decision
✗ AI Analysis
---
# Input
QualityValidator qabul qiladi:
• Schema Validated Data
• Validation Rules
• Quality Rules
• Runtime Data
---
# Output
QualityValidator yaratadi:
• Quality Validation Result
• Quality Score
• Validation Status
• Validation Report
• Quality Events
---
# Managed Objects
QualityValidator quyidagilar bilan ishlaydi:
• Quality Rules
• Runtime Data
• Quality Score
• Validation Metadata
---
# Workflow
```text
Receive Data
↓
Validate Completeness
↓
Validate Value Range
↓
Validate Freshness
↓
Generate Quality Score
↓
IntegrityValidator
```
---
# Golden Rules
1. Faqat Schema Validated Data qabul qilinadi.
2. Data sifati baholanadi.
3. Past sifatli Data rad etiladi.
4. Quality Score yaratiladi.
5. Validation Result majburiy.
6. Data o'zgartirilmaydi.
7. Business Logic bajarilmaydi.
8. Circular Validation taqiqlanadi.
---
# Related Documents
```text
QualityValidator/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
QualityValidator Data Validation Layer ichidagi Canonical Data Quality Validation komponentidir.
Uning vazifasi Runtime Data sifatini baholash, Quality Score yaratish va faqat sifatli ma'lumotlarni IntegrityValidator moduliga uzatishdan iborat.
