# Market Repository Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat MarketRepository Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
DatabaseManager
↓
MarketRepository
↓
Receive Repository Request
↓
Validate Market Data
↓
Save / Update / Query
↓
Return Repository Result
↓
Database Storage
```
---
# Runtime Rules
1. Market Record mavjud bo'lishi shart.
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
MarketRepository
↓
Database Storage
