# Chart API Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_API modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Chart_API quyidagilar uchun javobgar.
✓ Public API Exposure
✓ Event API Management
✓ Plugin API Management
✓ Renderer API Exposure
✓ Data API Exposure
✓ Request Validation
Chart_API bajarmaydi.
✗ Rendering
✗ Signal Generation
✗ BOS/CHoCH Calculation
✗ AI Analysis
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
GoldBot Core
↓
Chart_API
↓
Chart_Core
```
---
# Input Contract
• Market Context
• Indicator Context
• Signal
• Decision
• Trade
• External API Request
---
# Output Contract
• Chart Response
• Chart Event
• Plugin Context
• API Metadata
---
# Allowed Dependencies
✓ Chart_Core
✓ Analysis_Overlay
✓ Plugins
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
getChart_APIState()
subscribeChart_APIEvent(callback)
configureChart_API(options)
disposeChart_API()
```
---
# Architecture Rules
Chart_API:
✓ Public API Exposure bajaradi.
✓ Module Boundary'ni saqlaydi.
Chart_API:
✗ Signal yoki Decision yaratmaydi.
✗ BOS/CHoCH/FVG/Liquidity hisoblamaydi.
✗ AI ishlatmaydi.
---
# Runtime Rules
1. Chart_API faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Chart_API Signal yoki Decision yaratmaydi.
5. Chart_API BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Public API Exposure bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Chart_API Contract GoldBot Chart Layer ichidagi Chart API jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
