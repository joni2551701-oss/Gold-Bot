# ValidationService
Status: CANONICAL
---
# Purpose
ValidationService — Data Validation Layer'ning markaziy Orchestrator komponentidir.
Uning asosiy vazifasi Data Validation Layer ichidagi barcha Validation modullarini yagona Runtime Pipeline ichida boshqarish va koordinatsiya qilishdir.
ValidationService Data'ni tekshirmaydi.
ValidationService Validation Rule'larni bajarmaydi.
U faqat Validation Workflow'ni boshqaradi.
---
# Objective
ValidationService quyidagi vazifalarni bajaradi:
• Validation Orchestration
• Validation Workflow Coordination
• Runtime Validation Management
• Validator Coordination
• Lifecycle Coordination
• Recovery Coordination
• Validation Health Monitoring
• Runtime State Management
---
# Layer Position
```text
Runtime Data
↓
ValidationService
├── DataValidator
├── SchemaValidator
├── QualityValidator
├── IntegrityValidator
└── ValidationLifecycle
↓
Validated Data
```
---
# Responsibilities
ValidationService:
✓ Validation Workflow boshqarish
✓ Validator Coordination
✓ Runtime Lifecycle boshqarish
✓ Validation Pipeline boshqarish
✓ Recovery Coordination
✓ Health Monitoring
✓ Runtime State boshqarish
---
# Not Responsible
ValidationService:
✗ Data Validation
✗ Schema Validation
✗ Quality Validation
✗ Integrity Validation
✗ Data Storage
✗ Business Logic
✗ Strategy
✗ Decision
✗ AI Analysis
---
# Input
ValidationService qabul qiladi:
• Validation Request
• Runtime Data
• Startup Request
• Shutdown Request
• Recovery Request
• Validator Events
---
# Output
ValidationService yaratadi:
• Validation Commands
• Runtime Events
• Lifecycle Events
• Recovery Commands
• Health Status
---
# Controlled Modules
ValidationService boshqaradi:
• DataValidator
• SchemaValidator
• QualityValidator
• IntegrityValidator
• ValidationLifecycle
---
# Workflow
```text
Runtime Data
↓
ValidationService
↓
DataValidator
↓
SchemaValidator
↓
QualityValidator
↓
IntegrityValidator
↓
ValidationLifecycle
↓
Validated Data
```
---
# Golden Rules
1. ValidationService Data Validation Layer'ning yagona Canonical Orchestrator'i hisoblanadi.
2. Barcha Validator'lar ValidationService koordinatsiyasi ostida ishlaydi.
3. Validation Pipeline qat'iy ketma-ketlikda bajariladi.
4. Recovery avtomatik ishga tushirilishi mumkin.
5. Health Monitoring doim ishlaydi.
6. ValidationService Validation bajarmaydi.
7. ValidationService Data'ni o'zgartirmaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
ValidationService/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
ValidationService Data Validation Layer ichidagi barcha Validation modullarini boshqaruvchi yagona Canonical Orchestrator hisoblanadi.
