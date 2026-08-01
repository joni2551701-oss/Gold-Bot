══════════════════════════════════════════════════════════════════════════════
                        SENIOR TRADING AI
                    MODULE CONTRACTS STANDARD
══════════════════════════════════════════════════════════════════════════════

Document ID
03_Module_Contracts.md

Status
MASTER CONTRACT

Priority
CRITICAL

Authority
This document defines the official responsibility and boundaries
of every module inside the Senior Trading AI Ecosystem.

Every source file must follow this contract.

If any implementation conflicts with this document,
this document has higher priority.

══════════════════════════════════════════════════════════════════════════════
PURPOSE
══════════════════════════════════════════════════════════════════════════════

This document exists to define:

• What every module is responsible for.
• What every module is NOT allowed to do.
• Which modules it can communicate with.
• Which modules it cannot communicate with.
• What data enters the module.
• What data leaves the module.
• Which public API the module exposes.
• Which internal API remains private.

This document prevents:

• Duplicate logic
• Hidden responsibilities
• Layer violations
• Circular dependencies
• Architecture drift
• Unclear ownership

══════════════════════════════════════════════════════════════════════════════
MODULE CONTRACT TEMPLATE
══════════════════════════════════════════════════════════════════════════════

Every module must define the following sections.

1. Module Name

Official module name.

────────────────────────────────────────

2. Purpose

One sentence explaining why this module exists.

────────────────────────────────────────

3. Responsibilities

Only the work this module is allowed to perform.

────────────────────────────────────────

4. Input

Everything accepted by the module.

────────────────────────────────────────

5. Output

Everything returned by the module.

────────────────────────────────────────

6. Consumers

Who is allowed to use this module.

────────────────────────────────────────

7. Providers

Where this module receives its data.

────────────────────────────────────────

8. Dependencies

Official dependencies.

Only these modules may be imported.

────────────────────────────────────────

9. Public API

Functions/classes that other modules may use.

────────────────────────────────────────

10. Internal API

Private implementation details.

Must never be used outside this module.

────────────────────────────────────────

11. Forbidden

Everything this module is NOT allowed to do.

────────────────────────────────────────

12. Notes

Additional architectural information.

══════════════════════════════════════════════════════════════════════════════
DEPENDENCY RULES
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

Dependencies always go downward.

Lower layers never know higher layers.

Forbidden

Data Layer → Context

Data Layer → Strategy

Data Layer → Decision

Core → Telegram

Core → Mobile

Core → UI

Platform → Provider

Platform → Database

AI → Decision Engine

AI → Risk Engine

══════════════════════════════════════════════════════════════════════════════
MODULE EXAMPLE
══════════════════════════════════════════════════════════════════════════════

Module

PriceStreamService

Purpose

Manage the live market stream.

Responsibilities

• Connect provider.
• Receive ticks.
• Validate ticks.
• Publish events.
• Update Market Memory.

Input

Live Tick

Output

Tick Event

Consumers

CurrentPriceProvider

CandleBuilder

MarketMemory

Providers

Bitget

Twelve Data

Dependencies

StreamValidator

EventBus

Provider

Public API

start()

stop()

subscribe()

unsubscribe()

Internal API

_connect()

_reconnect()

_handle_tick()

Forbidden

Cannot create candles.

Cannot calculate context.

Cannot execute strategy.

Cannot calculate risk.

Cannot send Telegram messages.

Cannot execute trades.

══════════════════════════════════════════════════════════════════════════════
RESPONSIBILITY RULE
══════════════════════════════════════════════════════════════════════════════

One Module

↓

One Responsibility

Every module must have exactly one primary responsibility.

If a second responsibility appears,

the module must be split.

══════════════════════════════════════════════════════════════════════════════
IMPORT RULE
══════════════════════════════════════════════════════════════════════════════

Imports must follow the architecture.

Allowed

Data

↓

Core

↓

Services

↓

Platform

Forbidden

Platform

↓

Core

↓

Data

Circular imports are forbidden.

══════════════════════════════════════════════════════════════════════════════
PUBLIC API RULE
══════════════════════════════════════════════════════════════════════════════

Only Public API may be used.

Private methods

(_method)

must never be called

from another module.

══════════════════════════════════════════════════════════════════════════════
MODULE OWNERSHIP
══════════════════════════════════════════════════════════════════════════════

Every module has exactly one owner.

Every responsibility has exactly one module.

No duplicate ownership.

══════════════════════════════════════════════════════════════════════════════
REFACTORING RULES
══════════════════════════════════════════════════════════════════════════════

Before modifying any module,

Worker must verify

Purpose

Responsibilities

Dependencies

Forbidden

If implementation conflicts,

Architecture wins.

══════════════════════════════════════════════════════════════════════════════
WORKER RULES
══════════════════════════════════════════════════════════════════════════════

Before writing code

Worker must read

01_Ecosystem_Architecture.md

↓

02_Repository_Structure.md

↓

03_Module_Contracts.md

Only after all three are understood

implementation may begin.

══════════════════════════════════════════════════════════════════════════════
OWNER RULE
══════════════════════════════════════════════════════════════════════════════

Changing a Module Contract

requires

Owner approval.

Implementation cannot silently redefine

module responsibilities.

══════════════════════════════════════════════════════════════════════════════
FINAL LAW
══════════════════════════════════════════════════════════════════════════════

Architecture

defines

Layers.

Repository Structure

defines

Location.

Module Contracts

define

Responsibilities.

Code must follow all three.