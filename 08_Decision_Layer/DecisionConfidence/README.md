# Decision Confidence
Status: CANONICAL
---
# Purpose
DecisionConfidence GoldBot Decision Layer ichidagi Canonical Decision Confidence Assessment moduli hisoblanadi.
Uning asosiy vazifasi Signal Layer, AI Layer va boshqa Decision komponentlaridan olingan baholarni birlashtirib, yakuniy Decision Confidence Score hisoblashdir.
DecisionConfidence Trade Decision qabul qilmaydi.
DecisionConfidence Trade Approval bermaydi.
DecisionConfidence faqat Decision Quality Assessment bilan shug'ullanadi.
---
# Objective
DecisionConfidence quyidagi vazifalarni bajaradi.
• Technical Score Evaluation
• AI Confidence Integration
• Signal Quality Evaluation
• Context Quality Evaluation
• Decision Confidence Calculation
• Confidence Report Generation
---
# Layer Position
```text
Signal Layer
↓
AI Layer
↓
DecisionConfidence
↓
RuleEngine
↓
ApprovalEngine
```
---
# Responsibilities
DecisionConfidence
✓ Technical Score baholaydi
✓ AI Confidence qabul qiladi
✓ Signal Quality baholaydi
✓ Context sifatini baholaydi
✓ Yakuniy Decision Confidence hisoblaydi
✓ Confidence Report yaratadi
---
# Not Responsible
DecisionConfidence
✗ Final Decision
✗ Rule Validation
✗ Trade Approval
✗ Trade Execution
✗ Database Logging
✗ Risk Calculation
---
# Input
DecisionConfidence qabul qiladi.
• Signal Package
• AI Package
• AI Confidence
• Technical Context
• Market Context
---
# Output
DecisionConfidence yaratadi.
• Decision Confidence Score
• Confidence Report
• Confidence Metadata
• Confidence Context
---
# Workflow
```text
Receive Inputs
↓
Evaluate Technical Score
↓
Merge AI Confidence
↓
Evaluate Signal Quality
↓
Calculate Decision Confidence
↓
Generate Confidence Report
↓
RuleEngine
```
---
# Golden Rules
1. AI Confidence yakka holda ishlatilmaydi.
2. Technical Analysis ustuvor hisoblanadi.
3. Yakuniy Confidence bir nechta manbadan hisoblanadi.
4. DecisionConfidence Decision yaratmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
DecisionConfidence/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
DecisionConfidence GoldBot ichidagi yakuniy Decision Confidence Score hisoblovchi Canonical modul hisoblanadi.
