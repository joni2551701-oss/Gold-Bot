# Crosshair Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Crosshair modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Crosshair quyidagilar uchun javobgar.
✓ Cursor Tracking
✓ Magnet Snapping
✓ OHLC Tooltip
✓ Price Label
✓ Time Label
Crosshair bajarmaydi.
✗ Rendering Logic
✗ Signal Generation
✗ Data Calculation
✗ AI Analysis
---
# Module Boundary
```text
Chart_Interaction
↓
Crosshair
↓
Chart_Renderer
```
---
# Input Contract
• Interaction Context
• Candle Data
---
# Output Contract
• Crosshair Position
• Tooltip Content
• Price Label
• Time Label
---
# Allowed Dependencies
✓ Chart_Interaction
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
getCrosshairState()
subscribeCrosshairEvent(callback)
configureCrosshair(options)
disposeCrosshair()
```
---
# Architecture Rules
Crosshair:
✓ Cursor Tracking bajaradi.
✓ Module Boundary'ni saqlaydi.
Crosshair:
✗ Signal yoki Decision yaratmaydi.
✗ BOS/CHoCH/FVG/Liquidity hisoblamaydi.
✗ AI ishlatmaydi.
---
# Runtime Rules
1. Crosshair faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Crosshair Signal yoki Decision yaratmaydi.
5. Crosshair BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Cursor Tracking bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Crosshair Contract GoldBot Chart Layer ichidagi Crosshair jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
