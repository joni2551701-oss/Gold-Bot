# GFL-001 — Flow Dependency

## Maqsad

Ushbu hujjat GoldBot Data Flow o'rtasidagi bog'liqliklarni (Dependency) boshqaradi.

Har bir Flow:

- qayerdan ma'lumot oladi;
- nimani qayta ishlaydi;
- qayerga uzatadi;
- qaysi Flow'ga bog'liq;
- qaysi Flow'ni bloklaydi;

aniq ko'rsatiladi.

---

# Dependency Chain

FLOW-001
Configuration
↓
FLOW-002

FLOW-002
Provider Factory
↓
FLOW-003
FLOW-004

FLOW-003
Historical Data
↓

FLOW-005

FLOW-004
Price Stream
↓

FLOW-005

FLOW-005
Data Validation
↓

FLOW-006

FLOW-006
Market Memory
↓

FLOW-007

FLOW-007
Market Engine
↓

FLOW-008

FLOW-008
Context Engine
↓

FLOW-009

FLOW-009
Analysis Engine
↓

FLOW-010

FLOW-010
Indicator Engine
↓

FLOW-011

FLOW-011
Strategy Engine
↓

FLOW-012

FLOW-012
Confluence Engine
↓

FLOW-013

FLOW-013
Decision Engine
↓

FLOW-014

FLOW-014
Risk Engine
↓

FLOW-015

FLOW-015
Signal Engine
↓

FLOW-016

FLOW-016
Execution Engine
↓

FLOW-017

FLOW-017
Trade Monitoring
↓

FLOW-018

FLOW-018
GoldBot Core API
↓

FLOW-019

FLOW-019
Application Services
↓

FLOW-020
FLOW-021
FLOW-022
FLOW-023
FLOW-024
FLOW-025

FLOW-020
Telegram

FLOW-021
Mini App

FLOW-022
Android

FLOW-023
iOS

FLOW-024
Desktop

FLOW-025
Web

---

# Dependency Matrix

| Flow | Producer | Input | Output | Consumer | Depends On | Blocks |
|------|----------|-------|--------|----------|------------|--------|
| FLOW-001 | Configuration | Config | Runtime Config | Provider Factory | - | FLOW-002 |
| FLOW-002 | Provider Factory | Runtime Config | Providers | Historical / Price Stream | FLOW-001 | FLOW-003 / FLOW-004 |
| FLOW-003 | Historical Data | Provider | Historical Data | Validation | FLOW-002 | FLOW-005 |
| FLOW-004 | Price Stream | Provider | Live Price | Validation | FLOW-002 | FLOW-005 |
| FLOW-005 | Data Validation | Historical + Live | Validated Data | Market Memory | FLOW-003 / FLOW-004 | FLOW-006 |
| FLOW-006 | Market Memory | Validated Data | Market State | Market Engine | FLOW-005 | FLOW-007 |
| FLOW-007 | Market Engine | Market State | Engine State | Context | FLOW-006 | FLOW-008 |
| FLOW-008 | Context Engine | Engine State | Context | Analysis | FLOW-007 | FLOW-009 |
| FLOW-009 | Analysis Engine | Context | Analysis | Indicator | FLOW-008 | FLOW-010 |
| FLOW-010 | Indicator Engine | Analysis | Indicators | Strategy | FLOW-009 | FLOW-011 |
| FLOW-011 | Strategy Engine | Indicators | Strategy Result | Confluence | FLOW-010 | FLOW-012 |
| FLOW-012 | Confluence Engine | Strategy Result | Confluence | Decision | FLOW-011 | FLOW-013 |
| FLOW-013 | Decision Engine | Confluence | Decision | Risk | FLOW-012 | FLOW-014 |
| FLOW-014 | Risk Engine | Decision | Safe Decision | Signal | FLOW-013 | FLOW-015 |
| FLOW-015 | Signal Engine | Safe Decision | Signal | Execution | FLOW-014 | FLOW-016 |
| FLOW-016 | Execution Engine | Signal | Execution Result | Monitoring | FLOW-015 | FLOW-017 |
| FLOW-017 | Trade Monitoring | Execution Result | Trade State | Core API | FLOW-016 | FLOW-018 |
| FLOW-018 | GoldBot Core API | Trade State | API Response | Application | FLOW-017 | FLOW-019 |
| FLOW-019 | Application Services | API | Service Data | Platforms | FLOW-018 | FLOW-020...025 |

---

# Dependency Rules

Har bir Flow:

- faqat bitta asosiy Producer'ga ega bo'lishi kerak.
- kamida bitta Consumer'ga ega bo'lishi kerak.
- Input va Output aniq hujjatlashtirilgan bo'lishi kerak.

---

# Blocking Rules

Agar Producer ishlamasa:

↓

barcha Consumer Blocked bo'ladi.

Misol:

Price Stream

↓

Data Validation

↓

Market Memory

↓

Market Engine

↓

Telegram

Price Stream ishlamasa,

ushbu zanjirning barchasi Blocked hisoblanadi.

---

# End-to-End Rule

Har bir yangi Feature quyidagicha tekshiriladi:

Producer

↓

Input

↓

Processing

↓

Output

↓

Consumer

↓

Platform

↓

User

Har bir bosqich PASS bo'lishi kerak.

---

# Forbidden

Taqiqlanadi:

- Producer'ni chetlab o'tish.
- Market Memory'ni chetlab o'tish.
- Core API'ni chetlab o'tish.
- Dependency hujjatini yangilamasdan yangi Flow qo'shish.
- Documentation'siz Dependency yaratish.

---

# Final Principle

Har bir Flow boshqa Flow bilan bog'langan.

Har bir Dependency hujjatlashtirilgan bo'lishi shart.

GoldBot'da hujjatlashtirilmagan Dependency mavjud bo'lishi mumkin emas.
