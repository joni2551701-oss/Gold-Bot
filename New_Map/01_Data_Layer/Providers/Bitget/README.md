# Bitget
Status: CANONICAL
---
# Purpose
Bitget GoldBot Data Layer ichidagi Canonical Market Data Provider moduli hisoblanadi.
Uning asosiy vazifasi Bitget API orqali Market Data olish va uni GoldBot ProviderInterface standartiga mos formatda taqdim etishdir.
Bitget Market Analysis bajarmaydi.
Bitget Signal yaratmaydi.
Bitget faqat Market Data Provider hisoblanadi.
---
# Objective
Bitget quyidagi vazifalarni bajaradi.
• API Connection
• Historical Data Retrieval
• Live Market Data Retrieval
• Provider Health Check
• Response Standardization
• Error Handling
---
# Layer Position
```text
ProviderFactory
↓
ProviderInterface
↓
Bitget
↓
Historical_Data
Live_Data
```
---
# Responsibilities
Bitget
✓ Bitget API bilan bog'lanadi
✓ Historical Data oladi
✓ Live Market Data oladi
✓ Standard Response qaytaradi
✓ Connection Status kuzatadi
---
# Not Responsible
Bitget
✗ Provider Selection
✗ Data Validation
✗ Market Analysis
✗ Signal Generation
✗ Trading Decision
---
# Input
Bitget qabul qiladi.
• Provider Request
• Symbol
• Timeframe
• Data Request
---
# Output
Bitget yaratadi.
• Standard Market Data
• Provider Status
• Response Metadata
• Error Response
---
# Supported Features
• Historical OHLCV
• Live Price
• Multi Timeframe
• Symbol Search
• Health Check
---
# Workflow
```text
Receive Request
↓
Connect API
↓
Request Market Data
↓
Receive Response
↓
Standardize Response
↓
Return Market Data
```
---
# Golden Rules
1. Bitget ProviderInterface'ni implement qilishi shart.
2. Response standart formatda qaytarilishi shart.
3. API xatolari Error Contract bo'yicha qaytarilishi shart.
4. Business Logic bajarilmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Bitget/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Bitget GoldBot Data Layer ichidagi Canonical Market Data Provider bo'lib, Bitget API orqali Market Data olib, ProviderInterface standartiga mos ravishda tizimga uzatadi.
