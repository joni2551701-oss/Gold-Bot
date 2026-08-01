# MomentumIndicators Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat MomentumIndicators modulining rasmiy Architecture Contract hujjati hisoblanadi.
MomentumIndicators GoldBot Indicator Layer ichidagi barcha Momentum Indicator'larni hisoblaydigan yagona Canonical modul hisoblanadi.
---
# Module Responsibility
MomentumIndicators quyidagilar uchun javobgar.
✓ RSI Calculation
✓ Stochastic Calculation
✓ CCI Calculation
✓ ROC Calculation
✓ Momentum Calculation
✓ MACD Histogram Calculation
✓ Momentum Strength Calculation
✓ Momentum Indicator State Management
MomentumIndicators bajarmaydi.
✗ Context Analysis
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
MomentumIndicators
↓
IndicatorService
↓
Boundary End
---
# Input Contract
• Market Context
• OHLC Data
• Historical Data
---
# Output Contract
• RSI
• Stochastic
• CCI
• ROC
• Momentum
• MACD Histogram
• Momentum Strength
• Momentum Indicator State
---
# Allowed Dependencies
✓ IndicatorEngine
✓ Market Context
✓ IndicatorService
✓ Event System
---
# Forbidden Dependencies
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
2. OHLC Data tekshirilishi majburiy.
3. Har bir indikator deterministik hisoblanadi.
4. Indicator State immutable bo'lishi kerak.
5. Signal yaratish taqiqlanadi.
6. AI ishlatish taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
MomentumIndicators:
✓ Momentum indikatorlarini hisoblaydi.
✓ Momentum Strength yaratadi.
✓ Indicator State yaratadi.
MomentumIndicators:
✗ Strategy bajarmaydi.
✗ Signal yaratmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ RSI hisoblanadi.
✓ Stochastic hisoblanadi.
✓ CCI hisoblanadi.
✓ ROC hisoblanadi.
✓ Momentum Indicator State yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
MomentumIndicators Contract GoldBot Indicator Layer ichidagi Momentum Indicator Calculation modulining rasmiy arxitektura shartnomasi hisoblanadi.
