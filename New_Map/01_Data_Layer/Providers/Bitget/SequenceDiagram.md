# Bitget Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Bitget Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
ProviderFactory
↓
ProviderInterface
↓
Bitget
↓
Connect API
↓
Request Market Data
↓
Receive Response
↓
Standardize Response
↓
Return Data
```
---
# Runtime Rules
1. ProviderFactory orqali yaratilishi shart.
2. ProviderInterface implement qilinishi shart.
3. API Response standartlashtirilishi shart.
4. Error holatlari Contract bo'yicha qaytarilishi shart.
---
# State Flow
```text
Idle
↓
Connecting
↓
Requesting
↓
Receiving
↓
Formatting
↓
Completed
```
---
# Summary
ProviderFactory
↓
Bitget
↓
Historical_Data / Live_Data
