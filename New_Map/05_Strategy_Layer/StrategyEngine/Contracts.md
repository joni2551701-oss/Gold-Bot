# StrategyEngine Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat StrategyEngine modulining rasmiy Architecture Contract hujjati hisoblanadi.
StrategyEngine Strategy Layer ichidagi Strategy Execution, Coordination va Result Aggregation'ni boshqaruvchi yagona Canonical Engine hisoblanadi.
---
# Module Responsibility
StrategyEngine quyidagilar uchun javobgar.
✓ Strategy Execution
✓ Strategy Coordination
✓ Strategy Pipeline Management
✓ Strategy Result Collection
✓ Strategy Validation
✓ Strategy Result Aggregation
StrategyEngine bajarmaydi.
✗ Strategy Discovery
✗ Strategy Selection
✗ Strategy Profile Loading
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
StrategyManager
↓
StrategyEngine
↓
StrategyService
```
---
# Input Contract
• Faollashtirilgan Strategiya (StrategyManager'dan)
• Market Context
• Indicator Context
---
# Output Contract
• Strategy Result
• Strategy Score
• Strategy Confidence
• Strategy Metadata
---
# Allowed Dependencies
✓ StrategyManager
✓ Context Layer
✓ Indicator Layer
✓ Event System
---
# Forbidden Dependencies
✗ StrategyLibrary (to'g'ridan-to'g'ri)
✗ StrategyProfiles (to'g'ridan-to'g'ri)
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# State Contract
• Initializing
• Executing
• Validating
• Ready
• Failed
---
# Runtime Contract
1. StrategyEngine faqat StrategyManager tomonidan faollashtirilgan strategiyani qabul qiladi.
2. Context mavjud bo'lishi shart.
3. Indicator Context mavjud bo'lishi shart.
4. Strategy Discovery, Selection va Profile Loading StrategyEngine tomonidan bajarilmaydi.
5. Strategy Result immutable bo'lishi kerak.
6. Signal yaratish taqiqlanadi.
7. AI ishlatish taqiqlanadi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Faollashtirilgan Strategiya StrategyManager'dan qabul qilinadi.
✓ Strategy bajariladi.
✓ Strategy Result yig'iladi va birlashtiriladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
StrategyEngine Contract GoldBot Strategy Layer ichidagi Strategy Execution, Coordination va Result Aggregation'ni boshqaruvchi rasmiy arxitektura shartnomasi hisoblanadi. Strategy Discovery, Selection va Profile Loading StrategyManager vakolatida qoladi.
