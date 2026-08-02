# Decision Layer
Status: CANONICAL
---
# Purpose
Decision Layer GoldBot arxitekturasidagi yagona rasmiy qaror qabul qiluvchi qatlam hisoblanadi.
Uning asosiy vazifasi Signal Layer va AI Layer natijalarini baholash, barcha Trading Rule'larni tekshirish va yakuniy Trading Decision yaratishdir.
Decision Layer'dan tashqarida hech bir modul Trade Decision qabul qila olmaydi.
---
# Objective
Decision Layer quyidagi vazifalarni bajaradi.
• Signal Evaluation
• AI Evaluation
• Rule Validation
• Decision Confidence Calculation
• Trade Approval
• Decision Logging
---
# Layer Position
```text
Signal Layer
↓
AI Layer
↓
Decision Layer
↓
Risk Layer
```
---
# Internal Modules
```text
Decision Layer
├── DecisionEngine
├── ApprovalEngine
├── DecisionConfidence
├── RuleEngine
├── DecisionLogger
└── DecisionService
```
---
# Responsibilities
Decision Layer
✓ Signal baholaydi
✓ AI Context baholaydi
✓ Rule tekshiradi
✓ Decision Confidence hisoblaydi
✓ APPROVE / REJECT / HOLD qarorini chiqaradi
✓ Qarorni log qiladi
---
# Not Responsible
Decision Layer
✗ Market Data yig'ish
✗ Signal Generation
✗ Risk Calculation
✗ Lot Size Calculation
✗ Trade Execution
✗ Position Management
---
# Input
Decision Layer qabul qiladi.
• Signal Package
• AI Package
• Market Context
• Technical Context
---
# Output
Decision Layer yaratadi.
• Decision
• Decision Confidence
• Approval Status
• Decision Report
---
# Decision States
```text
APPROVE
Trade ruxsat berildi.
↓
REJECT
Trade rad etildi.
↓
HOLD
Qo'shimcha tasdiq kerak.
↓
WAIT
Bozor sharoiti mos emas.
```
---
# Workflow
```text
Receive Signal
↓
Receive AI Package
↓
Calculate Decision Confidence
↓
Validate Rules
↓
Approval Check
↓
Decision Engine
↓
Decision Logger
↓
Decision Service
↓
Risk Layer
```
---
# Golden Rules
1. AI hech qachon yakuniy qaror qabul qilmaydi.
2. Signal hech qachon Trade ochmaydi.
3. Qarorni faqat Decision Layer chiqaradi.
4. Har bir qaror log qilinishi shart.
5. RuleEngine barcha qoidalarni tekshirishi shart.
6. Decision Layer Risk Layer'dan oldin ishlaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
08_Decision_Layer/
├── README.md
├── DecisionEngine/
├── ApprovalEngine/
├── DecisionConfidence/
├── RuleEngine/
├── DecisionLogger/
├── DecisionService/
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
└── Layer_Contracts.md
```
---
# Summary
Decision Layer GoldBot arxitekturasidagi yagona Canonical Decision Authority hisoblanadi.
Signal va AI tavsiya beradi.
Decision Layer esa barcha ma'lumotlarni baholab yakuniy Trade Decision chiqaradi.
