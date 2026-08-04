# GFL-001 — Flow Catalog

## Maqsad

Ushbu hujjat GoldBot Data Flow'larini yagona katalog ko'rinishida boshqaradi.

Har bir Flow:

- mustaqil identifikatorga ega;
- aniq Input va Output'ga ega;
- End-to-End tekshiriladi;
- faqat Completed bo'lgandan keyin keyingi Flow boshlanadi.

---

# FLOW STATUS

Status:

🟦 Blueprint

🟨 In Progress

🟩 Completed

🟥 Blocked

---

# FLOW-001

## Current Price Flow

Status

Blueprint

Producer

Provider Factory

Input

Price Stream

Processing

Data Validation

Output

Validated Current Price

Consumer

Market Memory

Next Flow

FLOW-002

---

# FLOW-002

## Market Memory Flow

Producer

FLOW-001

Input

Validated Current Price

Processing

Store
Cache
Synchronization

Output

Market State

Consumer

Market Engine

Next Flow

FLOW-003

---

# FLOW-003

## Market Engine Flow

Producer

Market Memory

Input

Market State

Processing

Market Processing

Output

Market Context

Consumer

Context Engine

Next Flow

FLOW-004

---

# FLOW-004

## Context Engine Flow

Producer

Market Engine

Input

Market Context

Processing

SMC

Wyckoff

Liquidity

Structure

Output

Market Context Result

Consumer

Analysis Engine

Next Flow

FLOW-005

---

# FLOW-005

## Analysis Engine Flow

Producer

Context Engine

Input

Market Context Result

Processing

Analysis

Scoring

Output

Analysis Result

Consumer

Indicator Engine

Next Flow

FLOW-006

---

# FLOW-006

Indicator Engine

↓

FLOW-007

Strategy Engine

↓

FLOW-008

Confluence Engine

↓

FLOW-009

Decision Engine

↓

FLOW-010

Risk Engine

↓

FLOW-011

Signal Engine

↓

FLOW-012

Execution Engine

↓

FLOW-013

Trade Monitoring

↓

FLOW-014

GoldBot Core API

↓

FLOW-015

Application Services

↓

FLOW-016

Telegram

↓

FLOW-017

Mini App

↓

FLOW-018

Android

↓

FLOW-019

iOS

↓

FLOW-020

Desktop

↓

FLOW-021

Web

---

# Development Rule

Worker faqat bitta Flow ustida ishlaydi.

Har bir Flow:

Audit

↓

Implementation

↓

Testing

↓

Validation

↓

Documentation

↓

WORK_LOG

↓

Completed

↓

Next Flow

---

# Completion Checklist

□ Producer ishlaydi

□ Input ishlaydi

□ Processing ishlaydi

□ Output ishlaydi

□ Consumer ishlaydi

□ End-to-End Test PASS

□ Documentation yangilandi

□ WORK_LOG yozildi

□ Director Review talab qilinmaydi

---

# Forbidden

Worker:

- Flow o'tkazib yubormaydi.
- Ikki Flow ustida parallel ishlamaydi.
- Completed bo'lmagan Flow'dan keyingisiga o'tmaydi.
- Batch Development qilmaydi.

---

# Final Principle

GoldBot har doim bitta Flow bo'yicha rivojlanadi.

Flow tugaydi.

↓

Validation.

↓

Documentation.

↓

WORK_LOG.

↓

Keyingi Flow.

Hech qachon bundan chetga chiqilmaydi.
