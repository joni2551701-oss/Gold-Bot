# Mobile API
Status: CANONICAL
---
# Purpose
MobileAPI GoldBot Platform Layer ichidagi Canonical Mobile Application Gateway moduli hisoblanadi.
Uning asosiy vazifasi Mobile ilova va GoldBot tizimi o'rtasidagi barcha API aloqalarini boshqarish, foydalanuvchi so'rovlarini PlatformService'ga uzatish hamda natijalarni Mobile ilovaga qaytarishdir.
MobileAPI Trading Decision qabul qilmaydi.
MobileAPI Business Logic bajarmaydi.
MobileAPI faqat Mobile Platform Integration bilan shug'ullanadi.
---
# Objective
MobileAPI quyidagi vazifalarni bajaradi.
• Mobile API Request Processing
• Mobile Authentication Integration
• Navigation Support
• Push Notification Integration
• Session Management
• Mobile Response Delivery
---
# Layer Position
```text
Mobile App
↓
MobileAPI
↓
Authentication
↓
PlatformService
```
---
# Responsibilities
MobileAPI
✓ API Request qabul qiladi
✓ Authentication bilan ishlaydi
✓ PlatformService'ga Request uzatadi
✓ Navigation Data yuboradi
✓ Push Notification qabul qiladi
✓ API Response qaytaradi
---
# Not Responsible
MobileAPI
✗ Trading Decision
✗ AI Analysis
✗ Risk Calculation
✗ Database Management
✗ Order Execution
✗ Business Logic
---
# Input
MobileAPI qabul qiladi.
• REST Request
• WebSocket Request
• Authentication Request
• Push Event
• Mobile Session
---
# Output
MobileAPI yaratadi.
• API Response
• Navigation Response
• Push Notification
• Session Metadata
• Mobile Metadata
---
# Supported Features
• REST API
• WebSocket
• Push Notification
• Mobile Navigation
• Session Management
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
Format Mobile Response
↓
Return API Response
```
---
# Golden Rules
1. MobileAPI barcha Mobile Request'larni qabul qiladi.
2. Authentication Protected API uchun majburiy.
3. MobileAPI Business Logic bajarmaydi.
4. Response Mobile standartiga mos bo'lishi shart.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
MobileAPI/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
MobileAPI GoldBot Platform Layer ichidagi Canonical Mobile Integration moduli bo'lib, Mobile ilova va GoldBot tizimi o'rtasidagi barcha API aloqalarini boshqaradi.
