# Rule Engine
Status: CANONICAL
---
# Purpose
RuleEngine GoldBot Decision Layer ichidagi Canonical Trading Rule Validation moduli hisoblanadi.
Uning asosiy vazifasi barcha Trading Rule, Safety Rule va Business Rule'larni tekshirish hamda Trading Decision uchun Rule Validation natijasini yaratishdir.
RuleEngine Trade Decision qabul qilmaydi.
RuleEngine Signal yaratmaydi.
RuleEngine faqat Rule Validation bilan shug'ullanadi.
---
# Objective
RuleEngine quyidagi vazifalarni bajaradi.
• Trading Rule Validation
• Risk Rule Validation
• Safety Rule Validation
• Business Rule Validation
• Session Validation
• Rule Report Generation
---
# Layer Position
```text
DecisionConfidence
↓
RuleEngine
↓
ApprovalEngine
```
---
# Responsibilities
RuleEngine
✓ Trading Rule tekshiradi
✓ Risk Rule tekshiradi
✓ Session Rule tekshiradi
✓ Safety Rule tekshiradi
✓ Rule natijalarini yaratadi
✓ Rule Report yaratadi
---
# Not Responsible
RuleEngine
✗ Final Decision
✗ Trade Approval
✗ Signal Generation
✗ AI Analysis
✗ Trade Execution
✗ Database Logging
---
# Input
RuleEngine qabul qiladi.
• Decision Confidence
• Market Context
• Risk Context
---
# Output
RuleEngine yaratadi.
• Rule Result
• Rule Report
• Failed Rules
• Rule Metadata
---
# Rule Categories
• Trading Rules
• Risk Rules
• Safety Rules
• Business Rules
• Session Rules
---
# Workflow
```text
Receive Inputs
↓
Load Active Rules
↓
Validate Rules
↓
Collect Results
↓
Generate Rule Report
↓
ApprovalEngine
```
---
# Golden Rules
1. Har bir Rule mustaqil tekshiriladi.
2. Failed Rule log qilinadi.
3. Rule natijalari o'zgartirilmaydi.
4. RuleEngine Approval bermaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
RuleEngine/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
RuleEngine GoldBot ichidagi barcha Trading Rule va Safety Rule'larni tekshiruvchi Canonical Validation moduli hisoblanadi.
