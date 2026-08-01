# Layer Contracts

Status: CANONICAL

---

# Purpose

Layer Contracts hujjati Data Layer uchun rasmiy arxitektura shartnomasidir (Architecture Contract).

Bu hujjat Data Layer'ning:

• chegaralarini (Boundaries)

• mas'uliyatlarini (Responsibilities)

• bog'lanishlarini (Dependencies)

• kirish va chiqishlarini (Inputs / Outputs)

• taqiqlangan bog'lanishlarini (Forbidden Dependencies)

aniq belgilaydi.

Har bir modul va har bir yangi kod ushbu hujjatga mos bo'lishi shart.

---

# Layer Responsibility

Data Layer faqat market ma'lumotlari bilan ishlaydi.

Asosiy vazifalari:

✓ Historical Data

✓ Live Data

✓ Provider Management

✓ Data Validation

✓ Market Memory

✓ Event Distribution

Data Layer hech qachon biznes logikasi yoki trading logikasini bajarmaydi.

---

# Layer Input

Data Layer quyidagi manbalardan ma'lumot qabul qiladi.

External Providers

↓

Historical Providers

↓

Live Providers

↓

Configuration Layer

---

# Layer Output

Data Layer quyidagi ma'lumotlarni taqdim etadi.

• Current Price

• OHLC Candle

• Historical Data

• Timeframe Data

• Market Memory

• Event Notifications

Consumer:

GoldBot Core

---

# Allowed Dependencies

Data Layer quyidagilar bilan ishlashi mumkin.

✓ Configuration Layer

✓ Provider Factory

✓ External Providers

✓ Historical Providers

✓ Live Providers

✓ GoldBot Core (Read Only)

---

# Forbidden Dependencies

Data Layer quyidagi qatlamlarga bog'lanishi taqiqlanadi.

✗ Context Engine

✗ Analysis Engine

✗ Strategy Engine

✗ Confluence Engine

✗ Decision Engine

✗ Risk Engine

✗ Signal Engine

✗ AI Layer

✗ Platform Layer

✗ User Experience

✗ Business Layer

✗ Learning Layer

✗ Media Layer

✗ Future Expansion

---

# Read / Write Contract

Historical Data

Write →

Data Validation

---

Live Data

Write →

Data Validation

---

Data Validation

Write →

Market Memory

---

Market Memory

Write →

Internal Storage

Read →

MemoryReader

---

GoldBot Core

Read →

MemoryReader

Write →

NOT ALLOWED

---

# Module Contracts

## Historical_Data

Input

Historical Providers

Output

Validated Historical Data

Can Write

✓ Data Validation

Cannot Access

✗ Core

✗ AI

✗ Strategy

---

## Live_Data

Input

Live Providers

Output

Validated Live Data

Can Write

✓ Data Validation

Cannot Access

✗ Core

✗ Strategy

✗ AI

---

## Data_Validation

Input

Historical Data

Live Data

Output

Validated Data

Can Write

✓ Market Memory

Cannot Access

✗ Core

✗ Strategy

---

## Market_Memory

Input

Validated Data

Output

MemoryReader

Events

Can Write

Internal Memory Only

Cannot Access

✗ Strategy

✗ Decision

✗ AI

---

## Event_System

Input

Internal Events

Output

Subscribers

Cannot Execute

✗ Trading Logic

✗ Strategy

✗ Risk

---

## Providers

Input

External APIs

Output

Historical Data

Live Data

Cannot Access

✗ Core

✗ Market Memory

✗ AI

---

# Layer Boundary

Data Layer boshlanishi

↓

Provider Factory

↓

Historical Data

↓

Live Data

↓

Validation

↓

Market Memory

↓

MemoryReader

↓

Data Layer tugashi

GoldBot Core shu nuqtadan boshlanadi.

---

# Ownership

Data Layer egalik qiladi:

✓ Raw Market Data

✓ Historical Data

✓ Live Data

✓ Current Price

✓ Candle

✓ Market Memory

✓ Data Validation

Data Layer egalik qilmaydi:

✗ Context

✗ Analysis

✗ Strategy

✗ Decision

✗ Signal

✗ Risk

✗ Trade

✗ User

---

# Layer Rules

1. Data Layer faqat ma'lumot bilan ishlaydi.

2. Data Layer hisob-kitob qilmaydi.

3. Data Layer signal yaratmaydi.

4. Data Layer AI ishlatmaydi.

5. Data Layer faqat Validation'dan o'tgan ma'lumotni saqlaydi.

6. GoldBot Core Market Memory'ga yozmaydi.

7. MemoryReader yagona o'qish interfeysi hisoblanadi.

8. Providerlar Data Layer'dan tashqariga chiqmaydi.

9. Circular Dependency qat'iyan taqiqlanadi.

10. Har qanday yangi modul ushbu Contract'ga mos bo'lishi shart.

---

# Contract Violation

Quyidagilar Architecture Violation hisoblanadi:

• Data Layer → Strategy import

• Data Layer → Decision import

• Data Layer → AI import

• Data Layer → Business import

• Data Layer → Platform import

• GoldBot Core → Market Memory Write

• Validation Skip

• Provider Direct Access to Core

• Circular Dependency

---

# Summary

Layer Contracts Data Layer uchun rasmiy arxitektura shartnomasi hisoblanadi.

Bu hujjat:

• Layer chegaralarini;

• modul mas'uliyatlarini;

• ruxsat etilgan bog'lanishlarni;

• taqiqlangan bog'lanishlarni;

• ma'lumot oqimi va egaligini;

aniq belgilaydi.

Data Layer'ga qo'shiladigan har qanday yangi modul ushbu Contract talablariga to'liq mos kelishi shart.
