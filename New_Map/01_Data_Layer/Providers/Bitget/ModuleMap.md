# Bitget Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat Bitget modulining ichki tuzilishini tavsiflaydi.

---

# Module Position

```text
ProviderFactory
↓
Bitget (ProviderInterface orqali)
↓
LiveProviders
```

---

# Module Architecture

```text
Bitget
        │
        ├── WebSocket Connection
        ├── Subscription Manager
        ├── Tick Receiver
        └── Response Mapper
```

---

# Internal Components

## WebSocket Connection
Bitget WebSocket serveriga ulanishni boshqaradi.

---

## Subscription Manager
Symbol bo'yicha obunalarni boshqaradi.

---

## Tick Receiver
Kelayotgan Tick ma'lumotlarini qabul qiladi.

---

## Response Mapper
Bitget javobini ProviderInterface formatiga o'giradi.

---

# Allowed Dependencies

✓ ProviderInterface

---

# Forbidden Dependencies

✗ Data_Validation
✗ Market_Memory
✗ Historical_Data
✗ Context
✗ Strategy

---

# Summary

Bitget Providers bo'limidagi Live Data uchun tashqi integratsiya nuqtasi hisoblanadi.
