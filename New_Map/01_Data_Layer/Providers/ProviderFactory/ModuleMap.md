# Provider Factory Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ProviderFactory modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Data Request
↓
ProviderFactory
↓
ProviderInterface
↓
Concrete Providers
```
---
# Module Architecture
```text
ProviderFactory
        │
        ├── Configuration Loader
        ├── Provider Registry
        ├── Provider Selector
        ├── Instance Creator
        ├── Initialization Manager
        └── Metadata Generator
```
---
# Internal Components
## Configuration Loader
Provider konfiguratsiyasini yuklaydi.
---
## Provider Registry
Ro'yxatdan o'tgan Provider'larni saqlaydi.
---
## Provider Selector
Mos Provider'ni tanlaydi.
---
## Instance Creator
Provider obyektini yaratadi.
---
## Initialization Manager
Provider'ni ishga tayyorlaydi.
---
## Metadata Generator
Provider Metadata yaratadi.
---
# Allowed Dependencies
✓ ProviderInterface
✓ ProviderLifecycle
---
# Forbidden Dependencies
✗ TwelveData
✗ Bitget
✗ Historical_Data
✗ Live_Data
---
# Summary
ProviderFactory Provider yaratish va boshqarish uchun Canonical Factory Pattern modulidir.
