# Notification Center Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat NotificationCenter Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Internal Service
↓
NotificationCenter
↓
Receive Event
↓
Validate Notification
↓
Determine Priority
↓
Select Platform
↓
Deliver Notification
↓
Receive Delivery Status
↓
Return Delivery Report
```
---
# Runtime Rules
1. Notification Event mavjud bo'lishi shart.
2. Notification Validation bajarilishi shart.
3. Delivery Platform aniqlanishi shart.
4. Delivery Status qaytarilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Routing
↓
Delivering
↓
Completed
```
---
# Summary
Internal Services
↓
NotificationCenter
↓
Platform Channels
