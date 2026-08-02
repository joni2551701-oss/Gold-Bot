# Trade Monitoring Layer Module Map
Status: CANONICAL
---
# Layer Architecture
```text
11_Trade_Monitoring_Layer
│
├── MonitoringService
│
├── PositionMonitor
│
├── TradeLifecycleManager
│
├── SLTPMonitor
│
├── BreakevenManager
│
├── TrailingStop
│
├── PartialClose
│
├── RecoveryManager
│
└── Monitoring Result
```
---
# Processing Pipeline
```text
MonitoringService
        │
        ▼
PositionMonitor
        │
        ▼
TradeLifecycleManager
        │
        ▼
SLTPMonitor
        │
        ▼
BreakevenManager
        │
        ▼
TrailingStop
        │
        ▼
PartialClose
        │
        ▼
RecoveryManager
```
---
# Module Responsibilities
## MonitoringService
Monitoring Layer Gateway.
---
## PositionMonitor
Open Position'larni kuzatadi.
---
## TradeLifecycleManager
Trade State va Lifecycle'ni boshqaradi.
---
## SLTPMonitor
Stop Loss va Take Profit triggerlarini kuzatadi.
---
## BreakevenManager
Break Even qoidalarini qo'llaydi.
---
## TrailingStop
Dynamic Stop Loss boshqaradi.
---
## PartialClose
Position'ni qisman yopadi.
---
## RecoveryManager
Restart Recovery va State Restoration bajaradi.
---
# Summary
Trade Monitoring Layer GoldBot arxitekturasidagi Canonical Trade Lifecycle Management Layer hisoblanadi.
