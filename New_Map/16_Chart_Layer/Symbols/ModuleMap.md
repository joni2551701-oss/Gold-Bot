# Symbols Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Symbols ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Module Position
```text
Chart_API
↓
Symbols
↓
Chart_Data
```
---
# Module Architecture (Blueprint)
```text
Symbols
        │
(ichki submodullar implementatsiya bosqichida aniqlanadi)
```
---
# Allowed Dependencies
✓ Chart_API
✓ Chart_Data
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
Symbols GoldBot Chart Layer ichidagi Symbols moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
