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
Entry:  GoldBot Core ↓ Chart_API ↓ Chart_Core
Exit:   Chart_Renderer / Screenshot / Alerts ↓ Chart_API ↓ User
```
---
# Processing Pipeline (Planned)
```text
PublicAPI → EventAPI → PluginAPI → RendererAPI → DataAPI
```
---
# Dependency Map
```text
Entry:  GoldBot Core ↓ Chart_API ↓ Chart_Core
Exit:   Chart_Renderer / Screenshot / Alerts ↓ Chart_API ↓ User
```
---
# Allowed Dependencies
✓ Chart_Core
✓ Chart_Renderer
✓ Screenshot
✓ Alerts
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
Entry: Receive GoldBot Core Input → Process → Emit Chart Request/Configuration → Chart_Core
Exit:  Receive Chart_Renderer/Screenshot/Alerts Output → Process → Emit Chart Response/Event → User
```
---
# Summary
Chart_API GoldBot Chart Layer ichidagi Chart API moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
