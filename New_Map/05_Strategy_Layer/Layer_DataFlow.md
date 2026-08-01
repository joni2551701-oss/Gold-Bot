# Strategy Layer Data Flow
Status: CANONICAL
---
# Purpose
Ushbu hujjat Strategy Layer ichidagi ma'lumot oqimini (Data Flow) tavsiflaydi.
Bu implementatsiya emas.
Bu GoldBot Strategy Layer uchun rasmiy Data Flow Blueprint hisoblanadi.
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
```
---
# Data Flow
```text
Market Context
        │
Indicator Context
        │
        ▼
Strategy Manager
        │
        ▼
Strategy Profile
        │
        ▼
Strategy Engine
        │
        ▼
Strategy Library
        │
        ▼
Selected Strategy
        │
        ▼
Strategy Result
        │
        ▼
Strategy Service
        │
        ▼
Signal Layer
```
---
# Input
• Market Context
• Indicator Context
• Strategy Profiles
• Strategy Configuration
---
# Output
• Strategy Result
• Strategy Score
• Strategy Confidence
• Strategy Metadata
---
# Golden Rules
1. Strategy Layer signal yaratmaydi.
2. Strategy Layer AI ishlatmaydi.
3. Strategy Layer Decision qabul qilmaydi.
4. Strategy Result immutable hisoblanadi.
5. Circular Dependency taqiqlanadi.
---
# Summary
Strategy Layer Context va Indicator natijalarini Strategy Result'ga aylantiruvchi Canonical Analysis Layer hisoblanadi.
