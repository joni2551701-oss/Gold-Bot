# Decision Confidence Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat DecisionConfidence modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
DecisionConfidence quyidagilar uchun javobgar.
✓ Technical Score Evaluation
✓ AI Confidence Integration
✓ Signal Quality Evaluation
✓ Context Evaluation
✓ Decision Confidence Calculation
✓ Confidence Report Generation
DecisionConfidence bajarmaydi.
✗ Final Decision
✗ Trade Approval
✗ Rule Validation
✗ Trade Execution
✗ Database Logging
✗ Risk Calculation
---
# Module Boundary
```text
AI Layer
↓
DecisionConfidence
↓
RuleEngine
```
---
# Input Contract
• Signal Package
• AI Package
• AI Confidence
• Technical Context
• Market Context
---
# Output Contract
• Decision Confidence Score
• Confidence Report
• Confidence Context
• Confidence Metadata
---
# Allowed Dependencies
✓ Signal Layer
✓ AI Layer
✓ RuleEngine
---
# Forbidden Dependencies
✗ ApprovalEngine
✗ DecisionEngine
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. AI Confidence hisobga olinishi shart.
2. Technical Score hisobga olinishi shart.
3. Signal Quality hisobga olinishi shart.
4. Context Quality hisobga olinishi shart.
5. Yakuniy Decision Confidence standart formula orqali hisoblanishi shart.
6. DecisionConfidence Final Decision yaratmaydi.
7. Confidence Report RuleEngine'ga uzatilishi shart.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Technical Score baholanadi.
✓ AI Confidence integratsiya qilinadi.
✓ Signal Quality baholanadi.
✓ Decision Confidence hisoblanadi.
✓ Confidence Report yaratiladi.
✓ RuleEngine'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
DecisionConfidence Contract GoldBot Decision Layer ichidagi barcha texnik va AI baholarini birlashtirib, yakuniy Decision Confidence Score yaratish qoidalarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
