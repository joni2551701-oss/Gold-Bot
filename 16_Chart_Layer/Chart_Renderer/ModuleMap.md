# Chart Renderer Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_Renderer ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Internal Architecture (Planned)
```text
Chart_Renderer
        ├── CanvasRenderer
        ├── WebGLRenderer
        ├── LayerRenderer
        ├── OverlayRenderer
        ├── ObjectRenderer
        ├── WatermarkRenderer
        └── RenderPipeline
```
---
# Module Position
```text
Shared Render State
↓
Chart_Renderer
↓
Screenshot / Alerts / Chart_API
```
---
# Processing Pipeline (Planned)
```text
CanvasRenderer → WebGLRenderer → LayerRenderer → WatermarkRenderer → OverlayRenderer → ObjectRenderer → RenderPipeline
```
---
# Dependency Map
```text
Shared Render State
↓
Chart_Renderer
↓
Screenshot / Alerts / Chart_API
```
---
# Allowed Dependencies
✓ Chart_Data
✓ Chart_Interaction
✓ Objects
✓ Drawing_Tools
✓ Indicators
✓ Analysis_Overlay
✓ Theme
✓ Crosshair
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
Read Shared Render State (every frame)
↓
Process (Chart_Renderer)
↓
Emit Output
↓
Screenshot / Alerts / Chart_API
```
---
# Summary
Chart_Renderer GoldBot Chart Layer ichidagi Chart Renderer moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
