# TradingStyles
Status: CANONICAL
---
# Purpose
TradingStyles GoldBot Strategy Layer ichidagi barcha Trading Style konfiguratsiyalarini boshqaruvchi Canonical modul hisoblanadi.
Trading Style strategiyani o'zgartirmaydi.
Trading Style strategiyaning qanday ishlashini konfiguratsiya qiladi.
---
# Objective
TradingStyles quyidagi konfiguratsiyalarni taqdim etadi.
• Scalping
• Intraday
• Swing
• Position
Kelajakda zarurat bo'lsa yangi Trading Style qo'shilishi mumkin.
---
# Responsibilities
TradingStyles:
✓ Trading uslubini belgilaydi
✓ Trade davomiyligini belgilaydi
✓ Tavsiya etilgan Timeframe diapazonini belgilaydi
✓ Trade Profile yaratadi
✓ Strategy Configuration'ni to'ldiradi
---
# Not Responsible
TradingStyles:
✗ Strategy Logic
✗ Indicator Calculation
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Available Trading Styles
## Scalping
Qisqa muddatli savdo.
---
## Intraday
Bir kun ichidagi savdo.
---
## Swing
Bir necha kunlik savdo.
---
## Position
Uzoq muddatli savdo.
---
# Input
Trading Style Selection
---
# Output
Trading Style Configuration
---
# Workflow
```text
User Configuration
↓
Trading Style
↓
StrategyManager
↓
Strategy Result
```
---
# Golden Rules
1. Trading Style strategiyani almashtirmaydi.
2. Har qanday Strategy istalgan Trading Style bilan ishlashi mumkin.
3. Trading Style faqat konfiguratsiya hisoblanadi.
4. Trading Style mustaqil modul hisoblanadi.
---
# Related Documents
```text
TradingStyles/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
TradingStyles GoldBot ichidagi barcha Trading Style konfiguratsiyalarini boshqaruvchi Canonical modul hisoblanadi.
