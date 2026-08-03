# Backtest Service Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat BacktestService ichki arxitekturasini tavsiflaydi (ichki submodullar implementatsiya bosqichida to'ldiriladi).
---
# Internal Architecture (Planned)
```text
BacktestService
├── RequestValidator
├── BacktestCoordinator
└── ResultDispatcher
```
---
# Module Position
```text
Owner Command (Platform Layer)
↓
BacktestService
↓
BacktestEngine / ReplayController
```
---
# Processing Pipeline (Planned)
```text
RequestValidator → BacktestCoordinator → ResultDispatcher
```
---
# Dependency Map
```text
Owner Command (Platform Layer)
↓
BacktestService
↓
BacktestEngine / ReplayController
```
---
# Allowed Dependencies
✓ BacktestEngine
✓ ReplayController
✓ BacktestReport
✓ Optimization
---
# Forbidden Dependencies
✗ Execution Layer (real order — Backtesting Isolation Rule)
✗ Broker Gateway
✗ Platform Layer (to'g'ridan-to'g'ri)
✗ Live Data (real vaqt oqimi)
✗ Signal Layer (to'g'ridan-to'g'ri)
✗ AI Layer (to'g'ridan-to'g'ri)
✗ Decision Layer (to'g'ridan-to'g'ri)
✗ Risk Layer (to'g'ridan-to'g'ri)
---
# Runtime Flow
```text
Receive Input
↓
Process (BacktestService)
↓
Emit Output
↓
BacktestEngine / ReplayController
```
---
# Summary
BacktestService BacktestService Backtesting Layer'ning yagona Entry va Exit Gateway'i hisoblanadi.
