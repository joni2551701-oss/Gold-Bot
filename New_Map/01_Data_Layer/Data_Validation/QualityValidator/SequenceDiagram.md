# QualityValidator Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat QualityValidator modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu QualityValidator modulining Canonical Runtime Blueprint hisoblanadi.
---
# Complete Runtime Sequence
```text
SchemaValidator
↓
QualityValidator
↓
Validate Completeness
↓
Validate Value Range
↓
Validate Freshness
↓
Generate Quality Score
↓
IntegrityValidator
```
---
# Valid Quality Sequence
```text
Receive Data
↓
Quality Validation
↓
Passed
↓
Forward Data
```
---
# Invalid Quality Sequence
```text
Receive Data
↓
Quality Validation
↓
Failed
↓
Generate Validation Event
↓
Reject Data
```
---
# Runtime Rules
1. Schema Validation tugagandan keyin boshlanadi.
2. Quality Score yaratiladi.
3. Invalid Quality Data uzatilmaydi.
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
Scoring
↓
Passed
or
Failed
```
---
# Summary
Canonical Runtime Sequence:
SchemaValidator
↓
QualityValidator
↓
IntegrityValidator
