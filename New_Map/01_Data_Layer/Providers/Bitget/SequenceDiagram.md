# Bitget Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat Bitget Runtime Sequence'ni tavsiflaydi.

---

# Runtime Sequence

```text
LiveProviders Subscription So'rovi
↓
ProviderInterface
↓
Bitget
↓
WebSocket Ulanish
↓
Tick Stream Qabul Qilinadi
↓
LiveProviders'ga Uzatiladi
```

---

# Runtime Rules

1. Subscription Symbol bilan birga kelishi shart.
2. Bitget ProviderInterface Contract'iga mos Tick qaytaradi.
3. Ulanish uzilganda ProviderLifecycle Reconnect'ni boshqaradi.

---

# State Flow

```text
Idle
↓
Connecting
↓
Subscribed
↓
Streaming
↓
Disconnected (agar ulanish uzilsa)
```

---

# Summary

LiveProviders
↓
Bitget
↓
Live Tick / Current Price
