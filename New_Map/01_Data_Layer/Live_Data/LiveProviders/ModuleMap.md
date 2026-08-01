# LiveProviders Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat LiveProviders modulining ichki arxitekturasini, komponentlarini va boshqa modullar bilan bog'lanishini tavsiflaydi.

LiveProviders Live Data modulidagi yagona Canonical External Market Data Integration komponenti hisoblanadi.

Bu implementatsiya emas.

Bu LiveProviders modulining Canonical Architecture Blueprint hisoblanadi.

---

# Module Position

```text
                 Configuration Layer
                          │
                          ▼
                  PriceStreamService
                          │
                          ▼
                    LiveProviders
                          │
                          ▼
                  Provider Factory
                          │
      ┌───────────────────┼────────────────────┐
      ▼                   ▼                    ▼
   Bitget            Binance             Other Providers
      │                   │                    │
      └───────────────────┴────────────────────┘
                          │
                          ▼
                 CurrentPriceProvider
                          │
                          ▼
                  StreamValidator
                          │
                          ▼
                   CandleBuilder
                          │
                          ▼
                   Market Memory
                          │
                          ▼
                    GoldBot Core
```

---

# Module Architecture

```text
                   LiveProviders
                          │
      ┌───────────────────┼────────────────────┐
      ▼                   ▼                    ▼
 Provider Manager   Connection Manager   State Manager
      │                   │                    │
      └───────────────────┼────────────────────┘
                          ▼
               Authentication Manager
                          │
                          ▼
               Subscription Manager
                          │
                          ▼
                  Tick Receiver
                          │
                          ▼
                 Health Monitor
                          │
                          ▼
                Failover Manager
                          │
                          ▼
                 Provider Publisher
                          │
                          ▼
                 PriceStreamService
```

---

# Internal Components

## Provider Manager

Provider tanlash va boshqarish uchun javobgar.

Mas'ul:

- Provider Selection

- Provider Registration

- Provider Switching

---

## Connection Manager

Provider bilan ulanishni boshqaradi.

Mas'ul:

- Connect

- Disconnect

- Reconnect

---

## State Manager

LiveProviders holatini boshqaradi.

Holatlar:

- Idle

- Connecting

- Connected

- Streaming

- Reconnecting

- Failed

---

## Authentication Manager

Provider autentifikatsiyasini boshqaradi.

Mas'ul:

- API Key

- Secret

- Authentication

---

## Subscription Manager

Symbol obunalarini boshqaradi.

Mas'ul:

- Subscribe

- Unsubscribe

- Resubscribe

---

## Tick Receiver

Provider'dan kelayotgan Tick ma'lumotlarini qabul qiladi.

Mas'ul:

- Receive Tick

- Receive Metadata

- Receive Provider Events

---

## Health Monitor

Provider holatini nazorat qiladi.

Tekshiradi:

- Latency

- Heartbeat

- Connection Quality

- Availability

---

## Failover Manager

Provider ishlamay qolsa zaxira Provider'ga o'tadi.

Mas'ul:

- Failure Detection

- Backup Provider Selection

- Automatic Recovery

---

## Provider Publisher

Qabul qilingan Tick'larni PriceStreamService'ga uzatadi.

---

# Dependency Map

```text
Configuration Layer

↓

PriceStreamService

↓

LiveProviders

↓

Provider Manager

↓

Connection Manager

↓

Authentication Manager

↓

Subscription Manager

↓

Tick Receiver

↓

Health Monitor

↓

Failover Manager

↓

Provider Publisher

↓

PriceStreamService

↓

CurrentPriceProvider
```

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

# Input

LiveProviders qabul qiladi:

• Provider Configuration

• Connection Request

• Authentication Credentials

• Subscription Request

• Symbol List

---

# Output

LiveProviders yaratadi:

• Live Tick

• Provider Event

• Provider Status

• Connection Status

• Health Status

---

# Ownership

LiveProviders egalik qiladi:

✓ Provider Connections

✓ Provider Authentication

✓ Symbol Subscriptions

✓ Provider Health

✓ Provider Metadata

✓ Failover State

✓ Connection State

LiveProviders egalik qilmaydi:

✗ Current Price

✗ Tick Validation

✗ Candle

✗ Market Memory

✗ Trading Logic

✗ Strategy

✗ Decision

---

# Module Rules

1. LiveProviders tashqi Provider bilan ishlovchi yagona modul hisoblanadi.

2. Har bir Provider autentifikatsiyadan o'tishi shart.

3. Tick ma'lumotlari o'zgartirilmaydi.

4. Validation keyingi modul tomonidan bajariladi.

5. Provider Health doim monitoring qilinadi.

6. Provider ishlamay qolsa Failover ishga tushadi.

7. LiveProviders faqat PriceStreamService bilan ishlaydi.

8. LiveProviders Trading Logic bajarmaydi.

9. Circular Dependency qat'iyan taqiqlanadi.

---

# Summary

LiveProviders Module Map Live Data modulidagi tashqi Market Data Provider integratsiyasi komponentining ichki arxitekturasini belgilaydi.

Canonical Module Flow:

Configuration Layer

↓

PriceStreamService

↓

LiveProviders

↓

Provider Manager

↓

Connection Manager

↓

Authentication Manager

↓

Subscription Manager

↓

Tick Receiver

↓

Health Monitor

↓

Failover Manager

↓

Provider Publisher

↓

PriceStreamService

↓

CurrentPriceProvider

LiveProviders Live Data Pipeline ichidagi yagona Canonical External Market Data Integration moduli hisoblanadi.
