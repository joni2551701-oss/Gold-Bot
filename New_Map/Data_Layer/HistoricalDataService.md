══════════════════════════════════════════════════════════════════════════════
                           HistoricalDataService
══════════════════════════════════════════════════════════════════════════════

Layer
Data Layer

Status
Canonical

Purpose

HistoricalDataService GoldBot uchun tarixiy market
ma'lumotlarini yuklash, tekshirish va Market Memory'ga
joylashtirish uchun javobgar yagona modul hisoblanadi.

Bu modul faqat tarixiy ma'lumotlar bilan ishlaydi.

Live Stream bilan ishlamaydi.

──────────────────────────────────────────────────────────────────────────────
RESPONSIBILITIES
──────────────────────────────────────────────────────────────────────────────

• Historical Candle yuklash.

• Bootstrap vaqtida tarixni olish.

• Recovery vaqtida yetishmagan tarixni tiklash.

• Providerlardan tarixiy ma'lumotlarni olish.

• Data Validation orqali tekshirish.

• Market Memory'ni to'ldirish.

• Historical Database bilan ishlash.

──────────────────────────────────────────────────────────────────────────────
NOT RESPONSIBLE
──────────────────────────────────────────────────────────────────────────────

X

Live Tick

X

Current Price

X

Strategy

X

Decision

X

Risk

X

Signal

X

Telegram

X

Chart

X

Execution

──────────────────────────────────────────────────────────────────────────────
INPUT
──────────────────────────────────────────────────────────────────────────────

Provider Factory

↓

Historical Provider

↓

Request

↓

Historical Candle

Supported Inputs

• Asset

• Timeframe

• Start Time

• End Time

• Candle Limit

• Bootstrap Request

• Recovery Request

──────────────────────────────────────────────────────────────────────────────
OUTPUT
──────────────────────────────────────────────────────────────────────────────

Validated Historical Candle

↓

Market Memory

↓

Historical Database

──────────────────────────────────────────────────────────────────────────────
READ
──────────────────────────────────────────────────────────────────────────────

Provider Configuration

Asset Configuration

Timeframe Configuration

Historical Database

Recovery State

Bootstrap Configuration

──────────────────────────────────────────────────────────────────────────────
WRITE
──────────────────────────────────────────────────────────────────────────────

Market Memory

Historical Database

Bootstrap State

Recovery State

──────────────────────────────────────────────────────────────────────────────
PROVIDERS
──────────────────────────────────────────────────────────────────────────────

Provider Factory

↓

TwelveData Provider

↓

Future Providers

↓

CSV Provider

↓

Offline Provider

──────────────────────────────────────────────────────────────────────────────
CONSUMERS
──────────────────────────────────────────────────────────────────────────────

Market Memory

Market Engine

Context Engine

Analysis Engine

Replay

Simulation

──────────────────────────────────────────────────────────────────────────────
DEPENDENCIES
──────────────────────────────────────────────────────────────────────────────

Provider Factory

Historical Provider

Data Validation

Market Memory

Historical Database

Configuration

──────────────────────────────────────────────────────────────────────────────
PUBLIC API
──────────────────────────────────────────────────────────────────────────────

bootstrap()

recover()

load_history()

load_range()

load_latest()

reload()

refresh()

health()

──────────────────────────────────────────────────────────────────────────────
PRIVATE API
──────────────────────────────────────────────────────────────────────────────

_request_provider()

_validate_history()

_store_memory()

_store_database()

_merge_history()

_detect_missing()

──────────────────────────────────────────────────────────────────────────────
DATA FLOW
──────────────────────────────────────────────────────────────────────────────

Bootstrap

↓

HistoricalDataService

↓

Provider Factory

↓

Historical Provider

↓

Historical Candle

↓

Validation

↓

Market Memory

↓

Historical Database

↓

Market Engine

──────────────────────────────────────────────────────────────────────────────
BOOTSTRAP FLOW
──────────────────────────────────────────────────────────────────────────────

GoldBot Start

↓

Configuration

↓

HistoricalDataService

↓

Provider

↓

History Download

↓

Validation

↓

Market Memory

↓

Ready

──────────────────────────────────────────────────────────────────────────────
RECOVERY FLOW
──────────────────────────────────────────────────────────────────────────────

Gap Detected

↓

HistoricalDataService

↓

Provider

↓

Missing Candle

↓

Validation

↓

Market Memory

──────────────────────────────────────────────────────────────────────────────
ERROR HANDLING
──────────────────────────────────────────────────────────────────────────────

Provider Timeout

↓

Retry

────────────────────

Network Error

↓

Reconnect

────────────────────

Invalid Candle

↓

Reject

────────────────────

Missing Data

↓

Recovery

──────────────────────────────────────────────────────────────────────────────
PERFORMANCE
──────────────────────────────────────────────────────────────────────────────

Historical requests should be batched.

Duplicate requests must be avoided.

Downloaded candles should be cached.

Recovery should download only missing candles.

──────────────────────────────────────────────────────────────────────────────
CACHE POLICY
──────────────────────────────────────────────────────────────────────────────

Use Smart Data Cache.

Never duplicate Market Memory.

Historical Cache

≠

Market Memory

──────────────────────────────────────────────────────────────────────────────
EVENTS
──────────────────────────────────────────────────────────────────────────────

HISTORY_LOADING

HISTORY_READY

HISTORY_UPDATED

RECOVERY_STARTED

RECOVERY_FINISHED

──────────────────────────────────────────────────────────────────────────────
FORBIDDEN
──────────────────────────────────────────────────────────────────────────────

Must never

Create Tick

Create Current Price

Calculate Context

Calculate Strategy

Calculate Decision

Calculate Risk

Generate Signal

Send Telegram Message

Call UI

Call Platform Layer

Call AI Layer

──────────────────────────────────────────────────────────────────────────────
ARCHITECTURE POSITION
──────────────────────────────────────────────────────────────────────────────

Configuration

↓

Provider Factory

↓

HistoricalDataService

↓

Validation

↓

Market Memory

↓

GoldBot Core

──────────────────────────────────────────────────────────────────────────────
LAYER BOUNDARY
──────────────────────────────────────────────────────────────────────────────

Allowed

Provider Factory

Validation

Market Memory

Historical Database

────────────────────

Forbidden

Context

Strategy

Decision

Risk

Execution

Telegram

Chart

Platform

AI

──────────────────────────────────────────────────────────────────────────────
FUTURE EXPANSION
──────────────────────────────────────────────────────────────────────────────

Multi Provider

Parallel Download

Incremental Sync

Cloud History

Compressed Storage

Distributed History

Historical Replay

Backtest Integration

Offline Dataset Support

──────────────────────────────────────────────────────────────────────────────
SUMMARY
──────────────────────────────────────────────────────────────────────────────

HistoricalDataService is the only canonical module
responsible for historical market data.

It owns the complete lifecycle of historical candles:

• Download
• Validation
• Recovery
• Storage
• Market Memory Synchronization

It never performs market analysis,
strategy calculation,
decision making,
or user interaction.
