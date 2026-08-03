# Platform Service
Status: CANONICAL
---
# Purpose
PlatformService GoldBot Platform Layer ichidagi Canonical Platform Gateway moduli hisoblanadi.
PlatformService is the sole entry point to GoldBot Core services — Platform Layer emas (haqiqiy tashqi kirish nuqtalari Telegram/MobileAPI/WebAPI/DesktopAPI va Authentication hisoblanadi).
Uning asosiy vazifasi Authentication'dan o'tgan so'rovlarni qabul qilish, tekshirish va tegishli GoldBot Core Service'larga marshrutlashdir.
PlatformService Business Logic bajarmaydi.
PlatformService Trading Decision qabul qilmaydi.
PlatformService faqat Platform Routing va Service Coordination bilan shug'ullanadi.
---
# Objective
PlatformService quyidagi vazifalarni bajaradi.
• Platform Request Management
• Request Routing
• Service Coordination
• Response Standardization
• Session Coordination
• Platform Integration
---
# Layer Position
```text
Telegram
MobileAPI
WebAPI
DesktopAPI
↓
PlatformService
↓
Authentication
DatabaseService
AIService
DecisionService
RiskService
ExecutionService
MonitoringService
```
---
# Responsibilities
PlatformService
✓ Platform Request qabul qiladi
✓ Request Validation bajaradi
✓ Tegishli Service'ni tanlaydi
✓ Request Routing bajaradi
✓ Standard Response yaratadi
✓ Platform Session boshqaradi
---
# Not Responsible
PlatformService
✗ Authentication
✗ AI Analysis
✗ Trading Decision
✗ Risk Calculation
✗ Order Execution
✗ Database Management
---
# Input
PlatformService qabul qiladi.
• Platform Request
• API Request
• Session Metadata
• Authentication Result
---
# Output
PlatformService yaratadi.
• Standard Response
• Service Response
• Platform Metadata
• Routing Information
---
# Workflow
```text
Receive Platform Request
↓
Validate Request
↓
Route Request
↓
Internal Service
↓
Receive Response
↓
Standardize Response
↓
Return Platform Response
```
---
# Golden Rules
1. PlatformService is the sole entry point to GoldBot Core services (AIService, DecisionService, RiskService, ExecutionService, MonitoringService, DatabaseService) — Authentication'dan o'tgan barcha so'rovlar PlatformService orqali shu Service'larga marshrutlanadi.
2. Har bir Request Validation'dan o'tishi shart.
3. PlatformService Business Logic bajarmaydi.
4. Response yagona formatda qaytariladi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
PlatformService/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
PlatformService GoldBot Platform Layer ichidagi barcha tashqi platformalar uchun yagona Gateway va Public API hisoblanadi.
