# Provider Interface Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ProviderInterface modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
ProviderFactory
↓
ProviderInterface
↓
Concrete Providers
```
---
# Module Architecture
```text
ProviderInterface
        │
        ├── Connection Contract
        ├── Request Contract
        ├── Response Contract
        ├── Error Contract
        ├── Lifecycle Contract
        └── Metadata Contract
```
---
# Internal Components
## Connection Contract
Provider ulanish standartini belgilaydi.
---
## Request Contract
Request formatini belgilaydi.
---
## Response Contract
Response formatini belgilaydi.
---
## Error Contract
Xatolarni qaytarish standartini belgilaydi.
---
## Lifecycle Contract
Provider Lifecycle standartini belgilaydi.
---
## Metadata Contract
Metadata formatini belgilaydi.
---
# Allowed Dependencies
✓ None
---
# Forbidden Dependencies
✗ ProviderFactory
✗ TwelveData
✗ Bitget
✗ Historical_Data
✗ Live_Data
---
# Summary
ProviderInterface barcha Market Data Provider'lari implement qilishi shart bo'lgan yagona Canonical Contract hisoblanadi.
