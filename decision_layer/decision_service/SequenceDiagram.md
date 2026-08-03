# Decision Service Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat DecisionService Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
AI Layer
↓
DecisionService (Entry)
↓
Validate Request
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
Standardize Response
↓
Risk Layer
```
---
# Runtime Rules
1. Request Validation bajarilishi shart.
2. DecisionService pipeline'ni DecisionConfidence'dan boshlaydi, DecisionEngine yoki RuleEngine'ni bevosita chaqirmaydi.
3. DecisionLogger'dan qaytgan natija DecisionService orqali Risk Layer'ga uzatiladi.
4. Standard Response yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Forwarding
↓
Waiting (Pipeline)
↓
Receiving Response
↓
Completed
```
---
# Summary
AI Layer
↓
DecisionService
↓
Decision Pipeline
↓
DecisionService
↓
Risk Layer
