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
        └── RenderPipeline
```
---
# Module Position
```text
Chart_Data
↓
Chart_Renderer
↓
Chart_Interaction
```
---
# Processing Pipeline (Planned)
```text
CanvasRenderer → WebGLRenderer → LayerRenderer → OverlayRenderer → ObjectRenderer → RenderPipeline
```
---
# Dependency Map
```text
Chart_Data
↓
Chart_Renderer
↓
Chart_Interaction
```
---
# Allowed Dependencies
✓ Chart_Data
✓ Chart_Interaction
✓ Objects
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
Receive Input
↓
Process (Chart_Renderer)
↓
Emit Output
↓
Chart_Interaction
```
---
# Summary
Chart_Renderer GoldBot Chart Layer ichidagi Chart Renderer moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
