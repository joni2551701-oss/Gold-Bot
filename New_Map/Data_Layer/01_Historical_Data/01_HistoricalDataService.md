Document Name
01_HistoricalDataService.md
Layer
02_Data_Layer
Module
Historical Data
Component
HistoricalDataService
Status
Canonical
Priority
Critical

⸻

Purpose

HistoricalDataService — GoldBot Data Layer ichidagi yagona modul bo’lib, tarixiy market ma’lumotlarini providerlardan yuklash, tekshirish va Market Memory’ga joylashtirish uchun javobgar.

Bu modul faqat historical candles bilan ishlaydi.

Live Tick bilan ishlamaydi.

⸻

Goal

GoldBot ishga tushishidan oldin yoki Recovery vaqtida kerakli tarixiy ma’lumotlarni tayyorlash.

⸻

Responsibilities

HistoricalDataService quyidagilar uchun javobgar:

* Historical candle yuklash.
* Bootstrap vaqtida tarixni olish.
* Recovery vaqtida yetishmayotgan candlelarni tiklash.
* Providerlardan tarixiy ma’lumotlarni olish.
* Data Validation orqali tekshirish.
* Market Memory’ni to’ldirish.
* Historical Database bilan sinxronlash.
* Gap Detection uchun ma’lumot tayyorlash.

⸻

Not Responsible

HistoricalDataService quyidagilarni bajarmaydi:

* Live Tick qabul qilish.
* Current Price hisoblash.
* Candle yaratish.
* Context hisoblash.
* Strategy hisoblash.
* Decision chiqarish.
* Risk hisoblash.
* Signal yaratish.
* Telegram xabar yuborish.
* Chart chizish.
* Trade ochish yoki yopish.

⸻

Input

HistoricalDataService quyidagi ma’lumotlarni qabul qiladi:

Provider Factory
        │
        ▼
Historical Provider
        │
        ▼
Historical Candle Request

Request tarkibi:

* Asset
* Timeframe
* Start Time
* End Time
* Candle Limit
* Bootstrap Request
* Recovery Request

⸻

Output

Natija:

Validated Historical Candles
        │
        ├──► MarketMemory
        │
        └──► HistoricalDatabase

⸻

Read

HistoricalDataService quyidagi ma’lumotlarni o’qiydi:

* Provider Configuration
* Asset Configuration
* Timeframe Configuration
* Bootstrap Configuration
* Recovery Configuration
* Historical Database
* Feature Flags

⸻

Write

HistoricalDataService quyidagilarga yozadi:

* MarketMemory
* HistoricalDatabase
* Bootstrap Status
* Recovery Status
* Metrics

⸻

Providers

HistoricalDataService foydalanadigan providerlar:

ProviderFactory
      │
      ├── TwelveData
      ├── CSV Provider
      ├── Offline Dataset
      └── Future Providers

⸻

Consumers

HistoricalDataService natijasidan foydalanadigan modullar:

* MarketMemory
* Market Engine
* Context Engine
* Analysis Engine
* Replay
* Simulation

⸻

Dependencies

Majburiy bog’liqliklar:

* ProviderFactory
* DataValidation
* MarketMemory
* HistoricalDatabase
* Configuration

⸻

Public API

Tashqi modullar foydalanishi mumkin bo’lgan metodlar:

bootstrap()
recover()
load_history()
load_range()
load_latest()
reload()
health()
status()

⸻

Internal API

Faqat modul ichida ishlatiladi:

_request_provider()
_validate_history()
_store_memory()
_store_database()
_merge_history()
_detect_missing()
_prepare_request()

⸻

Data Flow

GoldBot Start
        │
        ▼
HistoricalDataService
        │
        ▼
Provider Factory
        │
        ▼
Historical Provider
        │
        ▼
Historical Candles
        │
        ▼
Data Validation
        │
        ▼
MarketMemory
        │
        ▼
HistoricalDatabase

⸻

State Flow

IDLE
↓
BOOTSTRAP
↓
LOADING
↓
VALIDATING
↓
SAVING
↓
READY

Recovery holati:

READY
↓
GAP DETECTED
↓
RECOVERY
↓
VALIDATION
↓
MARKET MEMORY
↓
READY

⸻

Error Handling

Xatoliklar:

* Provider Timeout
* Invalid Response
* Missing Candle
* Duplicate Candle
* Network Failure
* Invalid Timeframe
* Unsupported Asset

Har bir holat log qilinadi va Recovery mexanizmi ishga tushiriladi.

⸻

Performance

Talablar:

* Batch Download
* Parallel Requests (kelajakda)
* Duplicate Request Prevention
* Incremental Sync
* Retry Strategy
* Memory Efficient Loading

⸻

Security

* API Key ProviderFactory orqali olinadi.
* API Key modul ichida saqlanmaydi.
* Secret ma’lumotlar log qilinmaydi.

⸻

Architecture Position

Configuration
        │
        ▼
Provider Factory
        │
        ▼
HistoricalDataService
        │
        ▼
Data Validation
        │
        ▼
MarketMemory
        │
        ▼
GoldBot Core

⸻

Layer Rules

Allowed:

* ProviderFactory
* DataValidation
* MarketMemory
* HistoricalDatabase

Forbidden:

* Context Engine
* Strategy Engine
* Decision Engine
* Risk Engine
* Signal Engine
* Telegram
* AI Layer
* Platform Layer

⸻

Future Expansion

Kelajakdagi imkoniyatlar:

* Multi Provider Download
* Provider Failover
* Cloud History
* Distributed History Storage
* Historical Compression
* Historical Replay
* Offline Dataset Support
* Smart Incremental Recovery

⸻

Module Contract

Module Type:

Producer

Primary Responsibility:

Historical Market Data

Writes To:

MarketMemory
HistoricalDatabase

Reads From:

Providers
Configuration

⸻

Summary

HistoricalDataService — tarixiy market ma’lumotlarini boshqaruvchi yagona kanonik modul.

Uning vazifasi:

* Historical ma’lumotlarni yuklash.
* Validatsiya qilish.
* Bootstrap bajarish.
* Recovery bajarish.
* MarketMemory va HistoricalDatabase’ni sinxronlash.

U hech qachon market tahlili, strategiya, risk yoki savdo qarorlarini hisoblamaydi.
