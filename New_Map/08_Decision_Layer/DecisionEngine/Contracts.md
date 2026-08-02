# Decision Engine Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat DecisionEngine modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
DecisionEngine quyidagilar uchun javobgar.
✓ Decision Aggregation
✓ Final Decision
✓ Decision Status
✓ Decision Context
✓ Decision Metadata
✓ Final Decision Output
DecisionEngine bajarmaydi.
✗ Signal Generation
✗ AI Analysis
✗ Rule Validation
✗ Risk Calculation
✗ Trade Execution
✗ Decision Logging
---
# Module Boundary
```text
ApprovalEngine
↓
DecisionEngine
↓
DecisionLogger
```
---
# Input Contract
• Signal Package
• AI Package
• Approval Result
• Decision Confidence
• Rule Results
---
# Output Contract
• Final Decision
• Decision Status
• Decision Context
• Decision Metadata
---
# Allowed Dependencies
✓ ApprovalEngine
✓ DecisionConfidence
✓ RuleEngine
✓ DecisionLogger
---
# Forbidden Dependencies
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
✗ Platform Layer
---
# Runtime Contract
1. Approval Result mavjud bo'lishi shart.
2. Decision Confidence mavjud bo'lishi shart.
3. Rule Validation yakunlangan bo'lishi shart.
4. Final Decision faqat bir marta yaratiladi.
5. Decision o'zgartirilmaydi.
6. DecisionEngine Signal yoki AI yaratmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input tekshiriladi.
✓ Signal va AI natijalari birlashtiriladi.
✓ Final Decision yaratiladi.
✓ Decision Status belgilanadi.
✓ Decision Context yaratiladi.
✓ DecisionLogger'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
DecisionEngine Contract GoldBot arxitekturasidagi yagona yakuniy Trading Decision yaratish qoidalarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
