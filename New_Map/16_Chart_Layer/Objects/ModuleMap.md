# Objects Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Objects ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Internal Architecture (Planned)
```text
Objects
        ├── CandleObject
        ├── ShapeObject
        ├── TextObject
        ├── DrawingObject
        ├── OverlayObject
        └── ObjectManager
```
---
# Module Position
```text
Chart_Interaction
↓
Objects
↓
Shared Render State
```
---
# Processing Pipeline (Planned)
```text
CandleObject → ShapeObject → TextObject → DrawingObject → OverlayObject → ObjectManager
```
---
# Dependency Map
```text
Chart_Interaction
↓
Objects
↓
Shared Render State
```
---
# Allowed Dependencies
✓ Chart_Interaction
✓ Chart_Data
✓ Chart_Core
✓ Chart_Renderer
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
Process (Objects)
↓
Emit Output
↓
Shared Render State
```
---
# Summary
Objects GoldBot Chart Layer ichidagi Objects moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
