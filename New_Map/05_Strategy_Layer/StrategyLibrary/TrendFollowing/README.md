# Trend Following Strategy
Status: CANONICAL
---
# Purpose
Trend Following Strategy GoldBot Strategy Library ichidagi Canonical Trading Strategy hisoblanadi.
Uning asosiy vazifasi mavjud bozor trendini aniqlash, trend yo'nalishi bo'yicha yuqori ehtimollikdagi trade imkoniyatlarini topish va Strategy Result yaratishdir.
Trend Following Strategy signal yaratmaydi.
Trend Following Strategy trade ochmaydi.
Trend Following Strategy AI ishlatmaydi.
Trend Following Strategy faqat Strategy Analysis bajaradi.
---
# Objective
Trend Following Strategy quyidagi vazifalarni bajaradi.
• Trend Direction Analysis
• Trend Strength Analysis
• Pullback Analysis
• Continuation Analysis
• Momentum Confirmation
• Volume Confirmation
• Trend Confluence
• Strategy Result Generation
---
# Layer Position
```text
Market Context
↓
Indicator Context
↓
Trend Following Strategy
↓
StrategyEngine
```
---
# Responsibilities
Trend Following Strategy:
✓ Trend yo'nalishini aniqlaydi
✓ Trend kuchini baholaydi
✓ Pullback aniqlaydi
✓ Continuation tekshiradi
✓ Momentum tasdiqlaydi
✓ Volume tasdiqlaydi
✓ Trend Confluence yaratadi
✓ Strategy Result yaratadi
---
# Not Responsible
Trend Following Strategy:
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
Trend Following Strategy qabul qiladi.
• Market Context
• Indicator Context
• Strategy Profile
---
# Output
Trend Following Strategy yaratadi.
• Trend Following Result
• Trend Score
• Trend Confidence
• Trend Metadata
---
# Workflow
```text
Market Context
↓
Indicator Context
↓
Trend Analysis
↓
Pullback Detection
↓
Continuation Analysis
↓
Trend Confluence
↓
Strategy Validation
↓
Generate Strategy Result
↓
StrategyEngine
```
---
# Golden Rules
1. Trend yo'nalishiga qarshi trade qilinmaydi.
2. Pullback tasdiqlanishi kerak.
3. Strategy Result immutable hisoblanadi.
4. Signal yaratilmaydi.
5. AI ishlatilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
TrendFollowing/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Trend Following GoldBot Strategy Library ichidagi Canonical Trend Following Trading Strategy hisoblanadi.
