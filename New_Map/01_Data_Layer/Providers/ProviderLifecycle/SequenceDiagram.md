# Provider Lifecycle Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat ProviderLifecycle Runtime Sequence'ni tavsiflaydi.

---

# Startup Sequence

```text
ProviderFactory
↓
Provider Instance Yaratildi
↓
ProviderLifecycle
↓
Connect
↓
Health Check
↓
Ready
```

---

# Reconnect Sequence

```text
Connection Lost
↓
ProviderLifecycle
↓
Detect Failure
↓
Retry Connect
↓
Health Check
↓
Ready
```

---

# Shutdown Sequence

```text
Shutdown So'rovi
↓
ProviderLifecycle
↓
Disconnect
↓
Idle
```

---

# Runtime Rules

1. Har bir Provider Startup Health Check bilan yakunlanadi.
2. Ulanish uzilishi avtomatik Reconnect'ni ishga tushiradi.
3. Shutdown har doim Disconnect bilan yakunlanadi.

---

# Summary

Provider Instance
↓
ProviderLifecycle
↓
Ready / Reconnecting / Idle
