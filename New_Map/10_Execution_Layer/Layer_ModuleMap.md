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
└── ExecutionMonitor
```
---
# Processing Pipeline
```text
Risk Layer
        │
        ▼
ExecutionService (Entry)
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
        │
        ▼
ExecutionService (Exit)
        │
        ▼
Trade Monitoring Layer
```
---
# Module Responsibilities
## ExecutionService
Execution Layer'ning ikki tomonlama (bidirectional) Boundary Gateway'i — Entry va Exit.
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
Execution Status va Event'larni kuzatadi. Layer tashqarisiga chiqmaydi — natijani ExecutionService orqali uzatadi.
---
# Summary
Execution Layer GoldBot arxitekturasidagi Canonical Trade Execution Layer hisoblanadi.
