# User Profile Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat UserProfile modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
UserProfile quyidagilar uchun javobgar.
✓ User Identity
✓ User Settings
✓ User Preferences
✓ Trading Preferences
✓ AI Preferences
✓ Platform Preferences
UserProfile bajarmaydi.
✗ Memory Storage
✗ Knowledge Storage
✗ Learning
✗ AI Analysis
✗ News Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
InteractionManager
↓
UserProfile
↓
PersonaManager
```
---
# Input Contract
• User ID
• Profile Request
• Settings Update
---
# Output Contract
• User Profile
• User Preferences
• Configuration
---
# Allowed Dependencies
✓ InteractionManager
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
1. Har bir User faqat bitta Profile'ga ega.
2. User ID o'zgarmaydi.
3. Profile faqat konfiguratsiyani saqlaydi.
4. Memory UserProfile ichida saqlanmaydi.
5. Knowledge UserProfile ichida saqlanmaydi.
6. Persona UserProfile orqali boshqariladi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ User Profile muvaffaqiyatli yuklanadi.
✓ Preferences yuklanadi.
✓ AI sozlamalari yuklanadi.
✓ Trading sozlamalari yuklanadi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
UserProfile Contract GoldBot foydalanuvchisining identifikatsiyasi, konfiguratsiyasi va preferensiyalarini boshqaruvchi rasmiy Canonical Architecture Contract hisoblanadi.
