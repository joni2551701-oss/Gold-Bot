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
Chart_API Entry va Exit — Chart Layer'ning yagona tashqi kirish/chiqish nuqtasi (Chart Runtime Rule).
```text
Entry:  GoldBot Core ↓ Chart_API ↓ Chart_Core
Exit:   Chart_Renderer / Screenshot / Alerts ↓ Chart_API ↓ User
```
---
# Input Contract
Entry:
• Market Context
• Indicator Context
• Signal
• Decision
• Trade
• External API Request
Exit:
• Rendered Frame (Chart_Renderer)
• Export File (Screenshot)
• Alert Trigger (Alerts)
---
# Output Contract
Entry (Chart_Core'ga):
• Chart Request
• Chart Configuration
Exit (Userga):
• Chart Response
• Chart Event
• Plugin Context
• API Metadata
---
# Allowed Dependencies
✓ Chart_Core
✓ Chart_Renderer
✓ Screenshot
✓ Alerts
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
6. Chart_API ham Entry, ham Exit vazifasini bajaradi — Chart Layer'ga boshqa hech qanday to'g'ridan-to'g'ri tashqi kirish/chiqish nuqtasi yo'q.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Public API Exposure bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Chart_API Contract GoldBot Chart Layer ichidagi Chart API jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
