# Replay Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Replay ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Module Position
```text
Chart_API
↓
Replay
↓
Chart_Data
```
---
# Module Architecture (Blueprint)
```text
Replay
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
Replay GoldBot Chart Layer ichidagi Replay moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
