# Confluence Engine Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ConfluenceEngine Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Context
↓
Indicator Context
↓
Strategy Result
↓
ConfluenceEngine
↓
Merge Components
↓
Validate Alignment
↓
Generate Technical Confluence
↓
SignalBuilder
```
---
# Runtime Rules
1. Context mavjud bo'lishi kerak.
2. Indicator Context mavjud bo'lishi kerak.
3. Strategy Result mavjud bo'lishi kerak.
4. Alignment Validation majburiy.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Aggregating
↓
Validating
↓
Completed
or
Failed
```
---
# Summary
Context
↓
Indicators
↓
Strategy
↓
ConfluenceEngine
↓
Technical Confluence
↓
SignalBuilder
