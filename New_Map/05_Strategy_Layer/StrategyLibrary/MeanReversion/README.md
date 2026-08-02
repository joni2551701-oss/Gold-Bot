# Mean Reversion Strategy
Status: CANONICAL
---
# Purpose
Mean Reversion Strategy GoldBot Strategy Library ichidagi Canonical Trading Strategy hisoblanadi.
Uning asosiy vazifasi narxning o'zining muvozanat (Mean Value) atrofida harakatlanish xususiyatidan foydalanib, ekstremal og'ishlardan keyingi qaytish ehtimolini aniqlash hamda Execution Output yaratishdir.
Mean Reversion Strategy signal yaratmaydi.
Mean Reversion Strategy trade ochmaydi.
Mean Reversion Strategy AI ishlatmaydi.
Mean Reversion Strategy faqat Strategy Analysis bajaradi.
---
# Objective
Mean Reversion Strategy quyidagi vazifalarni bajaradi.
• Mean Value Analysis
• Deviation Analysis
• Overbought Analysis
• Oversold Analysis
• Reversal Confirmation
• Momentum Confirmation
• Volume Confirmation
• Mean Reversion Confluence
• Execution Output Generation
---
# Layer Position
```text
Market Context
↓
Indicator Context
↓
Mean Reversion Strategy
↓
StrategyEngine
```
---
# Responsibilities
Mean Reversion Strategy:
✓ Mean Value aniqlaydi
✓ Price Deviation baholaydi
✓ Overbought holatini tekshiradi
✓ Oversold holatini tekshiradi
✓ Reversal tasdiqlaydi
✓ Momentum baholaydi
✓ Volume tasdiqlaydi
✓ Mean Reversion Confluence yaratadi
✓ Execution Output yaratadi
---
# Not Responsible
Mean Reversion Strategy:
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
Mean Reversion Strategy qabul qiladi.
• Market Context
• Indicator Context
• Strategy Profile
---
# Output
Mean Reversion Strategy yaratadi.
• Mean Reversion Result
• Mean Reversion Score
• Mean Reversion Confidence
• Mean Reversion Metadata
---
# Workflow
```text
Market Context
↓
Indicator Context
↓
Mean Value Analysis
↓
Deviation Analysis
↓
Reversal Confirmation
↓
Confluence
↓
Strategy Validation
↓
Generate Execution Output
↓
StrategyEngine
```
---
# Golden Rules
1. Mean Reversion faqat Range yoki muvozanatli bozorlarda qo'llaniladi.
2. Kuchli trendda qo'llashdan oldin qo'shimcha tasdiqlash talab qilinadi.
3. Execution Output immutable hisoblanadi.
4. Signal yaratilmaydi.
5. AI ishlatilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
MeanReversion/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Mean Reversion GoldBot Strategy Library ichidagi Canonical Mean Reversion Trading Strategy hisoblanadi.
