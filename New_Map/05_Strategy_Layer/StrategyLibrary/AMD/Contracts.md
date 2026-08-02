# AMD Strategy Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat AMD Strategy modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
AMD Strategy quyidagilar uchun javobgar.
✓ Accumulation Analysis
✓ Manipulation Analysis
✓ Liquidity Sweep Analysis
✓ Distribution Analysis
✓ Expansion Analysis
✓ Session Analysis
✓ AMD Confluence
✓ Strategy Result Generation
AMD Strategy bajarmaydi.
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
AMD Strategy
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
• AMD Strategy Result
• AMD Score
• AMD Confidence
• AMD Metadata
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
3. AMD bosqichlari ketma-ket bajarilishi kerak.
4. Strategy Result immutable bo'lishi kerak.
5. Signal yaratish taqiqlanadi.
6. AI ishlatish taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Accumulation aniqlanadi.
✓ Manipulation aniqlanadi.
✓ Liquidity Sweep tekshiriladi.
✓ Distribution aniqlanadi.
✓ Expansion baholanadi.
✓ AMD Confluence yaratiladi.
✓ Strategy Result yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
AMD Strategy Contract GoldBot Strategy Library ichidagi Canonical Accumulation • Manipulation • Distribution Trading Strategy uchun rasmiy arxitektura shartnomasi hisoblanadi.
