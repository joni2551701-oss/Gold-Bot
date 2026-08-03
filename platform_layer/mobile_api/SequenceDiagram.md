# Mobile API Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat MobileAPI Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Mobile App
↓
MobileAPI
↓
Validate Request
↓
Authentication
↓
PlatformService
↓
Receive Response
↓
Build Mobile Response
↓
Return Response
```
---
# Runtime Rules
1. API Request mavjud bo'lishi shart.
2. Request Validation bajarilishi shart.
3. Authentication kerak bo'lsa bajarilishi shart.
4. Platform Response olinishi shart.
5. API Response qaytarilishi shart.
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
Waiting
↓
Responding
↓
Completed
```
---
# Summary
Mobile App
↓
MobileAPI
↓
PlatformService
