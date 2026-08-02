# TradingStyles Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat TradingStyles modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
TradingStyles quyidagilar uchun javobgar.
✓ Trading Style Selection
✓ Trading Profile Configuration
✓ Strategy Configuration Generation
✓ Configuration Validation
TradingStyles bajarmaydi.
✗ Strategy Logic
✗ Indicator Calculation
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Available Styles
• Scalping
• Intraday
• Swing
• Position
---
# Input Contract
• Trading Style Selection
---
# Output Contract
• Trading Style Configuration
• Strategy Profile
---
# Allowed Dependencies
✓ StrategyManager
✓ StrategyProfiles
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
1. Har bir Strategy istalgan Trading Style bilan ishlashi mumkin.
2. Trading Style Strategy Logic'ni o'zgartirmaydi.
3. Trading Style faqat konfiguratsiya yaratadi.
4. Configuration immutable hisoblanadi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Trading Style tanlanadi.
✓ Configuration yaratiladi.
✓ StrategyManager konfiguratsiyani qabul qiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
TradingStyles Contract GoldBot ichidagi barcha Trading Style konfiguratsiyalarini boshqaruvchi rasmiy arxitektura shartnomasi hisoblanadi.
