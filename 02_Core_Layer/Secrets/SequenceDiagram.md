# Secrets Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Secrets Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Secrets modulining Canonical Runtime Blueprint hisoblanadi.
---
# Startup Sequence
```text
GoldBot Start
↓
Secrets
↓
Read Environment / Secret Store
↓
Wrap as MaskedSecret
↓
SecretValidator (majburiy qiymatlarni tekshirish)
↓
Secrets Ready
↓
Configuration
```
---
# Runtime Request Sequence
```text
Module Secret Request
↓
Secrets
↓
SecretRegistry (kalitni aniqlash)
↓
MaskedSecret qaytariladi
↓
Module (kerak bo'lsa reveal() chaqiradi)
```
---
# Rotation Sequence
```text
Rotation Request
↓
SecretRotation
↓
Read New Secret Value
↓
Validate New Value
↓
Atomic Replace
↓
Notify Dependent Providers
↓
Secrets Ready
```
---
# Failure Sequence
```text
Majburiy Secret topilmadi
↓
SecretValidator Fail
↓
Log Error (qiymatsiz — faqat kalit nomi)
↓
Runtime boshlanmaydi (fail fast)
```
```text
Ixtiyoriy Secret topilmadi
↓
None qaytariladi
↓
Tegishli Provider "disabled" holatiga o'tadi
↓
Runtime davom etadi (fail safe)
```
---
# Runtime Rules
1. Secrets Configuration'dan oldin yuklanadi.
2. Majburiy qiymat yetishmasa Runtime boshlanmaydi.
3. Ixtiyoriy qiymat yetishmasa Provider "disabled" bo'ladi, Runtime davom etadi.
4. Xatolik log'ida faqat kalit nomi ko'rsatiladi — qiymat hech qachon yozilmaydi.
5. Rotation Runtime'ni to'xtatmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# State Flow
```text
Unloaded
↓
Loading
↓
Loaded
↓
Validated
↓
Ready
     │
     ├──→ Rotating ──→ Ready
     │
     └──→ Failed (majburiy qiymat yetishmasa)
```
---
# Summary
Environment
↓
Secrets
↓
Configuration
