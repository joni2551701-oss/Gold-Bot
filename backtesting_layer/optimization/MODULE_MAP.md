# Optimization Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Optimization ichki arxitekturasini tavsiflaydi (ichki submodullar implementatsiya bosqichida to'ldiriladi).
---
# Internal Architecture (Planned)
```text
Optimization
├── ParameterSweep
├── RunComparator
└── ResultRanker
```
---
# Module Position
```text
BacktestService
↓
Optimization
↓
BacktestEngine
```
---
# Processing Pipeline (Planned)
```text
ParameterSweep → RunComparator → ResultRanker
```
---
# Dependency Map
```text
BacktestService
↓
Optimization
↓
BacktestEngine
```
---
# Allowed Dependencies
✓ BacktestService
✓ BacktestEngine
✓ Statistics
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
Process (Optimization)
↓
Emit Output
↓
BacktestEngine
```
---
# Summary
Optimization Optimization turli parametrlar bilan ko'p marta Backtest ishga tushirib natijalarni taqqoslovchi Canonical modul hisoblanadi (Blueprint bosqichi).
