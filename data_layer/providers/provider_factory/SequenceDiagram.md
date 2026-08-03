# Provider Factory Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ProviderFactory Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Data Request
↓
ProviderFactory
↓
Read Configuration
↓
Select Provider
↓
Create Provider
↓
Initialize Provider
↓
Return Provider Instance
```
---
# Runtime Rules
1. Provider Request mavjud bo'lishi shart.
2. Provider Configuration o'qilishi shart.
3. Faqat ro'yxatdan o'tgan Provider yaratilishi mumkin.
4. ProviderInterface qaytarilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Selecting
↓
Creating
↓
Initializing
↓
Completed
```
---
# Summary
Provider Request
↓
ProviderFactory
↓
Provider Instance
