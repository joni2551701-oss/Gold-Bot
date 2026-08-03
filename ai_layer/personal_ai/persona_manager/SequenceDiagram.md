# Persona Manager Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat PersonaManager Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
User
↓
InteractionManager
↓
Load User Profile
↓
Read Persona
↓
PersonaManager
↓
Senior
or
Seniorita
```
---
# Runtime Rules
1. User Profile mavjud bo'lishi kerak.
2. Persona tekshiriladi.
3. Faqat bitta Persona tanlanadi.
4. Shared Memory ishlatiladi.
5. Shared Knowledge ishlatiladi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Loading Profile
↓
Selecting Persona
↓
Routing
↓
Completed
```
---
# Summary
User
↓
PersonaManager
↓
Senior / Seniorita
