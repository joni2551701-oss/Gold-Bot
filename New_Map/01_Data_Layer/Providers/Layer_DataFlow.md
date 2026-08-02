# Providers Layer Data Flow
Status: CANONICAL
---
# Purpose
Ushbu hujjat Providers Group ichidagi barcha Provider modullari o'rtasidagi Data Flow'ni tavsiflaydi.
Providers tashqi Market Data Provider'lardan ma'lumot olib, standart oqim orqali Data Layer ichiga uzatadi.
---
# Data Flow
```text
Data Request
        │
        ▼
ProviderFactory
        │
        ▼
ProviderInterface
        │
        ├──────────────┐
        ▼              ▼
   TwelveData      Bitget
        │              │
        └──────┬───────┘
               ▼
      ProviderLifecycle
               │
               ▼
         ProviderFlow
               │
        ┌──────┴──────┐
        ▼             ▼
Historical_Data   Live_Data
```
---
# Input
• Data Request
• Provider Configuration
• Connection Event
---
# Output
• Historical Market Data
• Live Market Data
• Provider Events
• Provider Status
---
# Data Flow Rules
1. Provider faqat ProviderFactory orqali yaratiladi.
2. Har bir Provider ProviderInterface'ni implement qiladi.
3. Barcha ma'lumotlar ProviderFlow orqali uzatiladi.
4. ProviderLifecycle Provider holatini nazorat qiladi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Summary
Providers Group tashqi Provider'lardan Market Data olib, standart Data Pipeline orqali Historical_Data va Live_Data modullariga uzatadi.
