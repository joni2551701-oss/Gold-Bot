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
VoiceAI
↓
ExplanationAI
↓
ConfidenceAI
```
---
# Input Contract
• AI Context
• Vision Context
• Voice Context
• Market Context
---
# Output Contract
• Human Explanation
• Educational Response
• Step-by-Step Reasoning
• Explanation Metadata
---
# Allowed Dependencies
✓ AICoordinator
✓ VisionAI
✓ VoiceAI
✓ ConfidenceAI
---
# Forbidden Dependencies
✗ Decision Engine
✗ PersonalAI
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
✓ ConfidenceAI'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
ExplanationAI Contract GoldBot AI ichidagi AI Pipeline natijalarini (Vision, Voice, Market) tushunarli va izchil tarzda izohlab, ConfidenceAI'ga uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi. ExplanationAI Decision Engine'dan input olmaydi va foydalanuvchiga to'g'ridan-to'g'ri javob qaytarmaydi.
