# Provider Interface Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ProviderInterface Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
ProviderFactory
↓
ProviderInterface
↓
Concrete Provider
↓
Contract Validation
↓
Provider Ready
```
---
# Runtime Rules
1. Har bir Provider Interface'ni implement qilishi shart.
2. Contract Validation muvaffaqiyatli o'tishi shart.
3. Factory faqat Interface orqali Provider bilan ishlashi shart.
---
# State Flow
```text
Defined
↓
Implemented
↓
Validated
↓
Ready
```
---
# Summary
ProviderFactory
↓
ProviderInterface
↓
Concrete Provider
