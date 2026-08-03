# TrendIndicators Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat TrendIndicators modulining rasmiy Architecture Contract hujjati hisoblanadi.
TrendIndicators GoldBot Indicator Layer ichidagi barcha Trend Indicator'larni hisoblaydigan yagona Canonical modul hisoblanadi.
---
# Module Responsibility
TrendIndicators quyidagilar uchun javobgar.
✓ EMA Calculation
✓ SMA Calculation
✓ WMA Calculation
✓ HMA Calculation
✓ SuperTrend Calculation
✓ Ichimoku Calculation
✓ Trend Strength Calculation
✓ Trend Indicator State Management
TrendIndicators bajarmaydi.
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
TrendIndicators
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
• EMA
• SMA
• WMA
• HMA
• SuperTrend
• Ichimoku
• Trend Strength
• Trend Indicator State
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
TrendIndicators:
✓ Trend indikatorlarini hisoblaydi.
✓ Trend Strength yaratadi.
✓ Indicator State yaratadi.
TrendIndicators:
✗ Strategy bajarmaydi.
✗ Signal yaratmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ EMA hisoblanadi.
✓ SMA hisoblanadi.
✓ SuperTrend hisoblanadi.
✓ Ichimoku hisoblanadi.
✓ Trend Indicator State yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
TrendIndicators Contract GoldBot Indicator Layer ichidagi Trend Indicator Calculation modulining rasmiy arxitektura shartnomasi hisoblanadi.
