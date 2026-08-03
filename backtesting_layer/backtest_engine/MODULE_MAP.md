# Backtest Engine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat BacktestEngine ichki arxitekturasini tavsiflaydi (ichki submodullar implementatsiya bosqichida to'ldiriladi).
---
# Internal Architecture (Planned)
```text
BacktestEngine
├── ChainRunner
├── CandidateEvaluator
└── SimulationLoop
```
---
# Module Position
```text
BacktestService
↓
BacktestEngine
↓
DataFeed
```
---
# Processing Pipeline (Planned)
```text
ChainRunner → CandidateEvaluator → SimulationLoop
```
---
# Dependency Map
```text
BacktestService
↓
BacktestEngine
↓
DataFeed
```
---
# Allowed Dependencies
✓ BacktestService
✓ DataFeed
✓ Statistics
✓ PaperTrading (11_Trade_Monitoring_Layer)
---
# Forbidden Dependencies
✗ Execution Layer (real order — Backtesting Isolation Rule)
✗ Broker Gateway
✗ Platform Layer (to'g'ridan-to'g'ri)
✗ Live Data (real vaqt oqimi)
---
# Runtime Flow
```text
Receive Input
↓
Process (BacktestEngine)
↓
Emit Output
↓
DataFeed
```
---
# Summary
BacktestEngine BacktestEngine tarixiy ma'lumot ustida to'liq GoldBot zanjirini simulyatsiya qiluvchi Canonical Orchestrator hisoblanadi.
