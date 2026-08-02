# Decision Layer Data Flow
Status: CANONICAL
---
# Purpose
Ushbu hujjat GoldBot Decision Layer ichidagi umumiy ma'lumot oqimini (Data Flow) tavsiflaydi.
Decision Layer Signal Layer va AI Layer natijalarini qabul qilib, yagona Final Decision yaratadi.
---
# Layer Data Flow
```text
Signal Layer
        │
        ▼
AI Layer
        │
        ▼
DecisionService
        │
        ▼
DecisionConfidence
        │
        ▼
RuleEngine
        │
        ▼
ApprovalEngine
        │
        ▼
DecisionEngine
        │
        ▼
DecisionLogger
        │
        ▼
Decision Response
        │
        ▼
Risk Layer
```
---
# Input Sources
• Signal Package
• AI Package
• Market Context
• Technical Context
---
# Output
• Final Decision
• Decision Confidence
• Approval Status
• Decision Report
• Audit Record
---
# Golden Rules
1. AI qaror qabul qilmaydi.
2. Signal Trade ochmaydi.
3. Decision faqat DecisionEngine tomonidan yaratiladi.
4. Approval faqat ApprovalEngine tomonidan beriladi.
5. Har bir Decision log qilinishi shart.
