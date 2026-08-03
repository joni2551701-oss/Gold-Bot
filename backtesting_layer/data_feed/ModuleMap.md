# Data Feed Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat DataFeed ichki arxitekturasini tavsiflaydi (ichki submodullar implementatsiya bosqichida to'ldiriladi).
---
# Internal Architecture (Planned)
```text
DataFeed
├── FeedContract
├── ReplayDataFeed
└── LiveDataFeedAdapter
```
---
# Module Position
```text
BacktestEngine
↓
DataFeed
↓
ReplayEngine
```
---
# Processing Pipeline (Planned)
```text
FeedContract → ReplayDataFeed → LiveDataFeedAdapter
```
---
# Dependency Map
```text
BacktestEngine
↓
DataFeed
↓
ReplayEngine
```
---
# Allowed Dependencies
✓ BacktestEngine
✓ ReplayEngine
---
# Forbidden Dependencies
✗ Execution Layer (real order — Backtesting Isolation Rule)
✗ Broker Gateway
✗ Platform Layer (to'g'ridan-to'g'ri)
✗ Live Data (real vaqt oqimi)
✗ Signal Layer
✗ Strategy Layer
✗ AI Layer
---
# Runtime Flow
```text
Receive Input
↓
Process (DataFeed)
↓
Emit Output
↓
ReplayEngine
```
---
# Summary
DataFeed DataFeed candle manbasi bilan qolgan barcha mantiq o'rtasidagi yagona Canonical seam hisoblanadi.
