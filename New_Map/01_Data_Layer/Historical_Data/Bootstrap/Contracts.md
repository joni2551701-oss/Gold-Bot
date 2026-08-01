# Bootstrap Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat Bootstrap modulining rasmiy Architecture Contract hujjati hisoblanadi.

Bootstrap moduliga qo'shiladigan har qanday kod ushbu Contract talablariga mos bo'lishi shart.

---

# Module Responsibility

Bootstrap faqat tizim ishga tushganda Historical Data yuklaydi.

Asosiy vazifalari:

✓ Initial Historical Loading

✓ Bootstrap Initialization

✓ Historical Synchronization

✓ Market Memory Initialization

Bootstrap biznes logikasi yoki trading logikasini bajarmaydi.

---

# Module Boundary

Bootstrap boshlanishi

↓

Configuration

↓

HistoricalDataService

↓

Bootstrap

↓

Historical Provider

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

Bootstrap tugashi

---

# Input Contract

Bootstrap quyidagilarni qabul qiladi:

• Configuration

• Symbols

• Timeframes

• Historical Provider

• Bootstrap Settings

---

# Output Contract

Bootstrap quyidagilarni yaratadi:

• Historical Candle

• Historical OHLC

• Bootstrap Status

• Initialized Market Memory

---

# Read Contract

Bootstrap o'qishi mumkin:

✓ Configuration

✓ Provider Factory

✓ Historical Provider

✓ Historical Database

---

# Write Contract

Bootstrap yozishi mumkin:

✓ Historical Database

✓ Data Validation

✓ Market Memory

---

# Allowed Dependencies

Bootstrap quyidagilar bilan ishlashi mumkin:

✓ Configuration

✓ HistoricalDataService

✓ Provider Factory

✓ Historical Provider

✓ Historical Database

✓ Data Validation

✓ Market Memory

---

# Forbidden Dependencies

Bootstrap quyidagilar bilan ishlashi mumkin emas:

✗ Live Data

✗ CurrentPriceProvider

✗ CandleBuilder

✗ Context Engine

✗ Analysis Engine

✗ Strategy Engine

✗ Confluence Engine

✗ Decision Engine

✗ Risk Engine

✗ Signal Engine

✗ AI Layer

✗ Platform Layer

✗ Business Layer

✗ Learning Layer

✗ Media Layer

---

# Ownership

Bootstrap egalik qiladi:

✓ Initial Historical Loading

✓ Bootstrap State

✓ Startup Synchronization

Bootstrap egalik qilmaydi:

✗ Live Stream

✗ Current Price

✗ Market Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal

✗ Trade

---

# State Contract

Bootstrap quyidagi holatlarda bo'lishi mumkin:

• Idle

• Starting

• Downloading

• Validating

• Initializing Memory

• Completed

• Failed

---

# Error Contract

Bootstrap quyidagi xatolarni qaytarishi mumkin:

• ProviderUnavailable

• DownloadFailed

• ValidationFailed

• DatabaseError

• MemoryInitializationFailed

Har qanday xato HistoricalDataService tomonidan boshqariladi.

---

# Runtime Contract

1. Bootstrap faqat bir marta ishga tushadi.

2. Bootstrap tugamaguncha Live Data boshlanmaydi.

3. Validation majburiy.

4. Validation o'tmagan ma'lumot Market Memory'ga yozilmaydi.

5. Bootstrap tugagandan keyin boshqaruv HistoricalDataService'ga qaytadi.

---

# Architecture Rules

Bootstrap:

✓ Historical Data bilan ishlaydi.

✓ Startup jarayonida ishlaydi.

✓ Provider orqali ma'lumot oladi.

✓ Validation orqali o'tadi.

✓ Market Memory'ni tayyorlaydi.

Bootstrap:

✗ Trading qilmaydi.

✗ Signal yaratmaydi.

✗ Decision chiqarmaydi.

✗ AI ishlatmaydi.

✗ Risk hisoblamaydi.

✗ Context hisoblamaydi.

---

# Contract Violations

Quyidagilar Architecture Violation hisoblanadi:

• Bootstrap → Strategy import

• Bootstrap → Decision import

• Bootstrap → AI import

• Bootstrap → Business import

• Bootstrap → Live Data import

• Validation Skip

• Direct Memory Write (Validation'siz)

• Circular Dependency

---

# Summary

Bootstrap Contract Bootstrap modulining rasmiy arxitektura shartnomasidir.

Bootstrap faqat tizim ishga tushganda tarixiy ma'lumotlarni yuklash va Market Memory'ni boshlang'ich holatga tayyorlash uchun javobgardir.

Ushbu hujjatda belgilangan chegaralar va qoidalardan chetga chiqish Architecture Violation hisoblanadi.
