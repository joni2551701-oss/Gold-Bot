# SchemaValidator Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat SchemaValidator modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu SchemaValidator modulining Canonical Runtime Blueprint hisoblanadi.
---
# Complete Runtime Sequence
```text
DataValidator
↓
SchemaValidator
↓
Load Schema
↓
Validate Structure
↓
Validate Fields
↓
Validate Types
↓
Generate Result
↓
QualityValidator
```
---
# Valid Schema Sequence
```text
Receive Data
↓
Load Schema
↓
Schema Match
↓
Forward Data
```
---
# Invalid Schema Sequence
```text
Receive Data
↓
Load Schema
↓
Schema Mismatch
↓
Generate Validation Event
↓
Reject Data
```
---
# Runtime Rules
1. Schema Validation har doim bajariladi.
2. Required Fields tekshiriladi.
3. Data Type tekshiriladi.
4. Invalid Schema uzatilmaydi.
5. Circular Runtime taqiqlanadi.
---
# State Flow
```text
Idle
↓
Loading Schema
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
DataValidator
↓
SchemaValidator
↓
QualityValidator
