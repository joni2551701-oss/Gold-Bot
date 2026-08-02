# Trade Repository Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat TradeRepository Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
DatabaseManager
↓
TradeRepository
↓
Receive Repository Request
↓
Validate Trade Data
↓
Save / Update / Query
↓
Return Repository Result
↓
DatabaseService
```
---
# Runtime Rules
1. Trade Record mavjud bo'lishi shart.
2. Ma'lumot Validation'dan o'tishi shart.
3. Transaction muvaffaqiyatli yakunlanishi shart.
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
TradeRepository
↓
DatabaseService
