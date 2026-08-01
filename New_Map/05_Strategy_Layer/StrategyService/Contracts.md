# Strategy Service Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat StrategyService modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
StrategyService quyidagilar uchun javobgar.
✓ Strategy Request Processing
✓ Strategy Request Validation
✓ StrategyEngine Dispatch
✓ Strategy Result Delivery
✓ Strategy Status Management
✓ Strategy Event Publishing
StrategyService bajarmaydi.
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
• Market Context
• Indicator Context
---
# Output Contract
• Strategy Result
• Strategy Status
• Strategy Metadata
---
# Allowed Dependencies
✓ StrategyEngine
✓ StrategyManager
✓ StrategyLibrary
✓ StrategyProfiles
---
# Forbidden Dependencies
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer Logic
---
# Runtime Contract
1. Barcha Strategy Request'lar StrategyService orqali o'tishi shart.
2. Strategy natijasi o'zgartirilmasdan uzatiladi.
3. StrategyService Strategy Logic bajarmaydi.
4. Validation majburiy.
5. Har bir Request bitta Result qaytarishi kerak.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Request qabul qilinadi.
✓ Request tekshiriladi.
✓ StrategyEngine ishga tushiriladi.
✓ Strategy Result qaytariladi.
✓ Natija Signal Layer'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
StrategyService Contract GoldBot Strategy Layer uchun yagona rasmiy Service Boundary bo'lib, boshqa Layer'lar bilan Strategy Layer o'rtasidagi barcha aloqalarni boshqaradi.
