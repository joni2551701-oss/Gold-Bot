# Backtest Report Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat BacktestReport ichki arxitekturasini tavsiflaydi (ichki submodullar implementatsiya bosqichida to'ldiriladi).
---
# Internal Architecture (Planned)
```text
BacktestReport
├── ReportBuilder
├── ReportFormatter
└── ReportModel
```
---
# Module Position
```text
Statistics
↓
BacktestReport
↓
BacktestService (Exit)
```
---
# Processing Pipeline (Planned)
```text
ReportBuilder → ReportFormatter → ReportModel
```
---
# Dependency Map
```text
Statistics
↓
BacktestReport
↓
BacktestService (Exit)
```
---
# Allowed Dependencies
✓ Statistics
✓ BacktestService
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
Process (BacktestReport)
↓
Emit Output
↓
BacktestService (Exit)
```
---
# Summary
BacktestReport BacktestReport yakuniy Backtest natijasini yig'uvchi va formatlovchi Canonical modul hisoblanadi.
