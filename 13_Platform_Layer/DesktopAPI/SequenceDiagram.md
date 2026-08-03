# Desktop API Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat DesktopAPI Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Desktop Client
↓
DesktopAPI
↓
Validate Request
↓
Authentication
↓
PlatformService
↓
Receive Response
↓
Build Desktop Response
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
Desktop Client
↓
DesktopAPI
↓
PlatformService
