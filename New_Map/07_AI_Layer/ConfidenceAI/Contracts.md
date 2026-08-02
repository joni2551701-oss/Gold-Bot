# Confidence AI Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat ConfidenceAI modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
ConfidenceAI quyidagilar uchun javobgar.
✓ Confidence Evaluation
✓ Reliability Assessment
✓ Source Evaluation
✓ Context Consistency
✓ Uncertainty Detection
✓ Confidence Report Generation
ConfidenceAI bajarmaydi.
✗ Decision Making
✗ Signal Generation
✗ Market Analysis
✗ Learning
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
ExplanationAI
↓
ConfidenceAI
↓
AICoordinator
```
---
# Input Contract
• AI Context
• Knowledge Context
• Vision Context
• Fundamental Context
• Explanation Context
• Provider Metadata
---
# Output Contract
• Confidence Score
• Reliability Report
• Confidence Context
• Confidence Metadata
---
# Allowed Dependencies
✓ AICoordinator
✓ ExplanationAI
✓ KnowledgeAI
✓ FundamentalAI
---
# Forbidden Dependencies
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Strategy Layer
---
# Runtime Contract
1. Har bir AI Context baholanishi shart.
2. Source Reliability tekshirilishi shart.
3. Context Consistency tekshirilishi shart.
4. Confidence Score standart diapazonda hisoblanishi shart.
5. Uncertainty darajasi aniqlanishi shart.
6. ConfidenceAI hech qachon qaror qabul qilmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Context qabul qilinadi.
✓ Reliability baholanadi.
✓ Consistency tekshiriladi.
✓ Confidence Score hisoblanadi.
✓ Confidence Report yaratiladi.
✓ AICoordinator'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
ConfidenceAI Contract GoldBot AI ichidagi barcha AI natijalarining ishonchliligini baholash, Confidence Score yaratish va AICoordinator'ga standart Confidence Context uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi. AICoordinator o'z navbatida AIEngine va AIService (Exit) orqali Decision Layer'ga uzatadi.
