# Decision Layer Sequence Diagram
Status: CANONICAL
---
# Runtime Sequence
```text
Signal Layer
↓
AI Layer
↓
DecisionService (Entry)
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
DecisionService (Exit)
↓
Decision Response
↓
Risk Layer
```
---
# Runtime Rules
1. DecisionService Decision Layer'ning yagona Entry va Exit nuqtasi hisoblanadi.
2. DecisionConfidence RuleEngine'dan oldin ishlaydi.
3. ApprovalEngine Rule natijasiga asoslanadi.
4. DecisionEngine faqat Approval'dan keyin ishlaydi.
5. DecisionLogger Layer tashqarisiga chiqmaydi — natija DecisionService orqali Risk Layer'ga uzatiladi.
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
