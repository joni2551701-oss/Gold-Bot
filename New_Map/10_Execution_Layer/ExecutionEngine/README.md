# Execution Engine
Status: CANONICAL
---
# Purpose
ExecutionEngine GoldBot Execution Layer ichidagi Canonical Trade Execution Controller moduli hisoblanadi.
Uning asosiy vazifasi Order Execution Pipeline'ni boshqarish, barcha Execution modullarini koordinatsiya qilish va yakuniy Execution jarayonini nazorat qilishdir.
ExecutionEngine Trading Decision qabul qilmaydi.
ExecutionEngine Risk hisoblamaydi.
ExecutionEngine faqat Execution Pipeline'ni boshqaradi.
---
# Objective
ExecutionEngine quyidagi vazifalarni bajaradi.
• Execution Pipeline Management
• Execution Context Management
• Order Execution Coordination
• Execution State Management
• Execution Result Generation
• Execution Report Generation
---
# Layer Position
```text
ExecutionService
↓
ExecutionEngine
↓
OrderValidator
```
---
# Responsibilities
ExecutionEngine
✓ Execution Request qabul qiladi
✓ Execution Context yaratadi
✓ Execution Pipeline boshqaradi
✓ Modullarni koordinatsiya qiladi
✓ Execution Result yaratadi
✓ Execution Report yaratadi
---
# Not Responsible
ExecutionEngine
✗ Trading Decision
✗ Risk Validation
✗ Order Routing
✗ Broker Communication
✗ Position Monitoring
✗ Portfolio Management
---
# Input
ExecutionEngine qabul qiladi.
• Validated Execution Request
• Position Package
• Order Request
• Execution Metadata
---
# Output
ExecutionEngine yaratadi.
• Execution Context
• Execution Result
• Execution Report
• Execution Metadata
---
# Workflow
```text
Receive Execution Request
↓
Validate Request
↓
Build Execution Context
↓
Start Execution Pipeline
↓
Collect Execution Results
↓
Generate Execution Report
↓
ExecutionMonitor
```
---
# Golden Rules
1. Faqat ExecutionService orqali kelgan Validated Execution Request qabul qilinadi.
2. Execution Pipeline ketma-ket ishlaydi.
3. Har bir modul natijasi tekshiriladi.
4. Execution Result standart formatda yaratiladi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
ExecutionEngine/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
ExecutionEngine GoldBot Execution Layer ichidagi barcha Execution jarayonlarini boshqaruvchi Canonical Controller modul hisoblanadi.
