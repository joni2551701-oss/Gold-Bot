# User Repository Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat UserRepository Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
DatabaseManager
↓
UserRepository
↓
Receive Repository Request
↓
Validate User Data
↓
Save / Update / Query
↓
Return Repository Result
↓
Database Storage
```
---
# Runtime Rules
1. User Record mavjud bo'lishi shart.
2. Validation muvaffaqiyatli o'tishi shart.
3. Transaction atomik bajarilishi shart.
4. Repository Result qaytarilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Persisting
↓
Completed
```
---
# Summary
DatabaseManager
↓
UserRepository
↓
Database Storage
