══════════════════════════════════════════════════════════════════════════════
                    SENIOR TRADING AI
                  DATA FLOW CONTRACTS
══════════════════════════════════════════════════════════════════════════════

Document ID
04_Data_Flow_Contracts.md

Status
MASTER CONTRACT

Priority
CRITICAL

Authority

This document defines the official data flow
inside the Senior Trading AI Ecosystem.

Every data movement must follow this document.

If implementation conflicts with this contract,
this contract has higher priority.

══════════════════════════════════════════════════════════════════════════════
PURPOSE
══════════════════════════════════════════════════════════════════════════════

This document defines:

• Data Producers
• Data Consumers
• Data Owners
• Data Flow
• Read Rules
• Write Rules
• Event Rules
• Cache Rules
• Memory Rules

This document prevents:

• Hidden data flow
• Multiple writers
• Duplicate cache
• Circular data flow
• Invalid dependencies
• Layer violations

══════════════════════════════════════════════════════════════════════════════
MASTER DATA FLOW
══════════════════════════════════════════════════════════════════════════════

Providers

↓

Historical Data Service
Price Stream Service

↓

Validation

↓

Market Memory

↓

GoldBot Core

↓

Application Services

↓

Platform

↓

User

No module may bypass this flow.

══════════════════════════════════════════════════════════════════════════════
DATA OWNERSHIP
══════════════════════════════════════════════════════════════════════════════

Every data object has exactly one owner.

Only the owner may write.

All other modules may only read.

Examples

Tick

Owner

PriceStreamService

──────────────────────────────

Current Price

Owner

MarketMemory

──────────────────────────────

Closed Candle

Owner

CandleBuilder

──────────────────────────────

Historical Candle

Owner

HistoricalDataService

──────────────────────────────

Context

Owner

Context Engine

──────────────────────────────

Signal

Owner

Signal Engine

──────────────────────────────

Decision

Owner

Decision Engine

══════════════════════════════════════════════════════════════════════════════
WRITE RULE
══════════════════════════════════════════════════════════════════════════════

One Data

↓

One Writer

Examples

Tick

↓

PriceStreamService

Only

──────────────────────────────

Market Memory

↓

PriceStreamService

CandleBuilder

HistoricalDataService

Only

──────────────────────────────

Decision

↓

Decision Engine

Only

No second writer is allowed.

══════════════════════════════════════════════════════════════════════════════
READ RULE
══════════════════════════════════════════════════════════════════════════════

Every module may read data

only through

official public interfaces.

Direct internal access

is forbidden.

Example

Correct

MemoryReader

↓

Market Memory

Incorrect

Module

↓

Memory Internal Objects

══════════════════════════════════════════════════════════════════════════════
EVENT RULE
══════════════════════════════════════════════════════════════════════════════

Events are immutable.

After publishing,

events cannot change.

Producer

↓

Event Bus

↓

Subscribers

Producer never calls subscribers directly.

══════════════════════════════════════════════════════════════════════════════
MARKET MEMORY RULE
══════════════════════════════════════════════════════════════════════════════

Market Memory

is

Single Source of Truth.

All market state

must come

from Market Memory.

No duplicate market state

is allowed.

══════════════════════════════════════════════════════════════════════════════
CACHE RULE
══════════════════════════════════════════════════════════════════════════════

Cache

does not own data.

Cache

only stores copies.

Market Memory

always wins.

══════════════════════════════════════════════════════════════════════════════
PRODUCER / CONSUMER RULE
══════════════════════════════════════════════════════════════════════════════

Producer

creates data.

Consumer

reads data.

Consumers never modify Producer data.

══════════════════════════════════════════════════════════════════════════════
DATA FLOW CONTRACT
══════════════════════════════════════════════════════════════════════════════

Tick

Producer

PriceStreamService

↓

Validator

↓

MarketMemory

↓

CurrentPriceProvider

↓

Consumers

──────────────────────────────

Historical Candle

Producer

HistoricalDataService

↓

Validator

↓

MarketMemory

↓

Core

──────────────────────────────

Closed Candle

Producer

CandleBuilder

↓

MarketMemory

↓

Market Engine

──────────────────────────────

Context

Producer

Context Engine

↓

Analysis Engine

↓

Strategy Engine

──────────────────────────────

Signal

Producer

Signal Engine

↓

Application Services

↓

Platform

──────────────────────────────

Decision

Producer

Decision Engine

↓

Execution

↓

Monitoring

══════════════════════════════════════════════════════════════════════════════
LAYER FLOW RULE
══════════════════════════════════════════════════════════════════════════════

Data Layer

↓

GoldBot Core

↓

Application Services

↓

Platform

↓

User

Reverse flow

is forbidden.

══════════════════════════════════════════════════════════════════════════════
DEPENDENCY RULE
══════════════════════════════════════════════════════════════════════════════

Every data dependency

must point downward.

Circular dependency

is forbidden.

══════════════════════════════════════════════════════════════════════════════
API RULE
══════════════════════════════════════════════════════════════════════════════

Public API

may expose data.

Private implementation

may never be accessed.

══════════════════════════════════════════════════════════════════════════════
IMMUTABILITY RULE
══════════════════════════════════════════════════════════════════════════════

Snapshots

Events

Context

Signals

must never mutate

after publication.

══════════════════════════════════════════════════════════════════════════════
REFACTOR RULE
══════════════════════════════════════════════════════════════════════════════

Before changing data flow,

Worker must verify

Producer

Consumer

Owner

Dependencies

Flow

If any rule breaks,

implementation stops.

══════════════════════════════════════════════════════════════════════════════
WORKER CHECKLIST
══════════════════════════════════════════════════════════════════════════════

Before implementation

Worker must answer

Who owns this data?

Who writes it?

Who reads it?

Can there be two writers?

Does this bypass Market Memory?

Does this violate Layer Flow?

Does this violate Single Source of Truth?

If any answer is uncertain,

implementation must stop.

══════════════════════════════════════════════════════════════════════════════
OWNER RULE
══════════════════════════════════════════════════════════════════════════════

Changing any data flow

requires

Owner approval.

No Worker

may redefine

official data movement.

══════════════════════════════════════════════════════════════════════════════
FINAL LAW
══════════════════════════════════════════════════════════════════════════════

Architecture

defines

Layers.

Repository

defines

Location.

Module Contracts

define

Responsibilities.

Data Flow Contracts

define

Movement.

Every implementation

must satisfy

all four.