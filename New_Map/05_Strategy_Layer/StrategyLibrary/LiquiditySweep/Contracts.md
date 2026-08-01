# Liquidity Sweep Strategy Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Liquidity Sweep Strategy modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Liquidity Sweep Strategy quyidagilar uchun javobgar.
✓ Liquidity Pool Analysis
✓ Equal High Analysis
✓ Equal Low Analysis
✓ Stop Hunt Detection
✓ False Breakout Detection
✓ Sweep Confirmation
✓ Rejection Analysis
✓ Liquidity Confluence
✓ Strategy Result Generation
Liquidity Sweep Strategy bajarmaydi.
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
Market Context
↓
Indicator Context
↓
Liquidity Sweep Strategy
↓
StrategyEngine
```
---
# Input Contract
• Market Context
• Indicator Context
• Strategy Profile
---
# Output Contract
• Liquidity Sweep Result
• Liquidity Score
• Liquidity Confidence
• Liquidity Metadata
---
# Allowed Dependencies
✓ Context Layer
✓ Indicator Layer
✓ StrategyEngine
✓ StrategyProfiles
---
# Forbidden Dependencies
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Runtime Contract
1. Market Context mavjud bo'lishi shart.
2. Indicator Context mavjud bo'lishi shart.
3. Liquidity Sweep qoidalari deterministik bajarilishi kerak.
4. Strategy Result immutable bo'lishi kerak.
5. Signal yaratish taqiqlanadi.
6. AI ishlatish taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Liquidity Pool aniqlanadi.
✓ Equal High / Equal Low tekshiriladi.
✓ Stop Hunt aniqlanadi.
✓ False Breakout baholanadi.
✓ Sweep Confirmation bajariladi.
✓ Liquidity Confluence yaratiladi.
✓ Strategy Result yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Liquidity Sweep Strategy Contract GoldBot Strategy Library ichidagi Canonical Liquidity Sweep Trading Strategy uchun rasmiy arxitektura shartnomasi hisoblanadi.
