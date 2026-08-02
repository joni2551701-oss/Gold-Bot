# Interaction Manager Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat InteractionManager Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
User
↓
InteractionManager
↓
Create Session
↓
Build Context
↓
UserProfile
↓
PersonaManager
↓
KnowledgeAI
↓
AIEngine
```
---
# Runtime Rules
1. Har bir Request InteractionManager orqali boshlanadi.
2. Session yaratilishi shart.
3. Interaction Context yaratilishi shart.
4. UserProfile yuklanishi shart.
5. Persona tanlanishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Session Created
↓
Context Building
↓
Routing
↓
Completed
```
---
# Summary
User
↓
InteractionManager
↓
UserProfile
↓
PersonaManager
↓
AI Pipeline
