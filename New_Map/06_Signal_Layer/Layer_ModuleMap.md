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
Context Layer
        │
Indicator Layer
        │
Strategy Layer
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
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Monitoring Layer
✗ Database Layer
---
# Summary
Signal Layer GoldBot ichidagi barcha Technical Signal Generation modullarining yagona Canonical xaritasi hisoblanadi.
