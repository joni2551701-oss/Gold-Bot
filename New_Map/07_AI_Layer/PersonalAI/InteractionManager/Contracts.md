# Interaction Manager Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat InteractionManager modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
InteractionManager quyidagilar uchun javobgar.
✓ User Interaction Management
✓ Session Management
✓ Context Building
✓ Request Routing
✓ Interaction Validation
✓ AI Pipeline Initialization
InteractionManager bajarmaydi.
✗ AI Analysis
✗ Memory Storage
✗ Knowledge Storage
✗ Learning
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
User
↓
InteractionManager
↓
UserProfile
↓
PersonaManager
↓
AIEngine
```
---
# Input Contract
• User Request
• Voice Request
• Vision Request
• System Event
---
# Output Contract
• Interaction Context
• Session Context
• Routed Request
---
# Allowed Dependencies
✓ UserProfile
✓ PersonaManager
---
# Forbidden Dependencies
✗ MemoryManager
✗ KnowledgeManager
✗ LearningEngine
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. Har bir AI Request InteractionManager orqali o'tishi shart.
2. Har bir Interaction uchun Session yaratilishi shart.
3. Interaction Context yaratilishi shart.
4. UserProfile yuklanishi shart.
5. Persona aniqlanishi shart.
6. AI Pipeline InteractionManager orqali boshlanishi shart.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Request qabul qilinadi.
✓ Session yaratiladi.
✓ Interaction Context yaratiladi.
✓ UserProfile yuklanadi.
✓ Persona tanlanadi.
✓ Request AI Pipeline'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
InteractionManager Contract GoldBot PersonalAI ichidagi barcha foydalanuvchi-AI muloqotlarini boshqaruvchi rasmiy Canonical Architecture Contract hisoblanadi.
