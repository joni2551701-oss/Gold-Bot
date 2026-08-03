# Interaction Manager
Status: CANONICAL
---
# Purpose
InteractionManager GoldBot PersonalAI ichidagi foydalanuvchi va AI o'rtasidagi barcha muloqotni boshqaruvchi Canonical modul hisoblanadi.
Uning asosiy vazifasi barcha kiruvchi AI so'rovlarini qabul qilish, Interaction Context yaratish va so'rovni tegishli AI Pipeline'ga uzatishdir.
InteractionManager AI Analysis bajarmaydi.
InteractionManager Knowledge saqlamaydi.
InteractionManager Memory saqlamaydi.
InteractionManager faqat Interaction Lifecycle'ni boshqaradi.
---
# Objective
InteractionManager quyidagi vazifalarni bajaradi.
• User Interaction Management
• Conversation Lifecycle
• Request Processing
• Context Building
• Session Management
• Interaction Routing
---
# Layer Position
```text
User
↓
InteractionManager
↓
UserProfile
↓
PersonaManager
↓
KnowledgeAI
```
---
# Responsibilities
InteractionManager
✓ User Request qabul qiladi
✓ Interaction Session yaratadi
✓ Interaction Context yaratadi
✓ Request'ni UserProfile'ga yuboradi
✓ PersonaManager bilan ishlaydi
✓ AI Pipeline'ni boshlaydi
---
# Not Responsible
InteractionManager
✗ AI Analysis
✗ Memory Storage
✗ Knowledge Storage
✗ Learning
✗ News Analysis
✗ Decision Making
✗ Trade Execution
---
# Input
InteractionManager qabul qiladi.
• User Request
• Voice Request
• Vision Request
• System Event
---
# Output
InteractionManager yaratadi.
• Interaction Context
• Session Context
• Routed Request
---
# Workflow
```text
Receive Request
↓
Create Session
↓
Build Context
↓
Load User Profile
↓
Load Persona
↓
Route Request
↓
Continue AI Pipeline
```
---
# Golden Rules
1. Har bir AI Request InteractionManager orqali o'tadi.
2. InteractionManager barcha Interaction turlarini qo'llab-quvvatlaydi.
3. InteractionManager AI Logic bajarmaydi.
4. InteractionManager Memory saqlamaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
InteractionManager/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
InteractionManager GoldBot PersonalAI ichidagi barcha foydalanuvchi-AI muloqotlarini boshqaruvchi Canonical Interaction Gateway hisoblanadi.
