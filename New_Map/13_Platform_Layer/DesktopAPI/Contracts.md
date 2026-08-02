# Desktop API Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat DesktopAPI modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
DesktopAPI quyidagilar uchun javobgar.
✓ API Request Reception
✓ Request Validation
✓ Desktop Navigation
✓ Real-Time Communication
✓ API Response Delivery
✓ Desktop Session Management
DesktopAPI bajarmaydi.
✗ Trading Decision
✗ AI Analysis
✗ Authentication Logic
✗ Database Management
✗ Risk Calculation
✗ Order Execution
---
# Module Boundary
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
# Input Contract
• REST Request
• WebSocket Request
• Authentication Request
• Desktop Event
• Desktop Session
---
# Output Contract
• API Response
• Desktop Response
• Real-Time Event
• Session Metadata
• Desktop Metadata
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
1. Har bir Desktop API Request qabul qilinishi shart.
2. Protected API Authentication'dan o'tishi shart.
3. Desktop Navigation PlatformService orqali boshqarilishi shart.
4. Real-Time Notification NotificationCenter orqali uzatilishi shart.
5. API Response standart formatda qaytarilishi shart.
6. DesktopAPI Business Logic bajarmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ API Request qabul qilinadi.
✓ Validation bajariladi.
✓ Authentication tekshiriladi.
✓ PlatformService bilan aloqa o'rnatiladi.
✓ Desktop Response qaytariladi.
✓ Real-Time Communication qo'llab-quvvatlanadi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
DesktopAPI Contract GoldBot Platform Layer ichidagi Desktop Client bilan integratsiyani, API Request/Response almashinuvini, Desktop Navigation va Real-Time Communication boshqaruvini hamda PlatformService bilan xavfsiz muloqotni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
