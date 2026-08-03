# Replay Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Replay ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Internal Architecture (Planned)
```text
Replay
        ├── Playback
        ├── ReplayEngine
        ├── ReplayControls
        ├── Speed
        └── Simulation
```
---
# Module Position
```text
Chart_API
↓
Replay
↓
Chart_Data
```
---
# Processing Pipeline (Planned)
```text
Playback → ReplayEngine → ReplayControls → Speed → Simulation
```
---
# Dependency Map
```text
Chart_API
↓
Replay
↓
Chart_Data
```
---
# Allowed Dependencies
✓ Chart_API
✓ Chart_Data
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
Process (Replay)
↓
Emit Output
↓
Chart_Data
```
---
# Summary
Replay GoldBot Chart Layer ichidagi Replay moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
