# Decision Layer Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Decision Layer uchun rasmiy Architecture Contract hisoblanadi.
---
# Layer Responsibility
Decision Layer quyidagilar uchun javobgar.
✓ Decision Confidence
✓ Rule Validation
✓ Trade Approval
✓ Final Decision
✓ Decision Logging
✓ Decision Response
---
# Layer Does NOT
✗ Signal Generation
✗ AI Analysis
✗ Market Data Collection
✗ Risk Calculation
✗ Trade Execution
✗ Position Management
---
# Input Contract
Decision Layer qabul qiladi.
• Signal Package
• AI Package
• Technical Context
• Market Context
---
# Output Contract
Decision Layer yaratadi.
• Final Decision
• Approval Status
• Decision Confidence
• Decision Report
• Audit Record
---
# Layer Pipeline
```text
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
Risk Layer
```
---
# Layer Rules
1. Yakuniy qarorni faqat DecisionEngine yaratadi.
2. AI hech qachon Final Decision qabul qilmaydi.
3. Signal Layer Trade ochmaydi.
4. RuleEngine barcha Trading Rule'larni tekshirishi shart.
5. ApprovalEngine Decision'ga ruxsat beradi yoki rad etadi.
6. Har bir Decision log qilinishi shart.
7. Risk Layer faqat APPROVED Decision qabul qiladi.
8. Decision Layer barcha tashqi aloqalarni faqat DecisionService orqali amalga oshiradi.
9. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Signal Package qabul qilinadi.
✓ AI Package qabul qilinadi.
✓ Decision Confidence hisoblanadi.
✓ Rule Validation bajariladi.
✓ Approval yaratiladi.
✓ Final Decision yaratiladi.
✓ Decision log qilinadi.
✓ Risk Layer'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Decision Layer Contract GoldBot arxitekturasidagi yagona Decision Authority sifatida ishlashini, barcha Signal va AI natijalarini baholashini, Trading Rule'larni tekshirishini, yakuniy Decision yaratishini va uni Risk Layer'ga uzatishini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
