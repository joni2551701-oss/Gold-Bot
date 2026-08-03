# Smart Money Indicators
Status: CANONICAL
---
# Purpose
SmartMoneyIndicators Indicator Layer ichidagi Smart Money Concept (SMC) va Institutional Trading asosidagi indikatorlarni hisoblovchi Canonical modul hisoblanadi.
Uning asosiy vazifasi Context Layer tomonidan yaratilgan Institutional Context ma'lumotlarini sonli (numeric) indikatorlarga aylantirish va Strategy Layer uchun Smart Money Indicator State yaratishdir.
SmartMoneyIndicators Market Context yaratmaydi.
SmartMoneyIndicators signal yaratmaydi.
SmartMoneyIndicators trade ochmaydi.
SmartMoneyIndicators AI ishlatmaydi.
SmartMoneyIndicators faqat Smart Money Indicator'larni hisoblaydi.
---
# Objective
SmartMoneyIndicators quyidagi vazifalarni bajaradi:
• Liquidity Score Calculation
• Order Block Strength Calculation
• Fair Value Gap Score Calculation
• Imbalance Score Calculation
• Premium / Discount Score Calculation
• AMD Score Calculation
• Wyckoff Score Calculation
• Institutional Activity Score Calculation
• Smart Money Indicator State Generation
---
# Layer Position
```text
Market Context
↓
IndicatorEngine
↓
SmartMoneyIndicators
↓
IndicatorService
```
---
# Responsibilities
SmartMoneyIndicators:
✓ Liquidity Score hisoblaydi
✓ Order Block Strength hisoblaydi
✓ Fair Value Gap Score hisoblaydi
✓ Imbalance Score hisoblaydi
✓ Premium / Discount Score hisoblaydi
✓ AMD Score hisoblaydi
✓ Wyckoff Score hisoblaydi
✓ Institutional Activity Score hisoblaydi
✓ Smart Money Indicator State yaratadi
---
# Not Responsible
SmartMoneyIndicators:
✗ Market Context Analysis
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
SmartMoneyIndicators qabul qiladi:
• Market Context
• Liquidity State
• Order Block State
• Fair Value Gap State
• Wyckoff State
• AMD State
• Trend State
---
# Output
SmartMoneyIndicators yaratadi:
• Liquidity Score
• Order Block Strength
• Fair Value Gap Score
• Imbalance Score
• Premium / Discount Score
• AMD Score
• Wyckoff Score
• Institutional Activity Score
• Smart Money Indicator State
---
# Workflow
```text
Market Context
↓
Load Smart Money Context
↓
Calculate Smart Money Indicators
↓
Validate Indicators
↓
Generate Smart Money Indicator State
↓
IndicatorService
```
---
# Golden Rules
1. Smart Money Indicator'lar faqat Market Context asosida hisoblanadi.
2. Context qayta hisoblanmaydi.
3. Natijalar immutable hisoblanadi.
4. Signal yaratilmaydi.
5. AI ishlatilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
SmartMoneyIndicators/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
SmartMoneyIndicators GoldBot Indicator Layer ichidagi Institutional va Smart Money Indicator'larni hisoblaydigan Canonical modul hisoblanadi.
