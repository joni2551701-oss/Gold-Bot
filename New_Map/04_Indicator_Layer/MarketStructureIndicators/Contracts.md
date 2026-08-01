# MarketStructureIndicators Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat MarketStructureIndicators modulining rasmiy Architecture Contract hujjati hisoblanadi.
MarketStructureIndicators GoldBot Indicator Layer ichidagi Market Structure asosidagi indikatorlarni hisoblaydigan yagona Canonical modul hisoblanadi.
---
# Module Responsibility
MarketStructureIndicators quyidagilar uchun javobgar.
✓ Swing Strength Calculation
✓ BOS Strength Calculation
✓ CHoCH Strength Calculation
✓ MSS Strength Calculation
✓ Trend Quality Calculation
✓ Breakout Quality Calculation
✓ Range Quality Calculation
✓ Structure Score Calculation
✓ Structure Indicator State Management
MarketStructureIndicators bajarmaydi.
✗ Market Structure Detection
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
MarketStructureIndicators
↓
IndicatorService
↓
Boundary End
---
# Input Contract
• Market Context
• Market Structure State
• Trend State
• Session State
---
# Output Contract
• Swing Strength
• BOS Strength
• CHoCH Strength
• MSS Strength
• Trend Quality
• Breakout Quality
• Range Quality
• Structure Score
• Structure Indicator State
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
2. Market Structure qayta hisoblanishi taqiqlanadi.
3. Har bir indikator deterministik hisoblanadi.
4. Indicator State immutable bo'lishi kerak.
5. Signal yaratish taqiqlanadi.
6. AI ishlatish taqiqlanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
MarketStructureIndicators:
✓ Structure indikatorlarini hisoblaydi.
✓ Structure Score yaratadi.
✓ Indicator State yaratadi.
MarketStructureIndicators:
✗ Market Structure yaratmaydi.
✗ Signal yaratmaydi.
✗ AI ishlatmaydi.
✗ Trade ochmaydi.
---
# Acceptance Criteria
✓ Swing Strength hisoblanadi.
✓ BOS Strength hisoblanadi.
✓ CHoCH Strength hisoblanadi.
✓ MSS Strength hisoblanadi.
✓ Structure Score yaratiladi.
✓ Structure Indicator State yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
MarketStructureIndicators Contract GoldBot Indicator Layer ichidagi Market Structure Indicator Calculation modulining rasmiy arxitektura shartnomasi hisoblanadi.
