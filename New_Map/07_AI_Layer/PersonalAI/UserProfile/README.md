# User Profile
Status: CANONICAL
---
# Purpose
UserProfile GoldBot PersonalAI ichidagi foydalanuvchi profilini boshqaruvchi Canonical modul hisoblanadi.
Uning asosiy vazifasi foydalanuvchining shaxsiy sozlamalari, AI preferensiyalari, trading preferensiyalari va profiling ma'lumotlarini boshqarishdir.
UserProfile Knowledge saqlamaydi.
UserProfile Memory saqlamaydi.
UserProfile faqat foydalanuvchi konfiguratsiyasini boshqaradi.
---
# Objective
UserProfile quyidagi vazifalarni bajaradi.
• User Identity
• User Preferences
• AI Preferences
• Trading Preferences
• Platform Preferences
• Profile Configuration
---
# Layer Position
```text
InteractionManager
↓
UserProfile
↓
PersonaManager
```
---
# Responsibilities
UserProfile
✓ User Profile yuklaydi
✓ User Settings boshqaradi
✓ AI Preferences boshqaradi
✓ Trading Preferences boshqaradi
✓ Platform Preferences boshqaradi
✓ Profile Configuration saqlaydi
---
# Not Responsible
UserProfile
✗ Memory Storage
✗ Knowledge Storage
✗ Learning
✗ AI Analysis
✗ News Analysis
✗ Decision Making
✗ Trade Execution
---
# Input
UserProfile qabul qiladi.
• User ID
• Profile Request
• Settings Update
---
# Output
UserProfile yaratadi.
• User Profile
• User Preferences
• Configuration
---
# Workflow
```text
User
↓
Load Profile
↓
Load Settings
↓
Load Preferences
↓
Return Profile
```
---
# Golden Rules
1. Har bir User faqat bitta Profile'ga ega.
2. Profile Knowledge emas.
3. Profile Memory emas.
4. Profile faqat konfiguratsiya hisoblanadi.
5. User ID o'zgarmaydi.
---
# Related Documents
```text
UserProfile/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
UserProfile GoldBot foydalanuvchilarining shaxsiy konfiguratsiyasi va preferensiyalarini boshqaruvchi Canonical modul hisoblanadi.
