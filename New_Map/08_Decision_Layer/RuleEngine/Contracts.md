# Rule Engine Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat RuleEngine modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
RuleEngine quyidagilar uchun javobgar.
✓ Trading Rule Validation
✓ Risk Rule Validation
✓ Safety Rule Validation
✓ Session Validation
✓ Rule Report Generation
✓ Failed Rule Reporting
RuleEngine bajarmaydi.
✗ Final Decision
✗ Trade Approval
✗ Signal Generation
✗ AI Analysis
✗ Trade Execution
✗ Database Logging
---
# Module Boundary
```text
DecisionConfidence
↓
RuleEngine
↓
ApprovalEngine
```
---
# Input Contract
• Signal Package
• AI Package
• Decision Confidence
• Market Context
• Risk Context
---
# Output Contract
• Rule Result
• Rule Report
• Failed Rules
• Rule Metadata
---
# Allowed Dependencies
✓ DecisionConfidence
✓ ApprovalEngine
---
# Forbidden Dependencies
✗ DecisionEngine
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
---
# Runtime Contract
1. Faol Rule Set yuklanishi shart.
2. Har bir Rule mustaqil tekshirilishi shart.
3. Failed Rule ro'yxati yaratilishi shart.
4. Rule Report ApprovalEngine'ga uzatilishi shart.
5. RuleEngine Final Decision yaratmaydi.
6. RuleEngine Trade Approval bermaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Rule Set yuklanadi.
✓ Trading Rules tekshiriladi.
✓ Risk Rules tekshiriladi.
✓ Session Rules tekshiriladi.
✓ Rule Report yaratiladi.
✓ ApprovalEngine'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
RuleEngine Contract GoldBot Decision Layer ichidagi barcha Trading, Risk, Session va Safety qoidalarini tekshirish, Rule Report yaratish va ApprovalEngine'ga uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
