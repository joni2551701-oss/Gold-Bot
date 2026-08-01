# Strategy Layer
Status: CANONICAL
---
# Purpose
Strategy Layer GoldBot Trading Engine ichidagi barcha savdo strategiyalarini boshqaruvchi Canonical Layer hisoblanadi.
Uning asosiy vazifasi Context Layer va Indicator Layer tomonidan yaratilgan ma'lumotlardan foydalanib strategik tahlilni bajarish hamda Strategy Result yaratishdir.
Strategy Layer signal yaratmaydi.
Strategy Layer trade ochmaydi.
Strategy Layer AI qaror qabul qilmaydi.
Strategy Layer faqat Strategy Analysis bajaradi.
---
# Objective
Strategy Layer quyidagi vazifalarni bajaradi.
• Strategy Execution
• Strategy Selection
• Strategy Validation
• Strategy Confluence
• Strategy Profile Management
• Strategy Result Generation
---
# Layer Position
```text
Context Layer
↓
Indicator Layer
↓
Strategy Layer
↓
Signal Layer
```
---
# Layer Structure
```text
Strategy Layer
│
├── StrategyEngine
│
├── StrategyLibrary
│   ├── ICT
│   ├── SMC
│   ├── Wyckoff
│   ├── AMD
│   ├── LiquiditySweep
│   ├── Breakout
│   ├── TrendFollowing
│   └── MeanReversion
│
├── StrategyProfiles
│   ├── TradingStyles
│   ├── Sessions
│   ├── Timeframes
│   ├── RiskProfiles
│   ├── Filters
│   └── Presets
│
├── StrategyManager
│
└── StrategyService
```
---
# Responsibilities
Strategy Layer:
✓ Strategy ishlatadi
✓ Strategy tanlaydi
✓ Strategy Validation bajaradi
✓ Strategy Profile qo'llaydi
✓ Strategy Result yaratadi
✓ Strategy Confluence hisoblaydi
---
# Not Responsible
Strategy Layer:
✗ Market Context yaratmaydi
✗ Indicator hisoblamaydi
✗ Signal yaratmaydi
✗ AI Analysis bajarmaydi
✗ Decision qabul qilmaydi
✗ Risk hisoblamaydi
✗ Trade ochmaydi
---
# Input
Strategy Layer qabul qiladi.
• Market Context
• Indicator Context
• Strategy Configuration
• Strategy Profile
---
# Output
Strategy Layer yaratadi.
• Strategy Result
• Strategy Score
• Strategy Confidence
• Strategy Metadata
---
# Workflow
```text
Market Context
↓
Indicator Context
↓
Strategy Selection
↓
Strategy Execution
↓
Apply Strategy Profile
↓
Strategy Validation
↓
Generate Strategy Result
↓
Signal Layer
```
---
# Golden Rules
1. Strategy Layer faqat Context va Indicator Context bilan ishlaydi.
2. Har bir Strategy mustaqil ishlaydi.
3. Strategy natijalari immutable hisoblanadi.
4. Strategy Layer signal yaratmaydi.
5. Strategy Layer AI ishlatmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
05_Strategy_Layer/
├── README.md
├── StrategyEngine/
├── StrategyLibrary/
├── StrategyProfiles/
├── StrategyManager/
├── StrategyService/
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
└── Layer_Contracts.md
```
---
# Summary
Strategy Layer GoldBot Trading Engine ichidagi barcha savdo strategiyalarini boshqaruvchi Canonical Layer hisoblanadi.
U Context Layer va Indicator Layer natijalaridan foydalanadi hamda Signal Layer uchun Strategy Result yaratadi.
