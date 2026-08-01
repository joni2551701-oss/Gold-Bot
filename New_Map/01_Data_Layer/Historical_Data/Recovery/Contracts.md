# Recovery Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat Recovery modulining rasmiy Architecture Contract hujjati hisoblanadi.

Recovery moduliga qo'shiladigan har qanday implementatsiya ushbu Contract talablariga to'liq mos bo'lishi shart.

Recovery modulining yagona vazifasi Historical Data ichidagi yetishmayotgan yoki buzilgan ma'lumotlarni tiklashdir.

---

# Module Responsibility

Recovery quyidagi vazifalar uchun javobgar:

✓ Gap Detection

✓ Missing Data Recovery

✓ Historical Synchronization

✓ Recovery Planning

✓ Recovery Execution

✓ Recovery Validation

✓ Recovery Status Management

Recovery quyidagi vazifalarni bajarmaydi:

✗ Initial Bootstrap

✗ Live Streaming

✗ Current Price Management

✗ Candle Building

✗ Market Analysis

✗ Trading Strategy

✗ Decision Making

✗ Risk Management

✗ Signal Generation

---

# Module Boundary

Recovery boshlanishi

↓

Recovery Request

↓

Gap Detection

↓

Recovery Planning

↓

Historical Provider

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

Recovery tugashi

---

# Input Contract

Recovery quyidagilarni qabul qiladi:

• Recovery Request

• Symbol

• Timeframe

• Missing Time Range

• Historical Provider

• Recovery Configuration

---

# Output Contract

Recovery quyidagilarni yaratadi:

• Recovered Historical Data

• Recovery Status

• Updated Historical Database

• Updated Market Memory

• Recovery Events

---

# Read Contract

Recovery quyidagi komponentlardan o'qishi mumkin:

✓ HistoricalDataService

✓ Historical Database

✓ Historical Provider

✓ Recovery Configuration

✓ Market Memory (Read Only)

---

# Write Contract

Recovery quyidagi komponentlarga yozishi mumkin:

✓ Historical Database

✓ Data Validation

✓ Market Memory

✓ Event Bus

---

# Allowed Dependencies

Recovery quyidagilar bilan ishlashi mumkin:

✓ HistoricalDataService

✓ Historical Provider

✓ Historical Database

✓ Data Validation

✓ Market Memory

✓ Event Bus

✓ Configuration Layer

---

# Forbidden Dependencies

Recovery quyidagilar bilan ishlashi mumkin emas:

✗ Live_Data

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

✗ User Experience Layer

✗ Business Layer

✗ Learning Layer

✗ Media Layer

✗ Future Expansion Layer

---

# Ownership

Recovery egalik qiladi:

✓ Gap Detection

✓ Missing Data Recovery

✓ Recovery Planning

✓ Recovery Execution

✓ Recovery State

✓ Retry Logic

Recovery egalik qilmaydi:

✗ Historical Bootstrap

✗ Live Market Data

✗ Current Price

✗ Market Context

✗ Technical Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Trading

---

# State Contract

Recovery quyidagi holatlarda bo'lishi mumkin:

• Idle

• Requested

• Running

• Detecting Gaps

• Downloading

• Validating

• Updating Memory

• Completed

• Failed

---

# Error Contract

Recovery quyidagi xatolarni qaytarishi mumkin:

• ProviderUnavailable

• ConnectionFailed

• DownloadFailed

• ValidationFailed

• DatabaseError

• MemoryUpdateFailed

• RecoveryTimeout

Har qanday xato HistoricalDataService tomonidan boshqariladi.

---

# Runtime Contract

1. Recovery faqat HistoricalDataService tomonidan ishga tushiriladi.

2. Recovery Bootstrap jarayonidan mustaqil ishlaydi.

3. Recovery faqat Missing Data mavjud bo'lsa ishlaydi.

4. Recovery faqat yetishmayotgan ma'lumotlarni yuklaydi.

5. Recovery mavjud ma'lumotlarni qayta yuklamaydi.

6. Validation majburiy.

7. Validation muvaffaqiyatsiz bo'lsa Recovery bekor qilinadi.

8. Recovery tugagandan keyin Market Memory yangilanadi.

9. Recovery yakunida Event Bus hodisa yuboradi.

10. Recovery GoldBot Core bilan to'g'ridan-to'g'ri ishlamaydi.

---

# Architecture Rules

Recovery:

✓ Historical Data bilan ishlaydi.

✓ Historical Provider orqali ma'lumot oladi.

✓ Validation orqali ishlaydi.

✓ Market Memory'ni yangilaydi.

✓ Event Bus orqali natijani bildiradi.

Recovery:

✗ Trading qilmaydi.

✗ Signal yaratmaydi.

✗ Decision chiqarmaydi.

✗ AI ishlatmaydi.

✗ Risk hisoblamaydi.

✗ Context hisoblamaydi.

✗ Live Stream'ni boshqarmaydi.

---

# Contract Violations

Quyidagilar Architecture Violation hisoblanadi:

• Recovery → Live_Data import

• Recovery → Context import

• Recovery → Strategy import

• Recovery → Decision import

• Recovery → AI import

• Recovery → Business Layer import

• Validation Skip

• Direct Market Memory Write (Validation'siz)

• Bootstrap Logic inside Recovery

• Circular Dependency

---

# Acceptance Criteria

Recovery moduli to'g'ri ishlaydi agar:

✓ Missing Data to'g'ri aniqlansa.

✓ Faqat yetishmayotgan ma'lumot yuklansa.

✓ Validation majburiy bajarilsa.

✓ Historical Database yangilansa.

✓ Market Memory yangilansa.

✓ Recovery Status qaytarilsa.

✓ Event Bus RecoveryCompleted yoki RecoveryFailed hodisasini yuborsa.

---

# Summary

Recovery Contract Recovery modulining rasmiy arxitektura shartnomasidir.

Recovery faqat tarixiy ma'lumotlardagi bo'shliqlarni aniqlash va tiklash uchun javobgardir.

Ushbu hujjatda belgilangan chegaralar, bog'lanishlar va qoidalardan chetga chiqish GoldBot Architecture Violation hisoblanadi.
