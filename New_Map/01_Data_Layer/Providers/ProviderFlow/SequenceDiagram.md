# Provider Flow Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat ProviderFlow Runtime Sequence'ni tavsiflaydi.

---

# Historical Flow Sequence

```text
TwelveData
↓
ProviderInterface
↓
ProviderFlow
↓
HistoricalProviders (Historical_Data)
```

---

# Live Flow Sequence

```text
Bitget
↓
ProviderInterface
↓
ProviderFlow
↓
LiveProviders (Live_Data)
```

---

# Runtime Rules

1. Historical va Live oqim alohida yo'naltiriladi.
2. Har ikkala oqim ham ProviderInterface orqali standartlashtiriladi.
3. ProviderFlow oqimlarni aralashtirmaydi.

---

# Summary

TwelveData / Bitget
↓
ProviderFlow
↓
Historical_Data / Live_Data
