# Decision Layer Sequence Diagram
Status: CANONICAL
---
# Runtime Sequence
```text
Signal Layer
↓
AI Layer
↓
DecisionService
↓
DecisionConfidence
↓
RuleEngine
↓
ApprovalEngine
↓
DecisionEngine
↓
DecisionLogger
↓
Decision Response
↓
Risk Layer
```
---
# Runtime Rules
1. DecisionService har doim birinchi ishlaydi.
2. DecisionConfidence RuleEngine'dan oldin ishlaydi.
3. ApprovalEngine Rule natijasiga asoslanadi.
4. DecisionEngine faqat Approval'dan keyin ishlaydi.
5. DecisionLogger har doim oxirida ishlaydi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Evaluating
↓
Validating
↓
Approving
↓
Creating Decision
↓
Logging
↓
Completed
```
---
# Summary
Decision Layer barcha Signal va AI natijalarini tekshirib, yagona Final Decision yaratadi.
