# Plugins Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Plugins ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Internal Architecture (Planned)
```text
Plugins
        ├── IndicatorPlugins
        ├── DrawingPlugins
        ├── OverlayPlugins
        ├── DataPlugins
        └── PluginManager
```
---
# Module Position
```text
Chart_API
↓
Plugins
↓
Chart_Core
```
---
# Processing Pipeline (Planned)
```text
IndicatorPlugins → DrawingPlugins → OverlayPlugins → DataPlugins → PluginManager
```
---
# Dependency Map
```text
Chart_API
↓
Plugins
↓
Chart_Core
```
---
# Allowed Dependencies
✓ Chart_API
✓ Chart_Core
✓ Indicators
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
# Runtime Flow
```text
Receive Input
↓
Process (Plugins)
↓
Emit Output
↓
Chart_Core
```
---
# Summary
Plugins GoldBot Chart Layer ichidagi Plugins moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
