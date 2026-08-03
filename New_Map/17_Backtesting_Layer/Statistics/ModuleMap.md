# Statistics Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Statistics ichki arxitekturasini tavsiflaydi (ichki submodullar implementatsiya bosqichida to'ldiriladi).
---
# Internal Architecture (Planned)
```text
Statistics
├── PerformanceMetrics
├── StrategyReport
├── EquityCurve
└── Benchmark
```
---
# Module Position
```text
BacktestEngine
↓
Statistics
↓
BacktestReport
```
---
# Processing Pipeline (Planned)
```text
PerformanceMetrics → StrategyReport → EquityCurve → Benchmark
```
---
# Dependency Map
```text
BacktestEngine
↓
Statistics
↓
BacktestReport
```
---
# Allowed Dependencies
✓ BacktestEngine
✓ BacktestReport
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
Process (Statistics)
↓
Emit Output
↓
BacktestReport
```
---
# Summary
Statistics Statistics simulyatsiya natijalaridan samaradorlik ko'rsatkichlarini hisoblovchi Canonical modul hisoblanadi.
