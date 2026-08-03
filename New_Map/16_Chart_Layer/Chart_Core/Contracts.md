# Chart Core Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_Core modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Chart_Core quyidagilar uchun javobgar.
✓ Chart Lifecycle Management
✓ Chart State Management
✓ Camera Control
✓ Coordinate System Management
✓ Viewport Management
✓ Module Coordination
Chart_Core bajarmaydi.
✗ Rendering
✗ Data Fetching
✗ Signal Generation
✗ BOS/CHoCH Calculation
✗ AI Analysis
✗ Risk Calculation
---
# Module Boundary
```text
Chart_API
↓
Chart_Core
↓
Chart_Data
```
---
# Input Contract
• Chart Request
• Chart Configuration
• Symbol
• Timeframe
---
# Output Contract
• Chart Instance
• Chart State
• Viewport Context
• Camera Context
---
# Allowed Dependencies
✓ Chart_API
✓ Chart_Data
✓ Templates
✓ Layout
✓ Settings
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
getChart_CoreState()
subscribeChart_CoreEvent(callback)
configureChart_Core(options)
disposeChart_Core()
```
---
# Architecture Rules
Chart_Core:
✓ Chart Lifecycle Management bajaradi.
✓ Module Boundary'ni saqlaydi.
Chart_Core:
✗ Signal yoki Decision yaratmaydi.
✗ BOS/CHoCH/FVG/Liquidity hisoblamaydi.
✗ AI ishlatmaydi.
---
# Runtime Rules
1. Chart_Core faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Chart_Core Signal yoki Decision yaratmaydi.
5. Chart_Core BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Chart Lifecycle Management bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Chart_Core Contract GoldBot Chart Layer ichidagi Chart Core jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
