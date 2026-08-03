# Screenshot Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Screenshot ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Module Position
```text
Alerts
↓
Screenshot
↓
Chart_API
```
---
# Module Architecture (Blueprint)
```text
Screenshot
        │
(ichki submodullar implementatsiya bosqichida aniqlanadi)
```
---
# Allowed Dependencies
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
Screenshot GoldBot Chart Layer ichidagi Screenshot moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
