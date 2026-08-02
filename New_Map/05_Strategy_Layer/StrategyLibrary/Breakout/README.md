# Breakout Strategy
Status: CANONICAL
---
# Purpose
Breakout Strategy GoldBot Strategy Library ichidagi Canonical Trading Strategy hisoblanadi.
Uning asosiy vazifasi muhim Support, Resistance, Range va Consolidation hududlaridan yuz beradigan haqiqiy Breakout'larni aniqlash hamda yuqori ehtimollikdagi trade imkoniyatlarini topishdir.
Breakout Strategy signal yaratmaydi.
Breakout Strategy trade ochmaydi.
Breakout Strategy AI ishlatmaydi.
Breakout Strategy faqat Strategy Analysis bajaradi.
---
# Objective
Breakout Strategy quyidagi vazifalarni bajaradi.
• Range Analysis
• Consolidation Analysis
• Support Analysis
• Resistance Analysis
• Breakout Detection
• Breakout Confirmation
• Retest Analysis
• Volume Confirmation
• Breakout Confluence
• Strategy Result Generation
---
# Layer Position
```text
Market Context
↓
Indicator Context
↓
Breakout Strategy
↓
StrategyManager
```
---
# Responsibilities
Breakout Strategy:
✓ Range aniqlaydi
✓ Consolidation tekshiradi
✓ Support baholaydi
✓ Resistance baholaydi
✓ Breakout aniqlaydi
✓ Retest tekshiradi
✓ Volume Confirmation bajaradi
✓ Breakout Confluence yaratadi
✓ Strategy Result yaratadi
---
# Not Responsible
Breakout Strategy:
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
Breakout Strategy qabul qiladi.
• Market Context
• Indicator Context
• Strategy Profile
---
# Output
Breakout Strategy yaratadi.
• Breakout Strategy Result
• Breakout Score
• Breakout Confidence
• Breakout Metadata
---
# Workflow
```text
Market Context
↓
Indicator Context
↓
Range Analysis
↓
Breakout Detection
↓
Retest Analysis
↓
Confluence
↓
Strategy Validation
↓
Generate Strategy Result
↓
StrategyManager
```
---
# Golden Rules
1. Breakout faqat Context va Indicator Context bilan ishlaydi.
2. False Breakout imkon qadar filtrlanadi.
3. Strategy Result immutable hisoblanadi.
4. Signal yaratilmaydi.
5. AI ishlatilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Breakout/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Breakout GoldBot Strategy Library ichidagi Canonical Breakout Trading Strategy hisoblanadi.
