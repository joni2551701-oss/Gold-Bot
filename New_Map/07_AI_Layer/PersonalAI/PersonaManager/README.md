# Persona Manager
Status: CANONICAL
---
# Purpose
PersonaManager GoldBot PersonalAI ichidagi Persona boshqaruv moduli hisoblanadi.
Uning asosiy vazifasi foydalanuvchi tanlagan Persona'ni boshqarish va barcha AI so'rovlarini to'g'ri Persona orqali ishlashini ta'minlashdir.
PersonaManager yangi AI yaratmaydi.
PersonaManager Knowledge saqlamaydi.
PersonaManager Memory saqlamaydi.
PersonaManager faqat Persona Routing bilan shug'ullanadi.
---
# Objective
PersonaManager quyidagi vazifalarni bajaradi.
• Persona Selection
• Persona Switching
• Active Persona Management
• Persona Validation
• Persona Routing
• Persona State Management
---
# Layer Position
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
# Supported Personas
• Senior
• Seniorita
---
# Responsibilities
PersonaManager
✓ Active Persona aniqlaydi
✓ Persona almashtiradi
✓ Persona holatini boshqaradi
✓ User Profile bilan ishlaydi
✓ AI Request'ni kerakli Persona'ga yuboradi
---
# Not Responsible
PersonaManager
✗ AI Analysis
✗ Memory
✗ Knowledge
✗ Learning
✗ News Analysis
✗ Voice Processing
✗ Decision Making
---
# Input
PersonaManager qabul qiladi.
• User Request
• User Profile
• Persona Settings
---
# Output
PersonaManager yaratadi.
• Active Persona
• Persona Context
• Routed Request
---
# Workflow
```text
User Request
↓
User Profile
↓
Persona Selection
↓
Senior
or
Seniorita
↓
Continue Pipeline
```
---
# Golden Rules
1. Bir vaqtning o'zida faqat bitta Persona faol bo'ladi.
2. Persona faqat javob uslubini o'zgartiradi.
3. Shared Memory ishlatiladi.
4. Shared Knowledge ishlatiladi.
5. Persona almashtirish Session davomida mumkin.
---
# Related Documents
```text
PersonaManager/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
PersonaManager foydalanuvchi tanlagan Senior yoki Seniorita Persona'ni boshqaruvchi Canonical modul hisoblanadi.
