# Order Router
Status: CANONICAL
---
# Purpose
OrderRouter GoldBot Execution Layer ichidagi Canonical Order Routing moduli hisoblanadi.
Uning asosiy vazifasi tayyorlangan Order'ni mos Broker yoki Exchange Gateway'ga yo'naltirishdir.
OrderRouter Order yaratmaydi.
OrderRouter Broker API bilan to'g'ridan-to'g'ri ishlamaydi.
OrderRouter faqat Order Routing bilan shug'ullanadi.
---
# Objective
OrderRouter quyidagi vazifalarni bajaradi.
• Route Selection
• Broker Selection
• Exchange Selection
• Route Validation
• Order Dispatch
• Routing Report Generation
---
# Layer Position
```text
OrderManager
↓
OrderRouter
↓
BrokerGateway
```
---
# Responsibilities
OrderRouter
✓ Order Route tanlaydi
✓ Broker tanlaydi
✓ Exchange tanlaydi
✓ Routing Rule tekshiradi
✓ Order Dispatch yaratadi
✓ Routing Report yaratadi
---
# Not Responsible
OrderRouter
✗ Trading Decision
✗ Risk Validation
✗ Broker Communication
✗ Order Validation
✗ Position Monitoring
✗ Execution Monitoring
---
# Input
OrderRouter qabul qiladi.
• Managed Order
• Routing Policy
• Broker Configuration
• Execution Context
---
# Output
OrderRouter yaratadi.
• Routed Order
• Routing Context
• Routing Report
• Routing Metadata
---
# Workflow
```text
Receive Managed Order
↓
Load Routing Policy
↓
Select Destination
↓
Validate Route
↓
Create Routed Order
↓
BrokerGateway
```
---
# Golden Rules
1. Har bir Order faqat bitta Route oladi.
2. Routing Policy majburiy.
3. Broker tanlash deterministik bo'lishi kerak.
4. Broker API bilan bevosita aloqa qilmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
OrderRouter/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
OrderRouter GoldBot Execution Layer ichidagi Order Routing va Destination Selection jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
