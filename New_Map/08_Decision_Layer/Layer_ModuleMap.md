# Decision Layer Module Map
Status: CANONICAL
---
# Layer Architecture
```text
08_Decision_Layer
│
├── DecisionService
│
├── DecisionConfidence
│
├── RuleEngine
│
├── ApprovalEngine
│
├── DecisionEngine
│
└── DecisionLogger
```
---
# Processing Pipeline
```text
DecisionService
        │
        ▼
DecisionConfidence
        │
        ▼
RuleEngine
        │
        ▼
ApprovalEngine
        │
        ▼
DecisionEngine
        │
        ▼
DecisionLogger
```
---
# Module Responsibilities
## DecisionService
Decision Layer Gateway.
---
## DecisionConfidence
Decision Confidence Score hisoblaydi.
---
## RuleEngine
Trading Rule va Safety Rule tekshiradi.
---
## ApprovalEngine
Trade Approval yaratadi.
---
## DecisionEngine
Final Decision yaratadi.
---
## DecisionLogger
Audit va Decision History yaratadi.
---
# Summary
Decision Layer GoldBot arxitekturasidagi yagona Canonical Decision Authority hisoblanadi.
