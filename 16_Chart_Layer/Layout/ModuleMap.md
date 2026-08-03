# Layout Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Layout ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Internal Architecture (Planned)
```text
Layout
        ├── SingleChart
        ├── SplitChart
        ├── Grid
        ├── Sync
        └── WorkspaceManager
```
---
# Module Position
```text
Chart_API
↓
Layout
↓
Chart_Core
```
---
# Processing Pipeline (Planned)
```text
SingleChart → SplitChart → Grid → Sync → WorkspaceManager
```
---
# Dependency Map
```text
Chart_API
↓
Layout
↓
Chart_Core
```
---
# Allowed Dependencies
✓ Chart_API
✓ Chart_Core
✓ Templates
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
Process (Layout)
↓
Emit Output
↓
Chart_Core
```
---
# Summary
Layout GoldBot Chart Layer ichidagi Layout moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
