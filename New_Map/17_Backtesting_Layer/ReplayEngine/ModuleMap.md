# Replay Engine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ReplayEngine ichki arxitekturasini tavsiflaydi (ichki submodullar implementatsiya bosqichida to'ldiriladi).
---
# Internal Architecture (Planned)
```text
ReplayEngine
├── ReplayClock
├── ReplayFeed
├── ReplayLoader
└── ReplayState
```
---
# Module Position
```text
DataFeed
↓
ReplayEngine
↓
Historical Data (Database Layer, read-only)
```
---
# Processing Pipeline (Planned)
```text
ReplayClock → ReplayFeed → ReplayLoader → ReplayState
```
---
# Dependency Map
```text
DataFeed
↓
ReplayEngine
↓
Historical Data (Database Layer, read-only)
```
---
# Allowed Dependencies
✓ DataFeed
✓ ReplayController
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
Process (ReplayEngine)
↓
Emit Output
↓
Historical Data (Database Layer, read-only)
```
---
# Summary
ReplayEngine ReplayEngine tarixiy candle'larni bosqichma-bosqich uzatuvchi Canonical Replay moduli hisoblanadi.
