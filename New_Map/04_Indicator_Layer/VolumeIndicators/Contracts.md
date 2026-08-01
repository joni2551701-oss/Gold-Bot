# VolumeIndicators Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat VolumeIndicators modulining rasmiy Architecture Contract hujjati hisoblanadi.
VolumeIndicators GoldBot Indicator Layer ichidagi barcha Volume Indicator'larni hisoblaydigan yagona Canonical modul hisoblanadi.
---
# Module Responsibility
VolumeIndicators quyidagilar uchun javobgar.
✓ VWAP Calculation
✓ VWMA Calculation
✓ OBV Calculation
✓ MFI Calculation
✓ CMF Calculation
✓ Accumulation/Distribution Line Calculation
✓ Volume Strength Calculation
✓ Volume Indicator State Management
VolumeIndicators bajarmaydi.
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
VolumeIndicators
↓
IndicatorService
↓
Boundary End
---
# Input Contract
• Market Context
• OHLC Data
• Volume Data
• Historical Data
---
# Output Contract
• VWAP
• VWMA
• OBV
• MFI
• CMF
• Accumulation/Distribution Line
• Volume Strength
• Volume Indicator State
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
2. Volume Data mavjud bo'lishi shart.
3. Har bir indikator deterministik hisoblanadi.
4. Indicator State immutable bo'lishi kerak.
5. Signal yaratish taqiqlanadi.
6. AI ishlatish taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
VolumeIndicators:
✓ Volume indikatorlarini hisoblaydi.
✓ Volume Strength yaratadi.
✓ Indicator State yaratadi.
VolumeIndicators:
✗ Strategy bajarmaydi.
✗ Signal yaratmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ VWAP hisoblanadi.
✓ VWMA hisoblanadi.
✓ OBV hisoblanadi.
✓ MFI hisoblanadi.
✓ CMF hisoblanadi.
✓ Volume Indicator State yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
VolumeIndicators Contract GoldBot Indicator Layer ichidagi Volume Indicator Calculation modulining rasmiy arxitektura shartnomasi hisoblanadi.
