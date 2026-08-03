# User Repository
Status: CANONICAL
---
# Purpose
UserRepository GoldBot Database Layer ichidagi Canonical User Persistence moduli hisoblanadi.
Uning asosiy vazifasi barcha User, Profile, Settings, Subscription va Preference ma'lumotlarini Database'da saqlash, yangilash va o'qishdir.
UserRepository Business Logic bajarmaydi.
UserRepository Authentication bajarmaydi.
UserRepository faqat User Domain ma'lumotlari bilan ishlaydi.
---
# Objective
UserRepository quyidagi vazifalarni bajaradi.
• User Storage
• Profile Storage
• User Settings Storage
• Subscription Storage
• Preference Storage
• User Query Processing
---
# Layer Position
```text
DatabaseManager
↓
UserRepository
↓
Database Storage
```
---
# Responsibilities
UserRepository
✓ User saqlaydi
✓ User Profile saqlaydi
✓ User Settings saqlaydi
✓ Subscription ma'lumotlarini saqlaydi
✓ Preference ma'lumotlarini saqlaydi
✓ User Query bajaradi
---
# Not Responsible
UserRepository
✗ Authentication
✗ Authorization
✗ Trading Decision
✗ Trade Storage
✗ Market Storage
✗ Cache Management
---
# Input
UserRepository qabul qiladi.
• User Record
• Profile Record
• Settings Record
• Subscription Record
• Query Request
---
# Output
UserRepository yaratadi.
• User Result
• User Profile
• Query Result
• Repository Metadata
---
# Workflow
```text
Receive Repository Request
↓
Validate User Data
↓
Save / Update / Query
↓
Return Repository Result
```
---
# Internal Storage (Real Implementations)
Domen: Foydalanuvchi va hisob domeni.
Repository Aggregation Rule (RAR-001): Database Layer'da repository soni biznes obyektlari soniga teng bo'lishi shart emas. Quyidagi storage implementatsiyalari alohida modul emas — ular shu Repository modulining ichki mas'uliyati hisoblanadi.
```text
UserRepository
├── user
├── subscription
├── feedback
└── admin
```
| Storage | Mas'uliyat |
|---|---|
| `user` | Foydalanuvchi yozuvlari |
| `subscription` | Obuna holati va tarixi |
| `feedback` | Foydalanuvchi fikr-mulohazalari |
| `admin` | Admin yozuvlari (telegram_id, role) |
---
# Golden Rules
1. Har bir User Unique ID bilan saqlanadi.
2. User Settings versiyalanishi kerak.
3. Subscription holati doimo yangilanadi.
4. Sensitive ma'lumotlar xavfsiz saqlanishi shart.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
UserRepository/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
UserRepository GoldBot Database Layer ichidagi User Domain ma'lumotlarini boshqaruvchi Canonical Repository moduli hisoblanadi.
