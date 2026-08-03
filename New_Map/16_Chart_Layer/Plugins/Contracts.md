# Plugins Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Plugins modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Plugins quyidagilar uchun javobgar.
✓ Indicator Plugin Support
✓ Drawing Plugin Support
✓ Overlay Plugin Support
✓ Data Plugin Support
✓ Plugin Lifecycle Management
Plugins bajarmaydi.
✗ Signal Generation
✗ AI Analysis
✗ Risk Calculation
✗ Trade Execution
✗ Rendering
---
# Module Boundary
```text
Chart_API
↓
Plugins
↓
Chart_Core
```
---
# Input Contract
• Plugin Registration Request
• Plugin Configuration
---
# Output Contract
• Plugin Context
• Plugin Status
• Plugin Metadata
---
# Allowed Dependencies
✓ Chart_API
✓ Chart_Core
✓ Indicators
✓ Drawing_Tools
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
getPluginsState()
subscribePluginsEvent(callback)
configurePlugins(options)
disposePlugins()
```
---
# Architecture Rules
Plugins:
✓ Indicator Plugin Support bajaradi.
✓ Module Boundary'ni saqlaydi.
Plugins:
✗ Signal yoki Decision yaratmaydi.
✗ BOS/CHoCH/FVG/Liquidity hisoblamaydi.
✗ AI ishlatmaydi.
---
# Runtime Rules
1. Plugins faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Plugins Signal yoki Decision yaratmaydi.
5. Plugins BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Indicator Plugin Support bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Plugins Contract GoldBot Chart Layer ichidagi Plugins jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
