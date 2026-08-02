# Seniorita Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Seniorita Persona modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Seniorita quyidagilar uchun javobgar.
✓ Friendly Conversation
✓ Trading Assistance
✓ Education Support
✓ Project Assistance
✓ Personalized Friendly Response
Seniorita bajarmaydi.
✗ Knowledge Storage
✗ Memory Storage
✗ Learning
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
PersonaManager
↓
Seniorita
↓
KnowledgeAI
```
---
# Input Contract
• User Request
• User Profile
• Conversation Context
• Knowledge Context
---
# Output Contract
• Friendly Response
• Educational Explanation
• Conversation Result
---
# Allowed Dependencies
✓ PersonaManager
✓ KnowledgeAI
✓ AIEngine
---
# Forbidden Dependencies
✗ MemoryManager
✗ LearningEngine
✗ FundamentalAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. Seniorita alohida AI emas.
2. Shared Memory ishlatilishi shart.
3. Shared Knowledge ishlatilishi shart.
4. Shared Learning ishlatilishi shart.
5. Persona faqat javob uslubi va taqdimotini o'zgartiradi.
6. Seniorita yangi bilim yaratmaydi va saqlamaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Persona to'g'ri tanlanadi.
✓ Shared Knowledge ishlatiladi.
✓ Friendly javob yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Seniorita Contract GoldBot PersonalAI ichidagi Friendly Persona uchun rasmiy Canonical Architecture Contract hisoblanadi. Seniorita mustaqil AI emas, balki Shared AI Core asosida ishlovchi Persona hisoblanadi.
