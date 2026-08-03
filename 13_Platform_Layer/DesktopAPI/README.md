# Desktop API
Status: CANONICAL
---
# Purpose
DesktopAPI GoldBot Platform Layer ichidagi Canonical Desktop Application Gateway moduli hisoblanadi.
Uning asosiy vazifasi Desktop Client va GoldBot tizimi o'rtasidagi barcha API aloqalarini boshqarish, foydalanuvchi so'rovlarini PlatformService'ga uzatish hamda natijalarni Desktop ilovaga qaytarishdir.
DesktopAPI Trading Decision qabul qilmaydi.
DesktopAPI Business Logic bajarmaydi.
DesktopAPI faqat Desktop Platform Integration bilan shug'ullanadi.
---
# Objective
DesktopAPI quyidagi vazifalarni bajaradi.
• Desktop API Request Processing
• Desktop Authentication Integration
• Desktop Navigation
• Real-Time Communication
• Session Management
• Desktop Response Delivery
---
# Layer Position
```text
Desktop Client
↓
DesktopAPI
↓
Authentication
↓
PlatformService
```
---
# Responsibilities
DesktopAPI
✓ API Request qabul qiladi
✓ Authentication bilan ishlaydi
✓ PlatformService'ga Request uzatadi
✓ Desktop Navigation boshqaradi
✓ Real-Time Event qabul qiladi
✓ API Response qaytaradi
---
# Not Responsible
DesktopAPI
✗ Trading Decision
✗ AI Analysis
✗ Risk Calculation
✗ Database Management
✗ Order Execution
✗ Business Logic
---
# Input
DesktopAPI qabul qiladi.
• REST Request
• WebSocket Request
• Authentication Request
• Desktop Event
• Desktop Session
---
# Output
DesktopAPI yaratadi.
• API Response
• Desktop Response
• Real-Time Event
• Session Metadata
• Desktop Metadata
---
# Supported Features
• REST API
• WebSocket
• Desktop Navigation
• Session Management
• Real-Time Updates
---
# Workflow
```text
Receive API Request
↓
Validate Request
↓
Authentication
↓
PlatformService
↓
Receive Response
↓
Format Desktop Response
↓
Return API Response
```
---
# Golden Rules
1. DesktopAPI barcha Desktop Request'larni qabul qiladi.
2. Authentication Protected API uchun majburiy.
3. DesktopAPI Business Logic bajarmaydi.
4. Response Desktop standartiga mos bo'lishi shart.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
DesktopAPI/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
DesktopAPI GoldBot Platform Layer ichidagi Canonical Desktop Integration moduli bo'lib, Desktop Client va GoldBot tizimi o'rtasidagi barcha API aloqalarini boshqaradi.
