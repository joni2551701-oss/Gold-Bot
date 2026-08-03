# Analysis Overlay Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Analysis_Overlay modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Analysis_Overlay quyidagilar uchun javobgar.
✓ Market Structure Visualization
✓ BOS/CHoCH Visualization
✓ Order Block Visualization
✓ FVG Visualization
✓ Liquidity Visualization
✓ Wyckoff Visualization
✓ AMD Visualization
✓ Premium/Discount Visualization
✓ Session Visualization
Analysis_Overlay bajarmaydi.
✗ BOS/CHoCH Calculation
✗ Order Block Calculation
✗ FVG Calculation
✗ Liquidity Calculation
✗ Signal Generation
✗ AI Analysis
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
Indicators
↓
Analysis_Overlay
↓
Alerts
```
---
# Input Contract
• Indicator Overlay Data
• Market Context (Chart_API'dan)
• Signal (Chart_API'dan)
• Decision (Chart_API'dan)
---
# Output Contract
• Overlay Object
• Overlay State
• Overlay Metadata
---
# Allowed Dependencies
✓ Indicators
✓ Alerts
✓ Chart_API
---
# Forbidden Dependencies
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
✗ Platform Layer
---
# Public API (Blueprint — imzolar implementatsiya bosqichida aniqlanadi)
```text
getAnalysis_OverlayState()
subscribeAnalysis_OverlayEvent(callback)
configureAnalysis_Overlay(options)
disposeAnalysis_Overlay()
```
---
# Architecture Rules
Analysis_Overlay:
✓ Market Structure Visualization bajaradi.
✓ Module Boundary'ni saqlaydi.
Analysis_Overlay:
✗ Signal yoki Decision yaratmaydi.
✗ BOS/CHoCH/FVG/Liquidity hisoblamaydi.
✗ AI ishlatmaydi.
---
# Runtime Rules
1. Analysis_Overlay faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Analysis_Overlay Signal yoki Decision yaratmaydi.
5. Analysis_Overlay BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Market Structure Visualization bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Analysis_Overlay Contract GoldBot Chart Layer ichidagi Analysis Overlay jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
