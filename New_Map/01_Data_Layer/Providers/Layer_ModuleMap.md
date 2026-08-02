# Providers Layer Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat Providers bo'limi tarkibidagi barcha modullar, ularning vazifalari va o'zaro bog'lanishlarini tavsiflaydi.

Bu hujjat Providers bo'limining rasmiy modul xaritasi (Module Architecture Blueprint) hisoblanadi.

---

# Providers Module Map

```text
                ProviderFactory
                        │
                        ▼
                ProviderInterface
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
     TwelveData                   Bitget
          │                           │
          └─────────────┬─────────────┘
                         ▼
                ProviderLifecycle
                         │
                         ▼
                  ProviderFlow
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
 Historical_Data                  Live_Data
```

---

# Module Dependencies

## ProviderFactory

Purpose

Barcha provider'larni yaratish va boshqarish.

Dependencies

• Configuration

Outputs

• ProviderInterface Instance

---

## ProviderInterface

Purpose

Barcha provider'lar uchun yagona standart Contract.

Dependencies

None

Implemented By

• TwelveData
• Bitget

---

## TwelveData

Purpose

Historical market ma'lumotlarini taqdim etish.

Reads

• External TwelveData API

Writes

• ProviderFlow (Historical Route)

---

## Bitget

Purpose

Live market ma'lumotlarini taqdim etish.

Reads

• External Bitget WebSocket

Writes

• ProviderFlow (Live Route)

---

## ProviderLifecycle

Purpose

Provider'larning ishga tushirish, qayta ulanish va to'xtatish jarayonlarini boshqarish.

Reads

• TwelveData
• Bitget

Writes

• Health Report

---

## ProviderFlow

Purpose

Historical va Live oqimlarni tegishli modullarga yo'naltirish.

Reads

• TwelveData
• Bitget

Writes

• Historical_Data
• Live_Data

---

# Allowed Dependencies

```text
ProviderFactory
        │
        ▼
ProviderInterface
        │
        ▼
TwelveData / Bitget
        │
        ▼
ProviderLifecycle
        │
        ▼
ProviderFlow
```

---

# Forbidden Dependencies

Providers

✗ Core
✗ Application Services
✗ Business Layer
✗ Data_Validation (to'g'ridan-to'g'ri)
✗ Market_Memory (to'g'ridan-to'g'ri)

---

# Module Communication Rules

1. TwelveData va Bitget bir-birini chaqirmaydi.
2. Barcha provider ProviderInterface orqali ishlaydi.
3. ProviderLifecycle barcha provider ulanishlarini boshqaradi.
4. ProviderFlow Historical va Live oqimlarni aralashtirmaydi.
5. Providers ichida Circular Dependency taqiqlanadi.

---

# Summary

Providers Layer Module Map bo'lim ichidagi barcha modullar va ularning bog'lanishlarini rasmiy ravishda belgilaydi.

Har bir modul faqat o'z vazifasini bajaradi va faqat ruxsat etilgan yo'nalish bo'yicha boshqa modullar bilan ishlaydi.
