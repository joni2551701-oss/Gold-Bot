══════════════════════════════════════════════════════════════════════════════
                           PriceStreamService
══════════════════════════════════════════════════════════════════════════════

Layer
Data Layer

Category
Live Data

Status
Canonical

Owner
Data Layer

Single Responsibility

Receive, validate and distribute live market ticks.

PriceStreamService is the only canonical module responsible
for managing real-time market data streams.

It maintains provider connections, validates incoming ticks,
publishes events and synchronizes Market Memory.

It never performs market analysis, strategy execution,
decision making or user interaction.

══════════════════════════════════════════════════════════════════════════════
PURPOSE
══════════════════════════════════════════════════════════════════════════════

Provide a continuous real-time market data stream.

Responsibilities include:

• Connect to live providers.
• Maintain WebSocket connections.
• Receive market ticks.
• Validate every incoming tick.
• Detect duplicate ticks.
• Detect out-of-order ticks.
• Publish tick events.
• Synchronize Market Memory.
• Notify downstream consumers.

══════════════════════════════════════════════════════════════════════════════
PRIMARY RESPONSIBILITIES
══════════════════════════════════════════════════════════════════════════════

✓ Live Tick Streaming

✓ Provider Connection

✓ Connection Monitoring

✓ Automatic Reconnect

✓ Tick Validation

✓ Tick Ordering

✓ Tick Deduplication

✓ Event Publishing

✓ Market Memory Synchronization

✓ Health Monitoring

══════════════════════════════════════════════════════════════════════════════
NOT RESPONSIBLE
══════════════════════════════════════════════════════════════════════════════

PriceStreamService must NEVER

✗ Calculate Context

✗ Calculate Strategy

✗ Calculate Analysis

✗ Calculate Confluence

✗ Calculate Decision

✗ Calculate Risk

✗ Generate Signals

✗ Execute Trades

✗ Send Telegram Messages

✗ Draw Charts

✗ Generate Reports

✗ Calculate Indicators

══════════════════════════════════════════════════════════════════════════════
INPUT
══════════════════════════════════════════════════════════════════════════════

Provider Factory

↓

Bitget WebSocket

↓

Exchange Stream

↓

Tick

────────────────────────

Configuration

────────────────────────

Reconnect Events

────────────────────────

Heartbeat

────────────────────────

Market Calendar

══════════════════════════════════════════════════════════════════════════════
OUTPUT
══════════════════════════════════════════════════════════════════════════════

Validated Tick

↓

EventBus

↓

MarketMemory

↓

CurrentPriceProvider

↓

CandleBuilder

══════════════════════════════════════════════════════════════════════════════
READ
══════════════════════════════════════════════════════════════════════════════

Provider Configuration

Feature Flags

Market Calendar

Connection State

Asset Configuration

Stream Configuration

══════════════════════════════════════════════════════════════════════════════
WRITE
══════════════════════════════════════════════════════════════════════════════

Market Memory

Event Bus

Connection State

Health Status

Metrics

══════════════════════════════════════════════════════════════════════════════
PROVIDERS
══════════════════════════════════════════════════════════════════════════════

Provider Factory

↓

Bitget

↓

Future Exchange Providers

↓

Simulation Provider

↓

Replay Provider

══════════════════════════════════════════════════════════════════════════════
CONSUMERS
══════════════════════════════════════════════════════════════════════════════

CurrentPriceProvider

CandleBuilder

TradingPipeline

Monitoring

Replay

Analytics

══════════════════════════════════════════════════════════════════════════════
DEPENDENCIES
══════════════════════════════════════════════════════════════════════════════

Provider Factory

Stream Validator

Market Calendar

Market Memory

Event Bus

Configuration

══════════════════════════════════════════════════════════════════════════════
PUBLIC API
══════════════════════════════════════════════════════════════════════════════

start()

stop()

restart()

subscribe()

unsubscribe()

connect()

disconnect()

health()

status()

══════════════════════════════════════════════════════════════════════════════
PRIVATE API
══════════════════════════════════════════════════════════════════════════════

_connect()

_disconnect()

_receive_tick()

_validate_tick()

_publish_tick()

_update_memory()

_reconnect()

_process_heartbeat()

══════════════════════════════════════════════════════════════════════════════
DATA FLOW
══════════════════════════════════════════════════════════════════════════════

Provider Factory

↓

Exchange Provider

↓

PriceStreamService

↓

Stream Validator

↓

Market Memory

↓

Event Bus

↓

CurrentPriceProvider

↓

CandleBuilder

══════════════════════════════════════════════════════════════════════════════
LIVE STREAM FLOW
══════════════════════════════════════════════════════════════════════════════

Connect

