# Web API
Status: CANONICAL
---
# Purpose
WebAPI GoldBot Platform Layer ichidagi Canonical Web Application Gateway moduli hisoblanadi.
Uning asosiy vazifasi Web Dashboard va GoldBot tizimi o'rtasidagi barcha API aloqalarini boshqarish, foydalanuvchi so'rovlarini PlatformService'ga uzatish hamda natijalarni Web Dashboard'ga qaytarishdir.
WebAPI Trading Decision qabul qilmaydi.
WebAPI Business Logic bajarmaydi.
WebAPI faqat Web Platform Integration bilan shug'ullanadi.
---
# Objective
WebAPI quyidagi vazifalarni bajaradi.
• Web API Request Processing
• Web Authentication Integration
• Dashboard Navigation
• Real-Time Communication
• Session Management
• Web Response Delivery
---
# Layer Position
```text
Web Dashboard
↓
WebAPI
↓
Authentication
↓
PlatformService
```
---
# Responsibilities
WebAPI
✓ API Request qabul qiladi
✓ Authentication bilan ishlaydi
✓ PlatformService'ga Request uzatadi
✓ Dashboard Navigation boshqaradi
✓ Real-Time Event qabul qiladi
✓ API Response qaytaradi
---
# Not Responsible
WebAPI
✗ Trading Decision
✗ AI Analysis
✗ Risk Calculation
✗ Database Management
✗ Order Execution
✗ Business Logic
---
# Input
WebAPI qabul qiladi.
• REST Request
• WebSocket Request
• Authentication Request
• Dashboard Event
• Web Session
---
# Output
WebAPI yaratadi.
• API Response
• Dashboard Response
• Real-Time Event
• Session Metadata
• Web Metadata
---
# Supported Features
• REST API
• WebSocket
• Dashboard Navigation
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
Format Web Response
↓
Return API Response
```
---
# Golden Rules
1. WebAPI barcha Web Request'larni qabul qiladi.
2. Authentication Protected API uchun majburiy.
3. WebAPI Business Logic bajarmaydi.
4. Response Web standartiga mos bo'lishi shart.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
WebAPI/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
WebAPI GoldBot Platform Layer ichidagi Canonical Web Integration moduli bo'lib, Web Dashboard va GoldBot tizimi o'rtasidagi barcha API aloqalarini boshqaradi.
