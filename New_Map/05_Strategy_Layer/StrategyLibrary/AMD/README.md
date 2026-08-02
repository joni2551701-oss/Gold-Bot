# AMD Strategy
Status: CANONICAL
---
# Purpose
AMD (Accumulation • Manipulation • Distribution) Strategy GoldBot Strategy Library ichidagi Canonical Trading Strategy hisoblanadi.
Uning asosiy vazifasi AMD Market Cycle asosida Accumulation, Manipulation va Distribution fazalarini aniqlash hamda yuqori ehtimollikdagi trade imkoniyatlarini topishdir.
AMD Strategy signal yaratmaydi.
AMD Strategy trade ochmaydi.
AMD Strategy AI ishlatmaydi.
AMD Strategy faqat Strategy Analysis bajaradi.
---
# Objective
AMD Strategy quyidagi vazifalarni bajaradi.
• Accumulation Analysis
• Manipulation Analysis
• Distribution Analysis
• Liquidity Sweep Analysis
• Session Analysis
• Expansion Analysis
• AMD Confluence
• Strategy Result Generation
---
# Layer Position
```text
Market Context
↓
Indicator Context
↓
AMD Strategy
↓
StrategyManager
```
---
# Responsibilities
AMD Strategy:
✓ Accumulation aniqlaydi
✓ Manipulation aniqlaydi
✓ Distribution aniqlaydi
✓ Liquidity Sweep tekshiradi
✓ Session mosligini baholaydi
✓ Expansion baholaydi
✓ AMD Confluence yaratadi
✓ Strategy Result yaratadi
---
# Not Responsible
AMD Strategy:
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
AMD Strategy qabul qiladi.
• Market Context
• Indicator Context
• Strategy Profile
---
# Output
AMD Strategy yaratadi.
• AMD Strategy Result
• AMD Score
• AMD Confidence
• AMD Metadata
---
# Workflow
```text
Market Context
↓
Indicator Context
↓
Accumulation Analysis
↓
Manipulation Analysis
↓
Distribution Analysis
↓
AMD Confluence
↓
Strategy Validation
↓
Generate Strategy Result
↓
StrategyManager
```
---
# Golden Rules
1. AMD faqat Context va Indicator Context bilan ishlaydi.
2. AMD qoidalari deterministik bo'lishi kerak.
3. Strategy Result immutable hisoblanadi.
4. Signal yaratilmaydi.
5. AI ishlatilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
AMD/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
AMD GoldBot Strategy Library ichidagi Canonical Accumulation • Manipulation • Distribution Trading Strategy hisoblanadi.
