# Platform Service Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat PlatformService modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
PlatformService quyidagilar uchun javobgar.
✓ Platform Request Management
✓ Request Validation
✓ Request Routing
✓ Service Coordination
✓ Response Formatting
✓ Session Coordination
PlatformService bajarmaydi.
✗ Authentication Logic
✗ Trading Decision
✗ AI Analysis
✗ Risk Calculation
✗ Order Execution
✗ Database Management
---
# Module Boundary
```text
Platform Channels
↓
PlatformService
↓
Internal Services
```
---
# Input Contract
• Platform Request
• API Request
• Session Metadata
• Authentication Result
---
# Output Contract
• Standard Response
• Service Response
• Platform Metadata
• Routing Metadata
---
# Allowed Dependencies
✓ Authentication
✓ DatabaseService
✓ AIService
✓ DecisionService
✓ RiskService
✓ ExecutionService
✓ MonitoringService
---
# Forbidden Dependencies
✗ Telegram
✗ MobileAPI
✗ WebAPI
✗ DesktopAPI
---
# Runtime Contract
1. PlatformService is the sole entry point to GoldBot Core services — Authentication'dan o'tgan barcha Request'lar PlatformService orqali GoldBot Core Service'larga yo'naltirilishi shart.
2. Har bir Request Validation'dan o'tishi shart.
3. Har bir Request faqat bitta maqsadli Service'ga marshrutlanishi shart.
4. PlatformService Business Logic bajarmaydi.
5. Response standart formatda qaytarilishi shart.
6. Session holati boshqarilishi shart.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Request qabul qilinadi.
✓ Validation bajariladi.
✓ Authentication tekshiriladi.
✓ Routing bajariladi.
✓ Service Response olinadi.
✓ Response standartlashtiriladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
PlatformService Contract GoldBot Platform Layer ichidagi yagona Gateway sifatida ishlashni, barcha tashqi platformalardan kelgan so'rovlarni boshqarishni, ichki Service'larga marshrutlashni va foydalanuvchiga standart javob qaytarishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
