# Approval Engine Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat ApprovalEngine modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
ApprovalEngine quyidagilar uchun javobgar.
✓ Rule Verification
✓ Decision Confidence Verification
✓ Trade Approval
✓ Approval Status
✓ Reject Reason
✓ Approval Context
ApprovalEngine bajarmaydi.
✗ Final Decision
✗ Signal Generation
✗ AI Analysis
✗ Risk Calculation
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
↓
DecisionEngine
```
---
# Input Contract
• Rule Results
• Decision Confidence
• Signal Package
• AI Package
---
# Output Contract
• Approval Status
• Reject Reason
• Approval Context
• Approval Metadata
---
# Allowed Dependencies
✓ RuleEngine
✓ DecisionConfidence
✓ DecisionEngine
---
# Forbidden Dependencies
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
✗ Platform Layer
---
# Runtime Contract
1. RuleEngine natijalari tekshirilishi shart.
2. Decision Confidence tekshirilishi shart.
3. Approval Status yaratilishi shart.
4. REJECT holatida Reject Reason majburiy.
5. ApprovalEngine Final Decision yaratmaydi.
6. Approval natijasi DecisionEngine'ga uzatilishi shart.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Rule natijalari tekshiriladi.
✓ Decision Confidence tekshiriladi.
✓ Approval Status yaratiladi.
✓ Reject Reason yaratiladi.
✓ Approval Context yaratiladi.
✓ DecisionEngine'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
ApprovalEngine Contract GoldBot Decision Layer ichidagi Trade Approval jarayonini boshqarish, Rule va Confidence natijalarini tekshirish hamda DecisionEngine uchun Approval Result yaratishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
