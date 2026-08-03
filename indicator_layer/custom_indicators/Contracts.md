# CustomIndicators Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat CustomIndicators modulining rasmiy Architecture Contract hujjati hisoblanadi.
CustomIndicators GoldBot Indicator Layer ichidagi proprietary indikatorlarni hisoblaydigan yagona Canonical modul hisoblanadi.
---
# Module Responsibility
CustomIndicators quyidagilar uchun javobgar.
✓ Composite Market Score Calculation
✓ Market Confidence Index Calculation
✓ Liquidity Pressure Index Calculation
✓ Institutional Strength Index Calculation
✓ Smart Trend Index Calculation
✓ Risk Environment Index Calculation
✓ Custom Indicator State Management
CustomIndicators bajarmaydi.
✗ Market Context Analysis
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
Indicator Context
↓
CustomIndicators
↓
IndicatorService
↓
Boundary End
---
# Input Contract
• Market Context
• Trend Indicators
• Momentum Indicators
• Volatility Indicators
• Volume Indicators
• Market Structure Indicators
• Smart Money Indicators
---
# Output Contract
• Composite Market Score
• Market Confidence Index
• Liquidity Pressure Index
• Institutional Strength Index
• Smart Trend Index
• Risk Environment Index
• Custom Indicator State
---
# Allowed Dependencies
✓ IndicatorEngine
✓ Indicator Context
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
1. Indicator Context mavjud bo'lishi shart.
2. Faqat GoldBot proprietary indikatorlari hisoblanadi.
3. Klassik indikatorlar qayta hisoblanmaydi.
4. Indicator State immutable bo'lishi shart.
5. Signal yaratish taqiqlanadi.
6. AI ishlatish taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
CustomIndicators:
✓ Proprietary indikatorlarni hisoblaydi.
✓ Composite Score yaratadi.
✓ Indicator State yaratadi.
CustomIndicators:
✗ Signal yaratmaydi.
✗ Strategy bajarmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ Composite Market Score yaratiladi.
✓ Market Confidence Index yaratiladi.
✓ Liquidity Pressure Index yaratiladi.
✓ Institutional Strength Index yaratiladi.
✓ Smart Trend Index yaratiladi.
✓ Custom Indicator State yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
CustomIndicators Contract GoldBot Indicator Layer ichidagi GoldBot proprietary indikatorlarini hisoblash uchun rasmiy arxitektura shartnomasi hisoblanadi.
