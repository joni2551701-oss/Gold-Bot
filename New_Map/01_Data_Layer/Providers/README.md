# Providers
Status: CANONICAL
---
# Purpose
Providers GoldBot Data Layer ichidagi Canonical External Market Data Provider Group hisoblanadi.
Uning asosiy vazifasi tashqi Market Data Provider'lar bilan xavfsiz va standart integratsiyani ta'minlashdir.
Providers Market Data yaratmaydi.
Providers Market Analysis bajarmaydi.
Providers faqat tashqi servislar bilan aloqa qiladi va olingan ma'lumotlarni Data Layer ichiga uzatadi.
---
# Objective
Providers quyidagi vazifalarni bajaradi.
• External Provider Integration
• Provider Selection
• Provider Standardization
• Provider Lifecycle Management
• Market Data Retrieval
• Provider Failover
---
# Layer Position
```text
External Providers
↓
Providers
↓
Historical_Data
Live_Data
↓
Data_Validation
↓
Market_Memory
```
---
# Internal Modules
```text
Providers
├── ProviderFactory
├── ProviderInterface
├── TwelveData
├── Bitget
├── ProviderLifecycle
└── ProviderFlow
```
---
# Responsibilities
Providers
✓ External API ulanishi
✓ Market Data olish
✓ Provider tanlash
✓ Provider Health Monitoring
✓ Reconnect boshqaruvi
✓ Standard Data Format yaratish
---
# Not Responsible
Providers
✗ Market Analysis
✗ Signal Generation
✗ AI Analysis
✗ Trading Decision
✗ Risk Calculation
✗ Database Management
---
# Input
Providers qabul qiladi.
• Data Request
• Connection Request
• Health Check
• Configuration
---
# Output
Providers yaratadi.
• Standard Market Data
• Provider Status
• Connection Metadata
• Provider Events
---
# Supported Providers
• Twelve Data
• Bitget
Kelajakda qo'shilishi mumkin.
• Binance
• Bybit
• Polygon
• Alpha Vantage
• Finnhub
---
# Workflow
```text
Receive Request
↓
ProviderFactory
↓
Selected Provider
↓
Retrieve Market Data
↓
ProviderFlow
↓
Historical_Data / Live_Data
```
---
# Golden Rules
1. Barcha Provider'lar ProviderInterface'ni implement qilishi shart.
2. Provider tanlash faqat ProviderFactory orqali amalga oshiriladi.
3. Provider'lar standart formatda ma'lumot qaytarishi shart.
4. Provider Failure holati ProviderLifecycle tomonidan boshqariladi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Providers/
├── README.md
├── ProviderFactory/
├── ProviderInterface/
├── TwelveData/
├── Bitget/
├── ProviderLifecycle/
├── ProviderFlow/
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
└── Layer_Contracts.md
```
---
# Summary
Providers GoldBot Data Layer ichidagi Canonical External Market Data Provider Group bo'lib, tashqi market provider'lar bilan integratsiyani, standart ma'lumot oqimini va provider lifecycle boshqaruvini ta'minlaydi.
