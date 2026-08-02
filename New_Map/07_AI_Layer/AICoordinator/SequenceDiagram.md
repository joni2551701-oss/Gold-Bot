# AI Coordinator Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat AICoordinator Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
AIEngine
↓
AICoordinator
↓
PersonalAI
↓
KnowledgeAI
↓
FundamentalAI
↓
VisionAI
↓
ExplanationAI
↓
ConfidenceAI
↓
Build AI Package
↓
Decision Layer
```
---
# Runtime Rules
1. Kerakli AI modullar aniqlanadi.
2. Modullar parallel yoki ketma-ket ishlashi mumkin.
3. Natijalar yagona formatga birlashtiriladi.
4. ConfidenceAI oxirida ishlaydi.
5. AI Package Decision Layer'ga uzatiladi.
---
# State Flow
```text
Idle
↓
Preparing
↓
Running Modules
↓
Collecting Results
↓
Building Package
↓
Completed
```
---
# Summary
AIEngine
↓
AICoordinator
↓
AI Package
↓
Decision Layer
