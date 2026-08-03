# Strategy Manager Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat StrategyManager modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
StrategyManager quyidagilar uchun javobgar.
✓ Strategy Registration
✓ Strategy Selection
✓ Strategy Configuration Management
✓ Strategy Profile Management
✓ Strategy Lifecycle Management
✓ Strategy Version Management
✓ Configuration Validation
StrategyManager bajarmaydi.
✗ Strategy Analysis
✗ Indicator Calculation
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Input Contract
• Strategy Request
• Strategy Configuration
• Strategy Profile
---
# Output Contract
• Active Strategy
• Active Configuration
• Active Strategy Profile
---
# Allowed Dependencies
✓ StrategyLibrary
✓ StrategyProfiles
✓ StrategyEngine
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
1. Strategy tanlanishi majburiy.
2. Strategy Profile yuklanishi majburiy.
3. Configuration Validation bajarilishi shart.
4. StrategyManager Strategy Logic bajarmaydi.
5. Har bir Active Strategy yagona Configuration bilan ishlaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Strategy muvaffaqiyatli tanlanadi.
✓ Strategy Profile yuklanadi.
✓ Configuration tekshiriladi.
✓ Active Strategy yaratiladi.
✓ StrategyEngine konfiguratsiyani qabul qiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
StrategyManager Contract GoldBot Strategy Layer ichidagi barcha Strategy va Strategy Profile boshqaruvini amalga oshiruvchi rasmiy arxitektura shartnomasi hisoblanadi.
