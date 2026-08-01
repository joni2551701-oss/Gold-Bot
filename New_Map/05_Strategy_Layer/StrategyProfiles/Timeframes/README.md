# Timeframes
Status: CANONICAL
---
# Purpose
Timeframes GoldBot Strategy Layer ichidagi barcha timeframe konfiguratsiyalarini boshqaruvchi Canonical modul hisoblanadi.
Timeframe strategiyani o'zgartirmaydi.
Timeframe strategiyaning qaysi vaqt oralig'idagi ma'lumotlarda ishlashini belgilaydi.
---
# Objective
Timeframes quyidagi vazifalarni bajaradi.
• Timeframe Selection
• Timeframe Validation
• Multi-Timeframe Configuration
• Strategy Timeframe Profile Generation
• Supported Timeframe Management
---
# Supported Timeframes
## Tick
• Tick
---
## Seconds
• S1
• S5
• S10
• S15
• S30
---
## Minutes
• M1
• M2
• M3
• M4
• M5
• M6
• M10
• M12
• M15
• M20
• M30
• M45
---
## Hours
• H1
• H2
• H3
• H4
• H6
• H8
• H12
---
## Days
• D1
---
## Weeks
• W1
---
## Months
• MN1
---
# Responsibilities
Timeframes
✓ Timeframe tanlaydi
✓ Multi-Timeframe qo'llab-quvvatlaydi
✓ Timeframe Validation bajaradi
✓ Strategy Profile'ni to'ldiradi
✓ Strategy Configuration yaratadi
---
# Not Responsible
Timeframes
✗ Strategy Logic
✗ Indicator Calculation
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
• User Timeframe Selection
---
# Output
• Timeframe Configuration
• Timeframe Profile
---
# Workflow
```text
User Settings
↓
Select Timeframe
↓
Validate Timeframe
↓
Build Timeframe Profile
↓
StrategyEngine
```
---
# Golden Rules
1. Timeframe strategiyani o'zgartirmaydi.
2. Har qanday Strategy istalgan Timeframe bilan ishlashi mumkin.
3. Multi-Timeframe qo'llab-quvvatlanadi.
4. Timeframe Configuration immutable hisoblanadi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Timeframes/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Timeframes GoldBot Strategy Layer ichidagi barcha timeframe konfiguratsiyalarini boshqaruvchi Canonical modul hisoblanadi.
