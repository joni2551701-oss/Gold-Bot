# ICT Strategy Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat ICT Strategy modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
ICT Strategy quyidagilar uchun javobgar.
✓ ICT Analysis
✓ Liquidity Analysis
✓ Order Block Analysis
✓ Fair Value Gap Analysis
✓ Premium / Discount Analysis
✓ Session Analysis
✓ ICT Confluence
✓ Strategy Result Generation
ICT Strategy bajarmaydi.
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
ICT Strategy
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
• ICT Strategy Result
• ICT Score
• ICT Confidence
• ICT Metadata
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
3. ICT qoidalari qat'iy bajarilishi kerak.
4. Strategy Result immutable bo'lishi kerak.
5. Signal yaratish taqiqlanadi.
6. AI ishlatish taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ ICT Analysis bajariladi.
✓ ICT Confluence yaratiladi.
✓ Strategy Result yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
ICT Strategy Contract GoldBot Strategy Library ichidagi Canonical ICT Trading Strategy uchun rasmiy arxitektura shartnomasi hisoblanadi.
