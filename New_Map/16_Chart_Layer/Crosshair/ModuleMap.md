# Crosshair Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Crosshair ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Internal Architecture (Planned)
```text
Crosshair
        ├── Cursor
        ├── Magnet
        ├── Tooltip
        ├── PriceLabel
        └── TimeLabel
```
---
# Module Position
```text
Chart_Interaction
↓
Crosshair
↓
Chart_Renderer
```
---
# Processing Pipeline (Planned)
```text
Cursor → Magnet → Tooltip → PriceLabel → TimeLabel
```
---
# Dependency Map
```text
Chart_Interaction
↓
Crosshair
↓
Chart_Renderer
```
---
# Allowed Dependencies
✓ Chart_Interaction
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
Process (Crosshair)
↓
Emit Output
↓
Chart_Renderer
```
---
# Summary
Crosshair GoldBot Chart Layer ichidagi Crosshair moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
