# Wyckoff Strategy Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Wyckoff Strategy modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Wyckoff Strategy quyidagilar uchun javobgar.
✓ Market Cycle Analysis
✓ Accumulation Analysis
✓ Distribution Analysis
✓ Phase Detection
✓ Spring Detection
✓ Upthrust Detection
✓ Volume Confirmation
✓ Wyckoff Confluence
✓ Execution Output Generation
Wyckoff Strategy bajarmaydi.
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
Wyckoff Strategy
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
• Wyckoff Execution Output
• Wyckoff Score
• Wyckoff Confidence
• Wyckoff Metadata
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
3. Wyckoff qoidalari qat'iy bajarilishi kerak.
4. Execution Output immutable bo'lishi kerak.
5. Signal yaratish taqiqlanadi.
6. AI ishlatish taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Market Cycle aniqlanadi.
✓ Accumulation va Distribution baholanadi.
✓ Wyckoff Phase aniqlanadi.
✓ Spring va Upthrust tekshiriladi.
✓ Volume Confirmation bajariladi.
✓ Wyckoff Confluence yaratiladi.
✓ Execution Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Wyckoff Strategy Contract GoldBot Strategy Library ichidagi Canonical Wyckoff Trading Strategy uchun rasmiy arxitektura shartnomasi hisoblanadi.
