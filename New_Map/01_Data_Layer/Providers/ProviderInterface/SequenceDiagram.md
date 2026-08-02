# Provider Interface Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat ProviderInterface qanday qo'llanilishini tavsiflaydi.

---

# Runtime Sequence

```text
ProviderFactory
↓
Provider Instance Yaratiladi
↓
ProviderInterface Metodlari Chaqiriladi (connect, fetch, subscribe)
↓
Provider (TwelveData / Bitget) O'z Implementatsiyasini Bajaradi
```

---

# Runtime Rules

1. Har bir chaqiruv ProviderInterface orqali amalga oshadi.
2. ProviderFactory faqat Interface metodlarini biladi, provider ichki detallarini bilmaydi.

---

# State Flow

```text
Idle
↓
Interface Chaqirilmoqda
↓
Provider Implementatsiyasi Bajarilmoqda
↓
Natija Qaytarilmoqda
```

---

# Summary

ProviderFactory
↓
ProviderInterface
↓
Provider Implementatsiyasi
