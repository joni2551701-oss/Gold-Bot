# Liquidity Sweep Strategy
Status: CANONICAL
---
# Purpose
Liquidity Sweep Strategy GoldBot Strategy Library ichidagi Canonical Trading Strategy hisoblanadi.
Uning asosiy vazifasi bozordagi Liquidity Sweep hodisalarini aniqlash, False Breakout va Stop Hunt holatlarini baholash hamda yuqori ehtimollikdagi trade imkoniyatlarini topishdir.
Liquidity Sweep Strategy signal yaratmaydi.
Liquidity Sweep Strategy trade ochmaydi.
Liquidity Sweep Strategy AI ishlatmaydi.
Liquidity Sweep Strategy faqat Strategy Analysis bajaradi.
---
# Objective
Liquidity Sweep Strategy quyidagi vazifalarni bajaradi.
• Liquidity Pool Analysis
• Equal High / Equal Low Analysis
• Stop Hunt Detection
• False Breakout Detection
• Sweep Confirmation
• Rejection Analysis
• Confluence Analysis
• Strategy Result Generation
---
# Layer Position
```text
Market Context
↓
Indicator Context
↓
Liquidity Sweep Strategy
↓
StrategyEngine
```
---
# Responsibilities
Liquidity Sweep Strategy:
✓ Liquidity Pool aniqlaydi
✓ Equal High baholaydi
✓ Equal Low baholaydi
✓ Stop Hunt aniqlaydi
✓ False Breakout tekshiradi
✓ Sweep Confirmation bajaradi
✓ Rejection baholaydi
✓ Liquidity Confluence yaratadi
✓ Strategy Result yaratadi
---
# Not Responsible
Liquidity Sweep Strategy:
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
Liquidity Sweep Strategy qabul qiladi.
• Market Context
• Indicator Context
• Strategy Profile
---
# Output
Liquidity Sweep Strategy yaratadi.
• Liquidity Sweep Result
• Liquidity Score
• Liquidity Confidence
• Liquidity Metadata
---
# Workflow
```text
Market Context
↓
Indicator Context
↓
Liquidity Analysis
↓
Sweep Detection
↓
Confluence
↓
Strategy Validation
↓
Generate Strategy Result
↓
StrategyEngine
```
---
# Golden Rules
1. Strategy faqat Context va Indicator Context bilan ishlaydi.
2. Liquidity qoidalari deterministik bo'lishi kerak.
3. Strategy Result immutable hisoblanadi.
4. Signal yaratilmaydi.
5. AI ishlatilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
LiquiditySweep/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Liquidity Sweep GoldBot Strategy Library ichidagi Canonical Liquidity Sweep Trading Strategy hisoblanadi.
