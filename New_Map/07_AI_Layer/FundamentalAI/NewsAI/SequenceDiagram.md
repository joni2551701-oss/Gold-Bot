# News AI Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat NewsAI Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
News Provider
↓
NewsAI
↓
Filter News
↓
Classify News
↓
Analyze Impact
↓
Generate Summary
↓
Generate News Context
↓
FundamentalAI
```
---
# Runtime Rules
1. News mavjud bo'lishi kerak.
2. News avval filtrlanadi.
3. Impact baholanishi shart.
4. Summary yaratiladi.
5. News Context yaratiladi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Filtering
↓
Analyzing
↓
Summarizing
↓
Completed
or
Failed
```
---
# Summary
News Provider
↓
NewsAI
↓
News Context
↓
FundamentalAI
