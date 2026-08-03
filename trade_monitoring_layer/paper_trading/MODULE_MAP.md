# Paper Trading Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat PaperTrading ichki arxitekturasini tavsiflaydi (ichki submodullar implementatsiya bosqichida to'ldiriladi).
---
# Internal Architecture (Planned)
```text
PaperTrading
├── PaperTrade
├── PaperTradeMonitor
├── VirtualPosition
├── VirtualBalance
└── TradeState
```
---
# Module Position
```text
MonitoringService
↓
PaperTrading
↓
MonitoringService
```
---
# Processing Pipeline (Planned)
```text
PaperTrade → PaperTradeMonitor → VirtualPosition → VirtualBalance → TradeState
```
---
# Dependency Map
```text
MonitoringService
↓
PaperTrading
↓
MonitoringService
```
---
# Allowed Dependencies
✓ MonitoringService
✓ PositionMonitor
✓ TradeLifecycleManager
---
# Forbidden Dependencies
✗ Execution Layer
✗ Broker Gateway
✗ Risk Layer (to'g'ridan-to'g'ri)
✗ Decision Layer
✗ Signal Layer
✗ AI Layer
✗ Database Layer
✗ Platform Layer
---
# Runtime Flow
```text
Receive Input
↓
Process (PaperTrading)
↓
Emit Output
↓
MonitoringService
```
---
# Summary
PaperTrading PaperTrading GoldBot Trade Monitoring Layer ichidagi Canonical Paper Trading moduli hisoblanadi. U real execution emas — pozitsiya hayot aylanishini simulyatsiya qiladi va Broker'ga hech qachon murojaat qilmaydi.
