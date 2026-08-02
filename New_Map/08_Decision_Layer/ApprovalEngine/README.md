# Approval Engine
Status: CANONICAL
---
# Purpose
ApprovalEngine GoldBot Decision Layer ichidagi Canonical Trade Approval moduli hisoblanadi.
Uning asosiy vazifasi DecisionConfidence va RuleEngine natijalarini tekshirib, Trading Decision'ga ruxsat berish yoki rad etishdir.
ApprovalEngine yakuniy Trade Decision yaratmaydi.
ApprovalEngine Signal yaratmaydi.
ApprovalEngine faqat Trade Approval bilan shug'ullanadi.
---
# Objective
ApprovalEngine quyidagi vazifalarni bajaradi.
• Trade Approval
• Rule Verification
• Decision Confidence Verification
• Approval Status Generation
• Reject Reason Generation
• Approval Context Generation
---
# Layer Position
```text
DecisionConfidence
↓
RuleEngine
↓
ApprovalEngine
↓
DecisionEngine
```
---
# Responsibilities
ApprovalEngine
✓ Rule natijalarini tekshiradi
✓ Decision Confidence tekshiradi
✓ Approval Status yaratadi
✓ Reject sababini yaratadi
✓ Approval Context yaratadi
✓ DecisionEngine'ga uzatadi
---
# Not Responsible
ApprovalEngine
✗ Final Decision
✗ Signal Generation
✗ AI Analysis
✗ Risk Calculation
✗ Trade Execution
✗ Database Logging
---
# Input
ApprovalEngine qabul qiladi.
• Rule Results
• Decision Confidence
• Signal Package
• AI Package
---
# Output
ApprovalEngine yaratadi.
• Approval Status
• Reject Reason
• Approval Context
• Approval Metadata
---
# Approval States
• APPROVED
• REJECTED
• HOLD
• WAIT
---
# Workflow
```text
Receive Inputs
↓
Validate Rules
↓
Validate Confidence
↓
Generate Approval
↓
Create Approval Context
↓
DecisionEngine
```
---
# Golden Rules
1. RuleEngine muvaffaqiyatli yakunlangan bo'lishi shart.
2. DecisionConfidence mavjud bo'lishi shart.
3. Har bir Reject uchun sabab yozilishi shart.
4. ApprovalEngine Final Decision yaratmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
ApprovalEngine/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
ApprovalEngine GoldBot ichidagi Trade Approval jarayonini boshqaruvchi Canonical modul hisoblanadi.
