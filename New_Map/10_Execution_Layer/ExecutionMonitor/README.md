# Execution Monitor
Status: CANONICAL
---
# Purpose
ExecutionMonitor GoldBot Execution Layer ichidagi Canonical Execution Monitoring moduli hisoblanadi.
Uning asosiy vazifasi Broker yoki Exchange tomonidan qaytarilgan barcha Execution Event'larni kuzatish, Order Status o'zgarishlarini aniqlash va Execution Lifecycle'ni nazorat qilishdir.
ExecutionMonitor Order yubormaydi.
ExecutionMonitor Trading Decision qabul qilmaydi.
ExecutionMonitor faqat Execution Monitoring bilan shug'ullanadi.
---
# Objective
ExecutionMonitor quyidagi vazifalarni bajaradi.
• Execution Status Monitoring
• Fill Monitoring
• Partial Fill Monitoring
• Reject Monitoring
• Timeout Monitoring
• Retry Monitoring
• Execution Report Generation
---
# Layer Position
```text
BrokerGateway
↓
ExecutionMonitor
↓
Trade Monitoring Layer
```
---
# Responsibilities
ExecutionMonitor
✓ Order Status kuzatadi
✓ Fill hodisasini aniqlaydi
✓ Partial Fill kuzatadi
✓ Reject holatini kuzatadi
✓ Timeout holatini kuzatadi
✓ Retry Trigger yaratadi
✓ Execution Report yaratadi
---
# Not Responsible
ExecutionMonitor
✗ Trading Decision
✗ Risk Validation
✗ Order Creation
✗ Broker Communication
✗ Position Management
✗ Portfolio Management
---
# Input
ExecutionMonitor qabul qiladi.
• Broker Response
• Execution Result
• Order Status
• Execution Context
---
# Output
ExecutionMonitor yaratadi.
• Execution Status
• Execution Report
• Monitoring Context
• Monitoring Metadata
---
# Execution States
PENDING
↓
SENT
↓
ACCEPTED
↓
PARTIAL_FILLED
↓
FILLED
↓
CANCELLED
↓
REJECTED
↓
TIMEOUT
↓
FAILED
---
# Workflow
```text
Receive Broker Response
↓
Track Order Status
↓
Detect Execution Event
↓
Generate Execution Report
↓
Trade Monitoring Layer
```
---
# Golden Rules
1. Har bir Status o'zgarishi qayd etilishi shart.
2. Fill hodisasi faqat Broker javobi bilan tasdiqlanadi.
3. Timeout alohida Event hisoblanadi.
4. Retry Event log qilinishi shart.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
ExecutionMonitor/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
ExecutionMonitor GoldBot Execution Layer ichidagi Order Execution Lifecycle'ni kuzatuvchi Canonical Monitoring moduli hisoblanadi.
