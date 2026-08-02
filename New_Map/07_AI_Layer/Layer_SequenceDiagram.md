# AI Layer Sequence Diagram
Status: CANONICAL
---
# Runtime Sequence
```text
Signal Layer
↓
AIService (Entry)
↓
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
VoiceAI
↓
ExplanationAI
↓
ConfidenceAI
↓
AI Package
↓
AICoordinator
↓
AIEngine
↓
AIService (Exit)
↓
Decision Layer
```
---
# Runtime Rules
1. AIService AI Layer'ning yagona Entry va Exit nuqtasi hisoblanadi.
2. AIEngine Pipeline'ni boshqaradi, AI modullarini bevosita chaqirmaydi.
3. AICoordinator AI modullarining yagona bevosita chaqiruvchisi hisoblanadi.
4. ConfidenceAI oxirida ishlaydi.
5. AI Package AIEngine va AIService orqali Decision Layer'ga uzatiladi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Processing
↓
Collecting
↓
Packaging
↓
Completed
```
---
# Summary
AI Layer barcha AI modullarini orkestratsiya qilib, Decision Layer uchun yagona AI Package yaratadi.
