# Signal Layer Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Signal Layer ichidagi barcha modullar va ularning bog'lanishini tavsiflaydi.
---
# Layer Architecture
```text
Signal Layer
        │
        ├── SignalEngine
        │
        ├── ConfluenceEngine
        │
        ├── SignalBuilder
        │
        ├── SignalValidator
        │
        ├── SignalScoring
        │
        ├── SignalFormatter
        │
        └── SignalService
```
---
# Dependency Flow
```text
Strategy Layer
        │
        ▼
SignalEngine (Pipeline Orchestration)
        │
Context Layer
        │
Indicator Layer
        │
        ▼
ConfluenceEngine
        │
        ▼
SignalBuilder
        │
        ▼
SignalValidator
        │
        ▼
SignalScoring
        │
        ▼
SignalFormatter
        │
        ▼
SignalService
        │
        ▼
AI Layer
```
---
# Internal Modules
✓ SignalEngine
✓ ConfluenceEngine
✓ SignalBuilder
✓ SignalValidator
✓ SignalScoring
✓ SignalFormatter
✓ SignalService
---
# External Dependencies
Input
• Context Layer
• Indicator Layer
• Strategy Layer
Output
• AI Layer
---
# Forbidden Dependencies
✗ AI Layer Internal Modules
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Monitoring Layer
✗ Database Layer
✗ Platform Layer
---
# Summary
Signal Layer GoldBot ichidagi barcha Technical Signal Generation modullarining yagona Canonical xaritasi hisoblanadi.
