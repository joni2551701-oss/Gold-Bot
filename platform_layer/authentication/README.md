# Authentication
Status: CANONICAL
---
# Purpose
Authentication GoldBot Platform Layer ichidagi Canonical Identity va Access Management moduli hisoblanadi.
Uning asosiy vazifasi foydalanuvchini ro'yxatdan o'tkazish (Register), tizimga kirishini tasdiqlash (Login), Session boshqarish, Token yaratish va Access Control'ni amalga oshirishdir.
Authentication Trading Decision qabul qilmaydi.
Authentication Business Logic bajarmaydi.
Authentication faqat User Identity va Security bilan shug'ullanadi.
---
# Objective
Authentication quyidagi vazifalarni bajaradi.
• User Registration
• User Login
• User Logout
• User ID Generation
• Session Management
• Token Management
• Access Control
---
# Layer Position
```text
Telegram
MobileAPI
WebAPI
DesktopAPI
↓
Authentication
↓
PlatformService
↓
DatabaseService
```
---
# Responsibilities
Authentication
✓ User Register
✓ User Login
✓ User Logout
✓ User ID yaratadi
✓ Session boshqaradi
✓ Token yaratadi
✓ Permission tekshiradi
---
# Not Responsible
Authentication
✗ Trading Decision
✗ AI Analysis
✗ Risk Calculation
✗ Order Execution
✗ Database Query
✗ Notification Delivery
---
# Input
Authentication qabul qiladi.
• Register Request
• Login Request
• Logout Request
• Token Request
• Session Request
---
# Output
Authentication yaratadi.
• User ID
• Authentication Result
• Access Token
• Session Metadata
• Access Permission
---
# Authentication Workflow
```text
Receive Request
↓
Validate Credentials
↓
Register / Login
↓
Generate User ID
↓
Create Session
↓
Generate Token
↓
Return Authentication Result
```
---
# Golden Rules
1. Har bir foydalanuvchi yagona User ID olishi shart.
2. User ID hech qachon o'zgarmaydi.
3. Har bir Protected Request Authentication'dan o'tishi shart.
4. Session Validation majburiy.
5. Token xavfsiz saqlanishi shart.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Authentication/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Authentication GoldBot Platform Layer ichidagi Canonical Identity va Access Management moduli bo'lib, foydalanuvchilarni ro'yxatdan o'tkazish, tizimga kirishini tasdiqlash, User ID yaratish, Session va Token boshqaruvini amalga oshiradi.
