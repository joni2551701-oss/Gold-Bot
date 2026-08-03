# Persona Manager Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat PersonaManager modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
PersonaManager quyidagilar uchun javobgar.
✓ Persona Selection
✓ Persona Validation
✓ Persona Switching
✓ Active Persona Management
✓ Persona Routing
✓ Persona Configuration
PersonaManager bajarmaydi.
✗ AI Analysis
✗ Knowledge Storage
✗ Memory Storage
✗ Learning
✗ Voice Processing
✗ Decision Making
✗ Trade Execution
---
# Module Boundary
```text
InteractionManager
↓
PersonaManager
↓
Senior
or
Seniorita
```
---
# Input Contract
• User Request
• User Profile
• Persona Settings
---
# Output Contract
• Active Persona
• Persona Context
• Routed Request
---
# Allowed Dependencies
✓ UserProfile
✓ InteractionManager
✓ Senior
✓ Seniorita
---
# Forbidden Dependencies
✗ KnowledgeManager
✗ MemoryManager
✗ LearningEngine
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. Har bir foydalanuvchida faqat bitta Active Persona bo'ladi.
2. Persona istalgan vaqtda almashtirilishi mumkin.
3. Persona almashtirilganda Memory o'zgarmaydi.
4. Persona almashtirilganda Knowledge o'zgarmaydi.
5. Persona faqat javob uslubi va ovozini o'zgartiradi.
6. Senior va Seniorita bir xil AI Core'dan foydalanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Persona muvaffaqiyatli yuklanadi.
✓ Persona tekshiriladi.
✓ Active Persona aniqlanadi.
✓ Request to'g'ri Persona'ga yuboriladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
PersonaManager Contract GoldBot PersonalAI ichidagi Senior va Seniorita Persona'larini boshqaruvchi rasmiy Canonical Architecture Contract hisoblanadi.
