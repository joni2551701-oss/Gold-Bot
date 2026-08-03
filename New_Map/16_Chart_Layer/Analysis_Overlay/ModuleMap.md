# Analysis Overlay Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Analysis_Overlay ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Module Position
```text
Indicators
↓
Analysis_Overlay
↓
Alerts
```
---
# Module Architecture (Blueprint)
```text
Analysis_Overlay
        │
(ichki submodullar implementatsiya bosqichida aniqlanadi)
```
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
# Summary
Analysis_Overlay GoldBot Chart Layer ichidagi Analysis Overlay moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
