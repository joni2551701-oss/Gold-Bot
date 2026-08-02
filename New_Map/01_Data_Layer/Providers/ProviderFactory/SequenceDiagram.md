# Provider Factory Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat ProviderFactory Runtime Sequence'ni tavsiflaydi.

---

# Runtime Sequence

```text
Configuration
↓
ProviderFactory
↓
Provider Turi Aniqlanadi
↓
Provider Instance Yaratiladi
↓
ProviderInterface orqali Registratsiya
↓
Historical_Data / Live_Data'ga Uzatiladi
```

---

# Runtime Rules

1. Configuration mavjud bo'lishi shart.
2. Provider turi (Historical / Live) aniqlanishi shart.
3. Yaratilgan provider ProviderInterface'ga mos bo'lishi shart.
4. Provider Registry'ga qayd etilishi shart.

---

# State Flow

```text
Idle
↓
Reading Configuration
↓
Creating Provider
↓
Registering
↓
Ready
```

---

# Summary

Configuration
↓
ProviderFactory
↓
Provider Instance
