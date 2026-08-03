# Theme Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Theme modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Theme quyidagilar uchun javobgar.
✓ Dark Theme
✓ Light Theme
✓ Custom Theme
✓ Font Management
✓ Color Management
Theme bajarmaydi.
✗ Rendering Logic
✗ Signal Generation
✗ Data Calculation
✗ AI Analysis
---
# Module Boundary
```text
Chart_API
↓
Theme
↓
Chart_Renderer
```
---
# Input Contract
• Theme Request
• Theme Configuration
---
# Output Contract
• Theme Context
• Color Palette
• Font Settings
---
# Allowed Dependencies
✓ Chart_API
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
getThemeState()
subscribeThemeEvent(callback)
configureTheme(options)
disposeTheme()
```
---
# Architecture Rules
Theme:
✓ Dark Theme bajaradi.
✓ Module Boundary'ni saqlaydi.
Theme:
✗ Signal yoki Decision yaratmaydi.
✗ BOS/CHoCH/FVG/Liquidity hisoblamaydi.
✗ AI ishlatmaydi.
---
# Runtime Rules
1. Theme faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Theme Signal yoki Decision yaratmaydi.
5. Theme BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Dark Theme bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Theme Contract GoldBot Chart Layer ichidagi Theme jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
