# Strategy Layer Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Strategy Layer ichidagi barcha modullar o'rtasidagi bog'lanishni tavsiflaydi.
---
# Layer Architecture
```text
Strategy Layer
        │
        ├── StrategyEngine
        │
        ├── StrategyLibrary
        │      ├── ICT
        │      ├── SMC
        │      ├── Wyckoff
        │      ├── AMD
        │      ├── LiquiditySweep
        │      ├── Breakout
        │      ├── TrendFollowing
        │      └── MeanReversion
        │
        ├── StrategyProfiles
        │      ├── TradingStyles
        │      ├── Sessions
        │      ├── Timeframes
        │      ├── RiskProfiles
        │      ├── Filters
        │      └── Presets
        │
        ├── StrategyManager
        │
        └── StrategyService
```
---
# Dependency Flow
```text
StrategyLibrary
↓
StrategyProfiles
↓
StrategyManager
↓
StrategyEngine
↓
StrategyService
```
---
# External Dependencies
Input
• Context Layer
• Indicator Layer
Output
• Signal Layer
---
# Forbidden Dependencies
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Monitoring Layer
✗ Database Layer
---
# Summary
Strategy Layer GoldBot ichidagi barcha Strategy modullarining yagona Canonical xaritasi hisoblanadi.
