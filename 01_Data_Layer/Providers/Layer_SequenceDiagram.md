# Providers Layer Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Providers Group Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Data Request
↓
ProviderFactory
↓
ProviderInterface
↓
Concrete Provider
↓
ProviderLifecycle
↓
ProviderFlow
↓
Historical_Data / Live_Data
```
---
# Runtime Rules
1. ProviderFactory Provider yaratadi.
2. ProviderInterface Contract tekshiriladi.
3. Concrete Provider API bilan ishlaydi.
4. ProviderLifecycle ulanishni nazorat qiladi.
5. ProviderFlow ma'lumotni marshrutlaydi.
---
# State Flow
```text
Idle
↓
Creating
↓
Connecting
↓
Receiving
↓
Monitoring
↓
Routing
↓
Completed
```
---
# Summary
ProviderFactory
↓
Concrete Provider
↓
ProviderFlow
↓
Historical_Data / Live_Data
