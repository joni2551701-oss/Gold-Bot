# Mobile API Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat MobileAPI modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
MobileAPI quyidagilar uchun javobgar.
✓ API Request Reception
✓ Request Validation
✓ Mobile Navigation
✓ Push Notification Integration
✓ API Response Delivery
✓ Mobile Session Management
MobileAPI bajarmaydi.
✗ Trading Decision
✗ AI Analysis
✗ Authentication Logic
✗ Database Management
✗ Risk Calculation
✗ Order Execution
---
# Module Boundary
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
# Input Contract
• REST Request
• WebSocket Request
• Authentication Request
• Push Event
• Mobile Session
---
# Output Contract
• API Response
• Navigation Response
• Push Notification
• Session Metadata
• Mobile Metadata
---
# Allowed Dependencies
✓ Authentication
✓ PlatformService
✓ NotificationCenter
---
# Forbidden Dependencies
✗ DatabaseService
✗ AIService
✗ DecisionService
✗ RiskService
✗ ExecutionService
✗ MonitoringService
---
# Runtime Contract
1. Har bir Mobile API Request qabul qilinishi shart.
2. Protected API Authentication'dan o'tishi shart.
3. Mobile Navigation ma'lumotlari PlatformService orqali olinishi shart.
4. Push Notification NotificationCenter orqali yuborilishi shart.
5. API Response standart formatda qaytarilishi shart.
6. MobileAPI Business Logic bajarmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ API Request qabul qilinadi.
✓ Validation bajariladi.
✓ Authentication tekshiriladi.
✓ PlatformService bilan aloqa o'rnatiladi.
✓ API Response qaytariladi.
✓ Push Notification qo'llab-quvvatlanadi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
MobileAPI Contract GoldBot Platform Layer ichidagi Mobile ilova bilan integratsiyani, API Request/Response almashinuvini, Navigation va Push Notification boshqaruvini hamda PlatformService bilan xavfsiz muloqotni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
