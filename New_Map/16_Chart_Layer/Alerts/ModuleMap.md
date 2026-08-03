# Alerts Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Alerts ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Module Position
```text
Analysis_Overlay
↓
Alerts
↓
Screenshot
```
---
# Module Architecture (Blueprint)
```text
Alerts
        │
(ichki submodullar implementatsiya bosqichida aniqlanadi)
```
---
# Allowed Dependencies
✓ Analysis_Overlay
✓ Screenshot
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
# Summary
Alerts GoldBot Chart Layer ichidagi Alerts moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