↓

Authenticate

↓

Subscribe

↓

Receive Tick

↓

Validate Tick

↓

Remove Duplicate

↓

Sequence Check

↓

Publish Event

↓

Update Market Memory

↓

Notify Consumers

══════════════════════════════════════════════════════════════════════════════
CONNECTION FLOW
══════════════════════════════════════════════════════════════════════════════

Disconnected

↓

Connect

↓

Connected

↓

Heartbeat

↓

Healthy

↓

Network Failure

↓

Reconnect

↓

Connected

══════════════════════════════════════════════════════════════════════════════
VALIDATION FLOW
══════════════════════════════════════════════════════════════════════════════

Tick Received

↓

Timestamp Validation

↓

Price Validation

↓

Duplicate Validation

↓

Sequence Validation

↓

Accepted Tick

↓

Market Memory

══════════════════════════════════════════════════════════════════════════════
ERROR HANDLING
══════════════════════════════════════════════════════════════════════════════

Connection Lost

↓

Reconnect

────────────────────────

Provider Timeout

↓

Retry

────────────────────────

Invalid Tick

↓

Reject

────────────────────────

Duplicate Tick

↓

Ignore

────────────────────────

Out-of-Order Tick

↓

Reject

────────────────────────

Unknown Asset

↓

Ignore

══════════════════════════════════════════════════════════════════════════════
EVENTS
══════════════════════════════════════════════════════════════════════════════

STREAM_STARTED

STREAM_STOPPED

STREAM_CONNECTED

STREAM_DISCONNECTED

STREAM_RECONNECTED

TICK_RECEIVED

TICK_VALIDATED

TICK_REJECTED

PRICE_UPDATED

HEALTH_CHANGED

══════════════════════════════════════════════════════════════════════════════
PERFORMANCE
══════════════════════════════════════════════════════════════════════════════

Low Latency

Minimal Memory Allocation

High Throughput

Async Processing

Non-Blocking IO

Backpressure Protection

Connection Pooling

══════════════════════════════════════════════════════════════════════════════
CACHE POLICY
══════════════════════════════════════════════════════════════════════════════

PriceStreamService

owns NO cache.

Market Memory

owns market state.

Cache

is only an optimization.

Market Memory always wins.

══════════════════════════════════════════════════════════════════════════════
RECOVERY
══════════════════════════════════════════════════════════════════════════════

Reconnect

↓

Resubscribe

↓

Resume Stream

↓

Gap Detection

↓

Historical Recovery

↓

Continue Streaming

══════════════════════════════════════════════════════════════════════════════
LAYER POSITION
══════════════════════════════════════════════════════════════════════════════

Configuration

↓

Provider Factory

↓

PriceStreamService

↓

Validation

↓

Market Memory

↓

GoldBot Core

══════════════════════════════════════════════════════════════════════════════
ALLOWED DEPENDENCIES
══════════════════════════════════════════════════════════════════════════════

Provider Factory

Market Calendar

Stream Validator

Event Bus

Market Memory

Configuration

══════════════════════════════════════════════════════════════════════════════
FORBIDDEN DEPENDENCIES
══════════════════════════════════════════════════════════════════════════════

Context Engine

Analysis Engine

Strategy Engine

Confluence Engine

Decision Engine

Risk Engine

Signal Engine

Telegram

Mobile

Desktop

Web

AI Layer

Execution

══════════════════════════════════════════════════════════════════════════════
ARCHITECTURE RULES
══════════════════════════════════════════════════════════════════════════════

Rule 1

PriceStreamService is the only writer of live ticks.

────────────────────────

Rule 2

Every tick must be validated before entering Market Memory.

────────────────────────

Rule 3

No consumer communicates directly with providers.

────────────────────────

Rule 4

All consumers receive market data from canonical sources only.

────────────────────────

Rule 5

PriceStreamService never performs business logic.

══════════════════════════════════════════════════════════════════════════════
FUTURE EXPANSION
══════════════════════════════════════════════════════════════════════════════

Multi Exchange Support

Provider Failover

Load Balancing

Distributed Streaming

Regional Stream Nodes

Kafka Integration

Message Queue Support

Latency Monitoring

AI Stream Quality Detection

High Availability Cluster

══════════════════════════════════════════════════════════════════════════════
SUMMARY
══════════════════════════════════════════════════════════════════════════════

PriceStreamService is the canonical live market data
stream manager.

It is responsible only for:

• Receiving live ticks.
• Validating ticks.
• Managing provider connections.
• Publishing events.
• Updating Market Memory.

It never performs analysis, strategy calculation,
decision making, execution, AI processing,
or platform communication.

It is the single entry point for all live market data
inside the Data Layer.