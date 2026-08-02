# Providers Layer Module Map
Status: CANONICAL
---
# Module Architecture
```text
Providers
│
├── ProviderFactory
│
├── ProviderInterface
│
├── TwelveData
│
├── Bitget
│
├── ProviderLifecycle
│
└── ProviderFlow
```
---
# Processing Pipeline
```text
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
# Module Responsibilities
## ProviderFactory
Provider yaratadi va tanlaydi.
---
## ProviderInterface
Yagona Contract.
---
## TwelveData
Twelve Data Provider.
---
## Bitget
Bitget Provider.
---
## ProviderLifecycle
Provider holatini boshqaradi.
---
## ProviderFlow
Provider Data Flow'ni marshrutlaydi.
---
# Summary
Providers Group GoldBot Data Layer ichidagi barcha tashqi Market Data Provider'larni boshqaruvchi Canonical modul guruhi hisoblanadi.
