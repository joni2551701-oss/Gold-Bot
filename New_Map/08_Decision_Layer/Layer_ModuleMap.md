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
AI Layer
        │
        ▼
DecisionService (Entry)
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
        │
        ▼
DecisionService (Exit)
        │
        ▼
Risk Layer
```
---
# Module Responsibilities
## DecisionService
Decision Layer'ning ikki tomonlama (bidirectional) Boundary Gateway'i — Entry va Exit.
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
