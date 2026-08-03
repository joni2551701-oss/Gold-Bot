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
Drawing_Tools
```
---
# Input Contract
• Interaction Context
• Drawing Object
• Overlay Object
• Indicator Overlay Data
---
# Output Contract
• Object List
• Object State
• Object Metadata
---
# Allowed Dependencies
✓ Chart_Interaction
✓ Drawing_Tools
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
3. Output standart formatda yaratilishi shart.
4. Objects Signal yoki Decision yaratmaydi.
5. Objects BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Candle Object Management bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Objects Contract GoldBot Chart Layer ichidagi Objects jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
