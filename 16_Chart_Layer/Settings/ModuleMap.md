# Settings Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Settings ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Internal Architecture (Planned)
```text
Settings
        ├── Grid
        ├── PriceScale
        ├── TimeScale
        ├── Behaviour
        ├── Magnet
        └── AutoScale
```
---
# Module Position
```text
Chart_API
↓
Settings
↓
Chart_Core
```
---
# Processing Pipeline (Planned)
```text
Grid → PriceScale → TimeScale → Behaviour → Magnet → AutoScale
```
---
# Dependency Map
```text
Chart_API
↓
Settings
↓
Chart_Core
```
---
# Allowed Dependencies
✓ Chart_API
✓ Chart_Core
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
# Runtime Flow
```text
Receive Input
↓
Process (Settings)
↓
Emit Output
↓
Chart_Core
```
---
# Summary
Settings GoldBot Chart Layer ichidagi Settings moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
