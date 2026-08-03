# DataValidator Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat DataValidator modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu DataValidator modulining Canonical Runtime Blueprint hisoblanadi.
---
# Complete Runtime Sequence
```text
Data Source
↓
DataValidator
↓
Validate Required Fields
↓
Validate Data Types
↓
Generate Result
↓
SchemaValidator
```
---
# Valid Data Sequence
```text
Receive Data
↓
Validate
↓
Passed
↓
Forward Data
```
---
# Invalid Data Sequence
```text
Receive Data
↓
Validate
↓
Failed
↓
Create Validation Event
↓
Reject Data
```
---
# Runtime Rules
1. Har bir Data tekshiriladi.
2. Invalid Data uzatilmaydi.
3. Validation Result yaratiladi.
4. Validation Event yaratiladi.
5. Circular Runtime taqiqlanadi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Passed
or
Failed
```
---
# Summary
Canonical Runtime Sequence:
Data Source
↓
DataValidator
↓
Validation
↓
SchemaValidator
