# Templates Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Templates ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Internal Architecture (Planned)
```text
Templates
        ├── Workspace
        ├── Layouts
        ├── IndicatorSets
        ├── DrawingSets
        └── Presets
```
---
# Module Position
```text
Chart_API
↓
Templates
↓
Chart_Core
```
---
# Processing Pipeline (Planned)
```text
Workspace → Layouts → IndicatorSets → DrawingSets → Presets
```
---
# Dependency Map
```text
Chart_API
↓
Templates
↓
Chart_Core
```
---
# Allowed Dependencies
✓ Chart_API
✓ Chart_Core
✓ Layout
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
Process (Templates)
↓
Emit Output
↓
Chart_Core
```
---
# Summary
Templates GoldBot Chart Layer ichidagi Templates moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
