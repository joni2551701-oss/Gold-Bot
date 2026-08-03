# Objects Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Objects modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Objects quyidagilar uchun javobgar.
✓ Candle Object Management
✓ Shape Object Management
✓ Text Object Management
✓ Drawing Object Management
✓ Overlay Object Management
✓ Object Lifecycle
Objects bajarmaydi.
✗ Rendering (Chart_Renderer vazifasi)
✗ Signal Generation
✗ Data Calculation
✗ AI Analysis
---
# Module Boundary
```text
Chart_Interaction
↓
Objects
↓
Shared Render State
```
Objects Drawing_Tools/Indicators/Analysis_Overlay'ning Output'ini Input sifatida olmaydi (Chart Shared State Rule). Ular barchasi Shared Render State orqali parallel ishlaydi.
---
# Input Contract
• Interaction Context (Chart_Interaction)
• Chart Data (Chart_Data)
• Chart State (Chart_Core)
---
# Output Contract
• Object List
• Object State
• Object Metadata
(Shared Render State'ga yoziladi)
---
# Allowed Dependencies
✓ Chart_Interaction
✓ Chart_Data
✓ Chart_Core
✓ Chart_Renderer
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
getObjectsState()
subscribeObjectsEvent(callback)
configureObjects(options)
disposeObjects()
```
---
# Architecture Rules
Objects:
✓ Candle Object Management bajaradi.
✓ Module Boundary'ni saqlaydi.
Objects:
✗ Signal yoki Decision yaratmaydi.
✗ BOS/CHoCH/FVG/Liquidity hisoblamaydi.
✗ AI ishlatmaydi.
---
# Runtime Rules
1. Objects faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart va Shared Render State'ga yoziladi.
4. Objects Signal yoki Decision yaratmaydi.
5. Objects BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Objects Drawing_Tools/Indicators/Analysis_Overlay'ning natijasini Input sifatida olmaydi — Chart Shared State Rule.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Candle Object Management bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Objects Contract GoldBot Chart Layer ichidagi Objects jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
