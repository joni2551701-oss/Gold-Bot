# Platform Layer
Status: CANONICAL
---
# Purpose
Platform Layer GoldBot arxitekturasidagi Canonical User Interaction Layer hisoblanadi.
Uning asosiy vazifasi foydalanuvchi va GoldBot tizimi o'rtasidagi barcha aloqalarni boshqarish, platformalardan kelgan so'rovlarni qabul qilish, autentifikatsiya qilish, kerakli Service'ga yo'naltirish va javobni foydalanuvchiga yetkazishdir.
Platform Layer Trading Decision qabul qilmaydi.
Platform Layer AI Analysis bajarmaydi.
Platform Layer Order Execution bajarmaydi.
Platform Layer faqat User Interface, Authentication, Routing va Notification bilan shug'ullanadi.
---
# Objective
Platform Layer quyidagi vazifalarni bajaradi.
• User Registration
• User Authentication
• Session Management
• Platform Routing
• User Notification
• Multi-Platform Communication
---
# Layer Position
```text
Database Layer
↓
Platform Layer
↓
User
```
---
# Internal Modules
```text
Platform Layer
├── PlatformService
├── Authentication
├── NotificationCenter
├── Telegram
├── MobileAPI
├── WebAPI
└── DesktopAPI
```
---
# Responsibilities
Platform Layer
✓ User Register
✓ User Login
✓ Authentication
✓ Session Management
✓ Platform Routing
✓ Notification Delivery
✓ Multi-Platform Support
---
# Not Responsible
Platform Layer
✗ Market Analysis
✗ AI Analysis
✗ Signal Generation
✗ Trading Decision
✗ Risk Calculation
✗ Order Execution
✗ Position Monitoring
✗ Database Management
---
# Input
Platform Layer qabul qiladi.
• User Request
• Authentication Request
• API Request
• Notification Event
• Platform Events
---
# Output
Platform Layer yaratadi.
• User Response
• Authentication Result
• Notification
• API Response
• Session Metadata
---
# Supported Platforms
• Telegram
• Mobile
• Web
• Desktop
---
# Workflow
```text
Receive User Request
↓
Authentication
↓
PlatformService
↓
Internal Services
↓
NotificationCenter
↓
Return Response
```
---
# Golden Rules
1. Platform Layer barcha foydalanuvchi so'rovlarining yagona kirish nuqtasi hisoblanadi.
2. Har bir foydalanuvchi noyob User ID bilan ishlaydi.
3. Authentication barcha Protected Request'lar uchun majburiy.
4. Platform Layer Business Logic bajarmaydi.
5. Platform Layer faqat Routing va User Communication bilan shug'ullanadi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
13_Platform_Layer/
├── README.md
├── PlatformService/
├── Authentication/
├── NotificationCenter/
├── Telegram/
├── MobileAPI/
├── WebAPI/
├── DesktopAPI/
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
└── Layer_Contracts.md
```
---
# Summary
Platform Layer GoldBot arxitekturasidagi Canonical User Interaction Layer hisoblanadi.
U foydalanuvchilarni autentifikatsiya qiladi, ularga noyob User ID taqdim etadi, barcha platformalardan kelgan so'rovlarni kerakli Service'larga yo'naltiradi va natijalarni foydalanuvchiga xavfsiz hamda standart formatda yetkazadi.
