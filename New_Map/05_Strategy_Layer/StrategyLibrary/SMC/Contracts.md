# SMC Strategy Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat SMC Strategy modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
SMC Strategy quyidagilar uchun javobgar.
✓ Market Structure Analysis
✓ BOS Analysis
✓ CHoCH Analysis
✓ Liquidity Analysis
✓ Order Block Analysis
✓ Fair Value Gap Analysis
✓ Imbalance Analysis
✓ Premium / Discount Analysis
✓ SMC Confluence
✓ Strategy Result Generation
SMC Strategy bajarmaydi.
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
SMC Strategy
↓
StrategyManager
```
---
# Input Contract
• Market Context
• Indicator Context
• Strategy Profile
---
# Output Contract
• SMC Strategy Result
• SMC Score
• SMC Confidence
• SMC Metadata
---
# Allowed Dependencies
✓ Context Layer
✓ Indicator Layer
✓ StrategyManager
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
3. SMC qoidalari qat'iy bajarilishi kerak.
4. Strategy Result immutable bo'lishi kerak.
5. Signal yaratish taqiqlanadi.
6. AI ishlatish taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Market Structure tekshiriladi.
✓ BOS va CHoCH baholanadi.
✓ Liquidity va Order Block tekshiriladi.
✓ Fair Value Gap va Imbalance baholanadi.
✓ SMC Confluence yaratiladi.
✓ Strategy Result yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
SMC Strategy Contract GoldBot Strategy Library ichidagi Canonical Smart Money Concepts Trading Strategy uchun rasmiy arxitektura shartnomasi hisoblanadi.
