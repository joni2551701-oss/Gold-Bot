# Chart Core Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_Core ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Internal Architecture (Planned)
```text
Chart_Core
        ├── ChartEngine
        ├── ChartState
        ├── Lifecycle
        ├── Camera
        ├── CoordinateSystem
        └── Viewport
```
---
# Module Position
```text
Chart_API
↓
Chart_Core
↓
Chart_Data
```
---
# Processing Pipeline (Planned)
```text
ChartEngine → ChartState → Lifecycle → Camera → CoordinateSystem → Viewport
```
---
# Dependency Map
```text
Chart_API
↓
Chart_Core
↓
Chart_Data
```
---
# Allowed Dependencies
✓ Chart_API
✓ Chart_Data
✓ Templates
✓ Layout
✓ Settings
✓ Plugins
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
Process (Chart_Core)
↓
Emit Output
↓
Chart_Data
```
---
# Summary
Chart_Core GoldBot Chart Layer ichidagi Chart Core moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
