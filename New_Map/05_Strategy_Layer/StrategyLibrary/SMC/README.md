# SMC Strategy
Status: CANONICAL
---
# Purpose
SMC (Smart Money Concepts) GoldBot Strategy Library ichidagi Canonical Trading Strategy hisoblanadi.
Uning asosiy vazifasi Smart Money Concepts metodologiyasi asosida yuqori ehtimollikdagi trade imkoniyatlarini aniqlash hamda Strategy Result yaratishdir.
SMC Strategy signal yaratmaydi.
SMC Strategy trade ochmaydi.
SMC Strategy AI ishlatmaydi.
SMC Strategy faqat Strategy Analysis bajaradi.
---
# Objective
SMC Strategy quyidagi vazifalarni bajaradi.
• Market Structure Analysis
• BOS Analysis
• CHoCH Analysis
• Liquidity Analysis
• Order Block Analysis
• Fair Value Gap Analysis
• Imbalance Analysis
• Premium / Discount Analysis
• Confluence Analysis
• Strategy Result Generation
---
# Layer Position
```text
Market Context
↓
Indicator Context
↓
SMC Strategy
↓
StrategyEngine
```
---
# Responsibilities
SMC Strategy:
✓ Market Structure tekshiradi
✓ BOS tekshiradi
✓ CHoCH tekshiradi
✓ Liquidity baholaydi
✓ Order Block tekshiradi
✓ Fair Value Gap tekshiradi
✓ Imbalance baholaydi
✓ Premium / Discount baholaydi
✓ SMC Confluence yaratadi
✓ Strategy Result yaratadi
---
# Not Responsible
SMC Strategy:
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
SMC Strategy qabul qiladi.
• Market Context
• Indicator Context
• Strategy Profile
---
# Output
SMC Strategy yaratadi.
• SMC Strategy Result
• SMC Score
• SMC Confidence
• SMC Metadata
---
# Workflow
```text
Market Context
↓
Indicator Context
↓
SMC Analysis
↓
SMC Confluence
↓
Strategy Validation
↓
Generate Strategy Result
↓
StrategyEngine
```
---
# Golden Rules
1. SMC faqat Context va Indicator Context bilan ishlaydi.
2. SMC qoidalari deterministik bo'lishi kerak.
3. Strategy Result immutable hisoblanadi.
4. Signal yaratilmaydi.
5. AI ishlatilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
SMC/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
SMC GoldBot Strategy Library ichidagi Canonical Smart Money Concepts Trading Strategy hisoblanadi.
