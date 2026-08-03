# ICT Strategy
Status: CANONICAL
---
# Purpose
ICT (Inner Circle Trader) GoldBot Strategy Library ichidagi Canonical Trading Strategy hisoblanadi.
Uning asosiy vazifasi Smart Money Concept va ICT metodologiyasi asosida yuqori ehtimollikdagi trade imkoniyatlarini aniqlash hamda Execution Output yaratishdir.
ICT Strategy signal yaratmaydi.
ICT Strategy trade ochmaydi.
ICT Strategy AI ishlatmaydi.
ICT Strategy faqat Strategy Analysis bajaradi.
---
# Objective
ICT Strategy quyidagi vazifalarni bajaradi.
• Market Structure Analysis
• Liquidity Analysis
• Order Block Analysis
• Fair Value Gap Analysis
• Premium / Discount Analysis
• Session Analysis
• Confluence Analysis
• Execution Output Generation
---
# Layer Position
```text
Market Context
↓
Indicator Context
↓
ICT Strategy
↓
StrategyEngine
```
---
# Responsibilities
ICT Strategy:
✓ ICT Rules qo'llaydi
✓ Liquidity baholaydi
✓ Order Block tekshiradi
✓ Fair Value Gap tekshiradi
✓ Premium / Discount baholaydi
✓ ICT Confluence yaratadi
✓ Execution Output yaratadi
---
# Not Responsible
ICT Strategy:
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
ICT Strategy qabul qiladi.
• Market Context
• Indicator Context
• Strategy Profile
---
# Output
ICT Strategy yaratadi.
• ICT Execution Output
• ICT Score
• ICT Confidence
• ICT Metadata
---
# Workflow
```text
Market Context
↓
Indicator Context
↓
ICT Analysis
↓
ICT Confluence
↓
Strategy Validation
↓
Generate Execution Output
↓
StrategyEngine
```
---
# Golden Rules
1. ICT faqat Context va Indicator Context bilan ishlaydi.
2. ICT qoidalari deterministik bo'lishi kerak.
3. Execution Output immutable hisoblanadi.
4. Signal yaratilmaydi.
5. AI ishlatilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
ICT/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
ICT GoldBot Strategy Library ichidagi Canonical ICT Trading Strategy hisoblanadi.
