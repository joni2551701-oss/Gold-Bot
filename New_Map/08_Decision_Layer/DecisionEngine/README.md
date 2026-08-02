# Decision Engine
Status: CANONICAL
---
# Purpose
DecisionEngine GoldBot Decision Layer ichidagi Canonical Final Decision moduli hisoblanadi.
Uning asosiy vazifasi ApprovalEngine, DecisionConfidence va RuleEngine natijalarini birlashtirib yakuniy Trading Decision yaratishdir.
DecisionEngine GoldBot ichida Trade Decision chiqarishga ruxsat berilgan yagona modul hisoblanadi.
---
# Objective
DecisionEngine quyidagi vazifalarni bajaradi.
• Decision Aggregation
• Final Decision
• Decision Validation
• Decision Context Generation
• Decision Status
• Decision Result
---
# Layer Position
```text
ApprovalEngine
↓
DecisionEngine
↓
DecisionLogger
↓
DecisionService
```
---
# Responsibilities
DecisionEngine
✓ Approval Result qabul qiladi
✓ Decision Confidence qabul qiladi
✓ Rule natijalarini qabul qiladi
✓ Approval Status tekshiradi
✓ Yakuniy Decision yaratadi
✓ Decision Context yaratadi
---
# Not Responsible
DecisionEngine
✗ Signal Generation
✗ AI Analysis
✗ Rule Validation
✗ Risk Calculation
✗ Trade Execution
✗ Decision Logging
---
# Input
DecisionEngine qabul qiladi.
• Approval Result
• Decision Confidence
• Rule Results
---
# Output
DecisionEngine yaratadi.
• Final Decision
• Decision Context
• Decision Status
• Decision Metadata
---
# Decision States
• APPROVE
• REJECT
• HOLD
• WAIT
---
# Workflow
```text
Receive Packages
↓
Validate Inputs
↓
Aggregate Results
↓
Create Decision
↓
Generate Decision Context
↓
DecisionLogger
```
---
# Golden Rules
1. Final Decision faqat shu modulda yaratiladi.
2. Approval mavjud bo'lmasa Decision yaratilmaydi.
3. Decision o'zgartirilmaydi.
4. Decision standart formatda yaratiladi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
DecisionEngine/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
DecisionEngine GoldBot arxitekturasidagi yakuniy Trading Decision yaratuvchi yagona Canonical modul hisoblanadi.
