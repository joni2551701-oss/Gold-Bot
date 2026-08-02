# Execution Layer Module Map
Status: CANONICAL
---
# Layer Architecture
```text
10_Execution_Layer
│
├── ExecutionService
│
├── ExecutionEngine
│
├── OrderValidator
│
├── OrderManager
│
├── OrderRouter
│
├── BrokerGateway
│
├── ExecutionMonitor
│
└── Execution Result
```
---
# Processing Pipeline
```text
ExecutionService
        │
        ▼
ExecutionEngine
        │
        ▼
OrderValidator
        │
        ▼
OrderManager
        │
        ▼
OrderRouter
        │
        ▼
BrokerGateway
        │
        ▼
ExecutionMonitor
```
---
# Module Responsibilities
## ExecutionService
Execution Layer Gateway.
---
## ExecutionEngine
Execution Pipeline boshqaradi.
---
## OrderValidator
Order parametrlarini tekshiradi.
---
## OrderManager
Order Lifecycle'ni boshqaradi.
---
## OrderRouter
Broker yoki Exchange tanlaydi.
---
## BrokerGateway
Tashqi API bilan ishlaydi.
---
## ExecutionMonitor
Execution Status va Event'larni kuzatadi.
---
# Summary
Execution Layer GoldBot arxitekturasidagi Canonical Trade Execution Layer hisoblanadi.
