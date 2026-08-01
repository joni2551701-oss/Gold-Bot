# Signal Layer Data Flow
Status: CANONICAL
---
# Purpose
Ushbu hujjat Signal Layer ichidagi ma'lumot oqimini (Data Flow) tavsiflaydi.
Bu implementatsiya emas.
Bu GoldBot Signal Layer uchun rasmiy Data Flow Blueprint hisoblanadi.
---
# Layer Position
```text
03_Context_Layer
↓
04_Indicator_Layer
↓
05_Strategy_Layer
↓
06_Signal_Layer
↓
07_AI_Layer
```
---
# Data Flow
```text
Market Context
        │
Indicator Context
        │
Strategy Result
        │
        ▼
Confluence Engine
        │
        ▼
Signal Builder
        │
        ▼
Signal Validator
        │
        ▼
Signal Scoring
        │
        ▼
Signal Formatter
        │
        ▼
Signal Service
        │
        ▼
AI Layer
```
---
# Input
• Market Context
• Indicator Context
• Strategy Result
• Strategy Metadata
---
# Output
• Signal Result
• Signal Direction
• Entry Price
• Stop Loss
• Take Profit
• Technical Score
• Technical Confidence
• Signal Metadata
---
# Golden Rules
1. Signal Layer faqat texnik signal yaratadi.
2. Signal Layer AI ishlatmaydi.
3. Signal Layer Decision qabul qilmaydi.
4. Signal Result immutable hisoblanadi.
5. Har bir Signal Validation'dan o'tishi shart.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Summary
Signal Layer Context, Indicator va Strategy natijalarini standart Technical Signal Result obyektiga aylantiruvchi Canonical Layer hisoblanadi.
