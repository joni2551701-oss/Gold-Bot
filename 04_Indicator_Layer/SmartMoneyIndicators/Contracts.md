# SmartMoneyIndicators Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat SmartMoneyIndicators modulining rasmiy Architecture Contract hujjati hisoblanadi.
SmartMoneyIndicators GoldBot Indicator Layer ichidagi Institutional va Smart Money Indicator'larni hisoblaydigan yagona Canonical modul hisoblanadi.
---
# Module Responsibility
SmartMoneyIndicators quyidagilar uchun javobgar.
✓ Liquidity Score Calculation
✓ Order Block Strength Calculation
✓ Fair Value Gap Score Calculation
✓ Imbalance Score Calculation
✓ Premium / Discount Score Calculation
✓ AMD Score Calculation
✓ Wyckoff Score Calculation
✓ Institutional Activity Score Calculation
✓ Smart Money Indicator State Management
SmartMoneyIndicators bajarmaydi.
✗ Market Context Analysis
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
Market Context
↓
SmartMoneyIndicators
↓
IndicatorService
↓
Boundary End
---
# Input Contract
• Market Context
• Liquidity State
• Order Block State
• Fair Value Gap State
• Wyckoff State
• AMD State
• Trend State
---
# Output Contract
• Liquidity Score
• Order Block Strength
• Fair Value Gap Score
• Imbalance Score
• Premium / Discount Score
• AMD Score
• Wyckoff Score
• Institutional Activity Score
• Smart Money Indicator State
---
# Allowed Dependencies
✓ IndicatorEngine
✓ Market Context
✓ IndicatorService
✓ Event System
---
# Forbidden Dependencies
✗ Context Layer (calculation)
✗ Strategy Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# State Contract
• Initializing
• Calculating
• Validating
• Ready
• Failed
---
# Runtime Contract
1. Market Context mavjud bo'lishi shart.
2. Context qayta hisoblanishi taqiqlanadi.
3. Har bir indikator deterministik hisoblanadi.
4. Indicator State immutable bo'lishi kerak.
5. Signal yaratish taqiqlanadi.
6. AI ishlatish taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
SmartMoneyIndicators:
✓ Institutional indikatorlarni hisoblaydi.
✓ Smart Money Score'larni yaratadi.
✓ Indicator State yaratadi.
SmartMoneyIndicators:
✗ Market Context yaratmaydi.
✗ Signal yaratmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ Liquidity Score hisoblanadi.
✓ Order Block Strength hisoblanadi.
✓ Fair Value Gap Score hisoblanadi.
✓ AMD Score hisoblanadi.
✓ Wyckoff Score hisoblanadi.
✓ Institutional Activity Score yaratiladi.
✓ Smart Money Indicator State yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
SmartMoneyIndicators Contract GoldBot Indicator Layer ichidagi Institutional va Smart Money Indicator Calculation modulining rasmiy arxitektura shartnomasi hisoblanadi.
