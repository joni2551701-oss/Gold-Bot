# Explanation AI Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat ExplanationAI modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
ExplanationAI quyidagilar uchun javobgar.
✓ Decision Explanation
✓ Signal Explanation
✓ Strategy Explanation
✓ Market Explanation
✓ Risk Explanation
✓ Educational Explanation
ExplanationAI bajarmaydi.
✗ Decision Making
✗ Signal Generation
✗ Market Analysis
✗ Learning
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
Decision Context
↓
ExplanationAI
↓
PersonalAI
↓
User
```
---
# Input Contract
• Decision Context
• Signal Context
• Market Context
• User Question
---
# Output Contract
• Human Explanation
• Educational Response
• Step-by-Step Reasoning
• Explanation Metadata
---
# Allowed Dependencies
✓ PersonalAI
✓ AICoordinator
---
# Forbidden Dependencies
✗ Decision Engine
✗ Signal Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. Explanation faktlarga asoslanishi shart.
2. Qaror o'zgartirilmasligi shart.
3. Tushuntirish foydalanuvchi darajasiga moslashtirilishi mumkin.
4. AI yangi Signal yaratmaydi.
5. AI yangi Decision yaratmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Context qabul qilinadi.
✓ Explanation yaratiladi.
✓ Reasoning shakllantiriladi.
✓ Educational javob tayyorlanadi.
✓ PersonalAI orqali foydalanuvchiga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
ExplanationAI Contract GoldBot AI ichidagi barcha qarorlar, signallar va bozor tahlillarini foydalanuvchiga tushunarli va izchil tarzda tushuntirishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
