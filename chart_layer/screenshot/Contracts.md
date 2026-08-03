# Screenshot Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Screenshot modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Screenshot quyidagilar uchun javobgar.
✓ PNG Export
✓ JPG Export
✓ PDF Export
✓ Export Management
Screenshot bajarmaydi.
✗ Rendering Logic
✗ Signal Generation
✗ Data Calculation
✗ AI Analysis
---
# Module Boundary
```text
Chart_Renderer
↓
Screenshot
↓
Chart_API (Exit)
```
Screenshot Alerts'ning Output'ini Input sifatida olmaydi — Chart_Renderer'dagi joriy Rendered Frame'ni capture qiladi (Render Loop Rule / Chart Shared State Rule).
---
# Input Contract
• Rendered Frame (Chart_Renderer)
• Export Configuration
---
# Output Contract
• Export File
• Export Status
• Export Metadata
---
# Allowed Dependencies
✓ Chart_Renderer
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
getScreenshotState()
subscribeScreenshotEvent(callback)
configureScreenshot(options)
disposeScreenshot()
```
---
# Architecture Rules
Screenshot:
✓ PNG Export bajaradi.
✓ Module Boundary'ni saqlaydi.
Screenshot:
✗ Signal yoki Decision yaratmaydi.
✗ BOS/CHoCH/FVG/Liquidity hisoblamaydi.
✗ AI ishlatmaydi.
---
# Runtime Rules
1. Screenshot faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Screenshot Signal yoki Decision yaratmaydi.
5. Screenshot BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Screenshot Alerts'ga bog'liq emas — faqat Chart_Renderer'ning joriy frame'ini capture qiladi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ PNG Export bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Screenshot Contract GoldBot Chart Layer ichidagi Screenshot jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
