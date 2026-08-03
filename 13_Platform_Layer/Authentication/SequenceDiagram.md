# Authentication Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Authentication Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Platform
↓
Authentication
↓
Receive Request
↓
Validate Credentials
↓
Register / Login
↓
Generate User ID
↓
Create Session
↓
Generate Token
↓
Return Authentication Result
↓
PlatformService
```
---
# Runtime Rules
1. Authentication Request mavjud bo'lishi shart.
2. Credentials Validation bajarilishi shart.
3. Register vaqtida User ID yaratilishi shart.
4. Login vaqtida Session yaratilishi shart.
5. Token muvaffaqiyatli yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Authenticating
↓
Creating Session
↓
Completed
```
---
# Summary
Platform
↓
Authentication
↓
PlatformService
