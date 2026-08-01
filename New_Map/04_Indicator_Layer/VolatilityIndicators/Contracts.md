# VolatilityIndicators Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat VolatilityIndicators modulining rasmiy Architecture Contract hujjati hisoblanadi.
VolatilityIndicators GoldBot Indicator Layer ichidagi barcha Volatility Indicator'larni hisoblaydigan yagona Canonical modul hisoblanadi.
---
# Module Responsibility
VolatilityIndicators quyidagilar uchun javobgar.
✓ ATR Calculation
✓ Bollinger Bands Calculation
✓ Keltner Channel Calculation
✓ Donchian Channel Calculation
✓ Standard Deviation Calculation
✓ Volatility Score Calculation
✓ Volatility Indicator State Management
VolatilityIndicators bajarmaydi.
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
VolatilityIndicators
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
• ATR
• Bollinger Bands
• Keltner Channel
• Donchian Channel
• Standard Deviation
• Volatility Score
• Volatility Indicator State
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
VolatilityIndicators:
✓ Volatility indikatorlarini hisoblaydi.
✓ Volatility Score yaratadi.
✓ Indicator State yaratadi.
VolatilityIndicators:
✗ Strategy bajarmaydi.
✗ Signal yaratmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ ATR hisoblanadi.
✓ Bollinger Bands hisoblanadi.
✓ Keltner Channel hisoblanadi.
✓ Donchian Channel hisoblanadi.
✓ Volatility Indicator State yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
VolatilityIndicators Contract GoldBot Indicator Layer ichidagi Volatility Indicator Calculation modulining rasmiy arxitektura shartnomasi hisoblanadi.
