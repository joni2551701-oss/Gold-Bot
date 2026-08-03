# Web API Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat WebAPI modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
WebAPI quyidagilar uchun javobgar.
✓ API Request Reception
✓ Request Validation
✓ Dashboard Navigation
✓ WebSocket Integration
✓ API Response Delivery
✓ Web Session Management
WebAPI bajarmaydi.
✗ Trading Decision
✗ AI Analysis
✗ Authentication Logic
✗ Database Management
✗ Risk Calculation
✗ Order Execution
---
# Module Boundary
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
# Input Contract
• REST Request
• WebSocket Request
• Authentication Request
• Dashboard Event
• Web Session
---
# Output Contract
• API Response
• Dashboard Response
• Real-Time Event
• Session Metadata
• Web Metadata
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
1. Har bir Web API Request qabul qilinishi shart.
2. Protected API Authentication'dan o'tishi shart.
3. Dashboard Navigation PlatformService orqali boshqarilishi shart.
4. Real-Time Notification NotificationCenter orqali uzatilishi shart.
5. API Response standart formatda qaytarilishi shart.
6. WebAPI Business Logic bajarmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ API Request qabul qilinadi.
✓ Validation bajariladi.
✓ Authentication tekshiriladi.
✓ PlatformService bilan aloqa o'rnatiladi.
✓ Dashboard Response qaytariladi.
✓ WebSocket qo'llab-quvvatlanadi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
WebAPI Contract GoldBot Platform Layer ichidagi Web Dashboard bilan integratsiyani, API Request/Response almashinuvini, Dashboard Navigation va Real-Time Communication boshqaruvini hamda PlatformService bilan xavfsiz muloqotni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
