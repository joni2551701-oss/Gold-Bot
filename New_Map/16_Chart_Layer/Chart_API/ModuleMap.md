# Chart API Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_API ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Internal Architecture (Planned)
```text
Chart_API
        ├── PublicAPI
        ├── EventAPI
        ├── PluginAPI
        ├── RendererAPI
        └── DataAPI
```
---
# Module Position
```text
GoldBot Core
↓
Chart_API
↓
Chart_Core
```
---
# Processing Pipeline (Planned)
```text
PublicAPI → EventAPI → PluginAPI → RendererAPI → DataAPI
```
---
# Dependency Map
```text
GoldBot Core
↓
Chart_API
↓
Chart_Core
```
---
# Allowed Dependencies
✓ Chart_Core
✓ Analysis_Overlay
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
Process (Chart_API)
↓
Emit Output
↓
Chart_Core
```
---
# Summary
Chart_API GoldBot Chart Layer ichidagi Chart API moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
