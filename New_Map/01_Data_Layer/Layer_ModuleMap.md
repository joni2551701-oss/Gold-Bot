# Layer Module Map

Status: CANONICAL

---

# Purpose

Layer Module Map hujjati Data Layer tarkibidagi barcha modullar, ularning vazifalari va o'zaro bog'lanishlarini tavsiflaydi.

Bu hujjat Data Layer'ning rasmiy modul xaritasi (Module Architecture Blueprint) hisoblanadi.

Bu yerda implementatsiya emas, balki modul chegaralari va bog'lanishlari ko'rsatiladi.

---

# Data Layer Module Map

```text
                    DATA LAYER

                           │
                           ▼
                    Provider Factory
                           │
          ┌────────────────┴────────────────┐
          ▼                                 ▼
 Historical Providers               Live Providers
          │                                 │
          ▼                                 ▼
 Historical_Data                  Live_Data
          │                                 │
          └──────────────┬──────────────────┘
                         ▼
                 Data_Validation
                         │
                         ▼
                  Market_Memory
                         │
                 ┌───────┴────────┐
                 ▼                ▼
          MemoryReader        Event_System
                 │                │
                 └───────┬────────┘
                         ▼
                    GoldBot Core
```

---

# Module Dependencies

## Providers

Purpose

External market ma'lumotlarini olish.

Dependencies

None

Outputs

• Historical_Data

• Live_Data

---

## Historical_Data

Purpose

Tarixiy Candle va OHLC ma'lumotlarini tayyorlash.

Reads

• Providers

Writes

• Data_Validation

---

## Live_Data

Purpose

Realtime Tick va Current Price boshqaruvi.

Reads

• Providers

Writes

• Data_Validation

---

## Data_Validation

Purpose

Barcha ma'lumotlarni tekshirish.

Reads

• Historical_Data

• Live_Data

Writes

• Market_Memory

---

## Market_Memory

Purpose

Single Source of Truth.

Reads

• Data_Validation

Writes

None

Provides

• MemoryReader

• Event_System

---

## MemoryReader

Purpose

Market Memory'dan xavfsiz o'qish.

Reads

• Market_Memory

Writes

None

Consumers

• GoldBot Core

---

## Event_System

Purpose

Ichki Event tarqatish.

Reads

• Market_Memory

Publishes

• Events

Consumers

• GoldBot Core

---

# Layer Dependency Tree

```text
Providers

↓

Historical_Data

↓

Data_Validation

↓

Market_Memory

↓

MemoryReader

↓

GoldBot Core
```

Realtime oqimi

```text
Providers

↓

Live_Data

↓

Data_Validation

↓

Market_Memory

↓

MemoryReader

↓

GoldBot Core
```

---

# Allowed Dependencies

Providers

↓

Historical_Data

↓

Live_Data

↓

Data_Validation

↓

Market_Memory

↓

MemoryReader

↓

GoldBot Core

---

# Forbidden Dependencies

Historical_Data

✗ Context

✗ Strategy

✗ Decision

✗ AI

---

Live_Data

✗ Context

✗ Strategy

✗ Decision

✗ Risk

---

Market_Memory

✗ Context

✗ Strategy

✗ AI

---

Providers

✗ Core

✗ Application Services

✗ Business Layer

---

Data_Validation

✗ Strategy

✗ AI

✗ Decision

---

Event_System

✗ Trading Logic

✗ Strategy

✗ Risk

---

# Layer Inputs

External Providers

↓

Historical Providers

↓

Live Providers

---

# Layer Outputs

MarketMemory

↓

MemoryReader

↓

GoldBot Core

---

# Module Communication Rules

1. Historical_Data va Live_Data bir-birini chaqirmaydi.

2. Barcha ma'lumot Data_Validation orqali o'tadi.

3. Market_Memory yagona yozish nuqtasi hisoblanadi.

4. GoldBot Core faqat MemoryReader orqali ma'lumot oladi.

5. Event_System faqat Event uzatadi.

6. Providerlar faqat Data Layer bilan ishlaydi.

7. Har bir modul Single Responsibility prinsipiga amal qiladi.

8. Data Layer ichida aylana (Circular Dependency) bo'lishi taqiqlanadi.

---

# Golden Rules

• Providers ma'lumot beradi.

• Historical_Data tarixni tayyorlaydi.

• Live_Data realtime oqimni boshqaradi.

• Data_Validation ma'lumotni tekshiradi.

• Market_Memory saqlaydi.

• MemoryReader o'qiydi.

• Event_System xabar tarqatadi.

• GoldBot Core hisoblaydi.

---

# Summary

Layer Module Map Data Layer ichidagi barcha modullar va ularning bog'lanishlarini rasmiy ravishda belgilaydi.

Har bir modul faqat o'z vazifasini bajaradi va faqat ruxsat etilgan yo'nalish bo'yicha boshqa modullar bilan ishlaydi.

Bu hujjat Data Layer uchun Canonical Module Blueprint hisoblanadi.
