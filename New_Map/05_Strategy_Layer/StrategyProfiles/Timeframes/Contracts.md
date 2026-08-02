# Timeframes Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Timeframes modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Timeframes quyidagilar uchun javobgar.
✓ Timeframe Selection
✓ Multi-Timeframe Configuration
✓ Timeframe Validation
✓ Strategy Timeframe Profile Generation
✓ Configuration Management
Timeframes bajarmaydi.
✗ Strategy Logic
✗ Indicator Calculation
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Supported Timeframes
Tick
Seconds
Minutes
Hours
Days
Weeks
Months
---
# Input Contract
• User Timeframe Selection
---
# Output Contract
• Timeframe Configuration
• Strategy Timeframe Profile
---
# Allowed Dependencies
✓ StrategyProfiles
✓ StrategyManager
---
# Forbidden Dependencies
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer Logic
---
# Runtime Contract
1. Har qanday Strategy istalgan Timeframe bilan ishlashi mumkin.
2. Multi-Timeframe qo'llab-quvvatlanishi shart.
3. Timeframe strategiyani o'zgartirmaydi.
4. Configuration immutable bo'lishi kerak.
5. Validation majburiy.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Timeframe tanlanadi.
✓ Multi-Timeframe qo'llab-quvvatlanadi.
✓ Configuration yaratiladi.
✓ Validation muvaffaqiyatli bajariladi.
✓ StrategyManager konfiguratsiyani qabul qiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Timeframes Contract GoldBot Strategy Layer ichidagi barcha timeframe konfiguratsiyalarini boshqaruvchi rasmiy arxitektura shartnomasi hisoblanadi.
