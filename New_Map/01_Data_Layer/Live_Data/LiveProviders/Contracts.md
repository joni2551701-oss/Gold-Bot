# LiveProviders Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat LiveProviders modulining rasmiy Architecture Contract hujjati hisoblanadi.

LiveProviders Live Data modulining yagona Canonical External Market Data Integration komponentidir.

Tashqi Exchange yoki Market Data Provider bilan barcha ulanishlar faqat ushbu modul orqali amalga oshiriladi.

Har qanday implementatsiya ushbu Contract talablariga to'liq mos bo'lishi shart.

---

# Module Responsibility

LiveProviders quyidagi vazifalar uchun javobgar.

✓ Provider Connection Management

✓ Provider Authentication

✓ Provider Session Management

✓ Symbol Subscription

✓ Live Tick Receiving

✓ Provider Health Monitoring

✓ Provider Failover

✓ Connection Recovery

✓ Provider Event Publishing

LiveProviders quyidagi vazifalarni bajarmaydi.

✗ Current Price Generation

✗ Tick Validation

✗ Candle Generation

✗ Historical Data

✗ Historical Storage

✗ Market Calendar

✗ Market Memory

✗ Context Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal Generation

✗ AI Analysis

---

# Module Boundary

Configuration Layer

↓

PriceStreamService

↓

LiveProviders

↓

Exchange APIs

↓

Boundary End

---

# Input Contract

LiveProviders quyidagilarni qabul qiladi.

• Provider Configuration

• Connection Request

• Authentication Credentials

• Subscription Request

• Symbol List

• Reconnect Request

---

# Output Contract

LiveProviders quyidagilarni yaratadi.

• Live Tick

• Provider Event

• Provider Status

• Connection Status

• Health Status

• Authentication Status

---

# Read Contract

LiveProviders quyidagilarni o'qishi mumkin.

✓ Configuration Layer

✓ Provider Configuration

✓ API Credentials

✓ Subscription Configuration

✓ Exchange Metadata

---

# Write Contract

LiveProviders quyidagilarga yozishi mumkin.

✓ PriceStreamService

✓ Event Bus

Boshqa modullarga yozish taqiqlanadi.

---

# Allowed Dependencies

LiveProviders quyidagilar bilan ishlashi mumkin.

✓ PriceStreamService

✓ Provider Factory

✓ Exchange APIs

✓ Event Bus

✓ Configuration Layer

---

# Forbidden Dependencies

LiveProviders quyidagilar bilan ishlashi mumkin emas.

✗ Historical Data

✗ HistoricalDatabase

✗ HistoricalDataService

✗ CurrentPriceProvider

✗ StreamValidator

✗ CandleBuilder

✗ Market Memory

✗ Memory Reader

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

LiveProviders egalik qiladi.

✓ Provider Connections

✓ Provider Authentication

✓ Provider Sessions

✓ Symbol Subscriptions

✓ Provider Health

✓ Provider Metadata

✓ Connection State

✓ Failover State

LiveProviders egalik qilmaydi.

✗ Current Price

✗ Tick Validation

✗ Candle

✗ Market Memory

✗ Trading Logic

✗ Strategy

✗ Decision

---

# State Contract

LiveProviders quyidagi holatlarda bo'lishi mumkin.

• Idle

• Loading Configuration

• Connecting

• Authenticating

• Connected

• Subscribing

• Streaming

• Reconnecting

• Failover

• Disconnected

• Failed

---

# Error Contract

LiveProviders quyidagi xatolarni qaytarishi mumkin.

• ConnectionFailed

• AuthenticationFailed

• SubscriptionFailed

• ProviderUnavailable

• ProviderDisconnected

• HeartbeatTimeout

• ReconnectFailed

• FailoverFailed

• InvalidProviderConfiguration

• UnknownProviderError

Har qanday xato PriceStreamService tomonidan boshqariladi va Event Bus orqali e'lon qilinadi.

---

# Runtime Contract

1. LiveProviders faqat PriceStreamService tomonidan boshqariladi.

2. Har bir Provider ulanishidan oldin autentifikatsiyadan o'tishi shart.

3. Streaming faqat Subscription muvaffaqiyatli yakunlangandan keyin boshlanadi.

4. Har bir Tick o'zgartirilmasdan uzatiladi.

5. Tick Validation LiveProviders ichida bajarilmaydi.

6. Provider uzilganda avtomatik Reconnect yoki Failover ishga tushadi.

7. Provider Health doim monitoring qilinadi.

8. LiveProviders faqat PriceStreamService bilan muloqot qiladi.

9. LiveProviders GoldBot Core bilan bevosita ishlamaydi.

10. Trading Logic bajarilishi qat'iyan taqiqlanadi.

---

# Architecture Rules

LiveProviders:

✓ Provider ulanishini boshqaradi.

✓ Authentication bajaradi.

✓ Symbol Subscription'ni boshqaradi.

✓ Live Tick qabul qiladi.

✓ Provider Health monitoringini bajaradi.

✓ Failover va Recovery boshqaradi.

✓ Tick'larni PriceStreamService'ga uzatadi.

LiveProviders:

✗ Current Price yaratmaydi.

✗ Tick Validation bajarmaydi.

✗ Candle yaratmaydi.

✗ Market Memory'ga yozmaydi.

✗ Trading qilmaydi.

✗ Strategy hisoblamaydi.

✗ Signal yaratmaydi.

✗ Decision chiqarmaydi.

✗ AI ishlatmaydi.

---

# Contract Violations

Quyidagilar Architecture Violation hisoblanadi.

• LiveProviders → Historical Data import

• LiveProviders → CurrentPriceProvider import

• LiveProviders → StreamValidator import

• LiveProviders → CandleBuilder import

• LiveProviders → Market Memory import

• LiveProviders → Context Engine import

• LiveProviders → Strategy Engine import

• LiveProviders → Decision Engine import

• LiveProviders → AI Layer import

• LiveProviders → Business Layer import

• Current Price yaratish

• Tick Validation bajarish

• Candle yaratish

• Market Memory'ga yozish

• Circular Dependency

---

# Acceptance Criteria

LiveProviders to'g'ri ishlaydi agar:

✓ Provider bilan ulanish muvaffaqiyatli amalga oshsa.

✓ Authentication muvaffaqiyatli yakunlansa.

✓ Symbol Subscription ishlasa.

✓ Live Tick uzluksiz qabul qilinsa.

✓ Tick o'zgartirilmasdan PriceStreamService'ga uzatilsa.

✓ Connection Health monitoringi ishlasa.

✓ Reconnect va Failover muvaffaqiyatli ishlasa.

✓ Arxitektura chegaralari buzilmasa.

---

# Summary

LiveProviders Contract Live Data modulidagi External Market Data Integration komponentining rasmiy arxitektura shartnomasi hisoblanadi.

LiveProviders tashqi Exchange va Market Data Provider'lar bilan ishlovchi yagona Canonical modul hisoblanadi.

Ushbu hujjatda belgilangan Boundary, Dependency, Runtime va Ownership qoidalaridan chetga chiqadigan har qanday implementatsiya **GoldBot Architecture Violation** hisoblanadi.
