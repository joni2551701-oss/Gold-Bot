# Replay Controller Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ReplayController ichki arxitekturasini tavsiflaydi (ichki submodullar implementatsiya bosqichida to'ldiriladi).
---
# Internal Architecture (Planned)
```text
ReplayController
├── SessionManager
├── SessionRegistry
└── PlaybackCommands
```
---
# Module Position
```text
BacktestService
↓
ReplayController
↓
ReplayEngine
```
---
# Processing Pipeline (Planned)
```text
SessionManager → SessionRegistry → PlaybackCommands
```
---
# Dependency Map
```text
BacktestService
↓
ReplayController
↓
ReplayEngine
```
---
# Allowed Dependencies
✓ BacktestService
✓ ReplayEngine
---
# Forbidden Dependencies
✗ Execution Layer (real order — Backtesting Isolation Rule)
✗ Broker Gateway
✗ Platform Layer (to'g'ridan-to'g'ri)
✗ Live Data (real vaqt oqimi)
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
---
# Runtime Flow
```text
Receive Input
↓
Process (ReplayController)
↓
Emit Output
↓
ReplayEngine
```
---
# Summary
ReplayController ReplayController Replay sessiyalarini boshqaruvchi Canonical Session Management moduli hisoblanadi.
