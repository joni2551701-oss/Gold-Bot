# Telegram
Status: CANONICAL
---
# Purpose
Telegram GoldBot Platform Layer ichidagi Canonical Telegram Integration moduli hisoblanadi.
Uning asosiy vazifasi Telegram foydalanuvchilari bilan muloqot qilish, Command, Callback, Message va Navigation jarayonlarini boshqarish hamda PlatformService bilan integratsiyani ta'minlashdir.
Telegram Trading Decision qabul qilmaydi.
Telegram Business Logic bajarmaydi.
Telegram faqat Telegram Platform Integration bilan shug'ullanadi.
---
# Objective
Telegram quyidagi vazifalarni bajaradi.
• Command Processing
• Callback Processing
• Message Processing
• Navigation Management
• Media Processing
• Telegram Session Management
---
# Layer Position
```text
Telegram User
↓
Telegram
↓
Authentication
↓
PlatformService
```
---
# Responsibilities
Telegram
✓ Telegram Update qabul qiladi
✓ Command qayta ishlaydi
✓ Callback qayta ishlaydi
✓ Navigation boshqaradi
✓ Message yuboradi
✓ Media yuboradi
✓ Telegram Session boshqaradi
---
# Not Responsible
Telegram
✗ Authentication Logic
✗ Trading Decision
✗ AI Analysis
✗ Risk Calculation
✗ Database Management
✗ Notification Logic
---
# Input
Telegram qabul qiladi.
• Telegram Update
• Command
• Callback Query
• User Message
• Platform Response
---
# Output
Telegram yaratadi.
• Telegram Message
• Telegram Media
• Reply Keyboard
• Inline Keyboard
• Telegram Metadata
---
# Supported Features
• Commands
• Reply Keyboard
• Inline Keyboard
• Text Messages
• Images
• Documents
• Voice
• Video
---
# Workflow
```text
Receive Telegram Update
↓
Parse Update
↓
Authentication
↓
PlatformService
↓
Receive Response
↓
Generate UI
↓
Send Telegram Response
```
---
# Golden Rules
1. Telegram barcha Update'larni qabul qiladi.
2. Authentication Protected Command uchun majburiy.
3. Telegram Business Logic bajarmaydi.
4. UI Telegram standartlariga mos bo'lishi shart.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Telegram/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Telegram GoldBot Platform Layer ichidagi Canonical Telegram Integration moduli bo'lib, Telegram foydalanuvchilari bilan barcha muloqotni boshqaradi.
