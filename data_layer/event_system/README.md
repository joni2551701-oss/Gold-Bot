# Event System

Status: CANONICAL

---

# Purpose

Event System — Data Layer ichidagi modullar o'rtasida ma'lumot almashishni boshqaruvchi ichki kommunikatsiya qatlamidir.

Uning asosiy vazifasi modullarni bir-biridan mustaqil (Decoupled) holda ishlashini ta'minlash va barcha hodisalarni (Events) standart ko'rinishda tarqatishdir.

Event System hech qachon marketni tahlil qilmaydi va savdo qarorini hisoblamaydi.

---

# Objective

Event System quyidagi vazifalarni bajaradi:

• Event Publishing

• Event Subscription

• Event Routing

• Module Communication

• Decoupled Architecture

• Event Distribution

• Event Lifecycle

• Internal Messaging

---

# Layer Position

Source Modules

↓

Event System Layer

↓

Target Modules

---

# Internal Structure

Event_System/

├── README.md
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
├── Layer_Contracts.md
│
├── EventService/
├── EventPublisher/
├── EventBus/
├── EventDispatcher/
├── EventSubscriber/
└── EventLifecycle/

---

# Module Overview

## EventService

Event System Layer'ning markaziy Orchestrator'i.

---

## EventPublisher

Event yaratadigan yagona Producer.

---

## EventBus

Yagona Event Transport.

---

## EventDispatcher

Yagona Event Routing komponenti.

---

## EventSubscriber

Yagona Event Consumer.

---

## EventLifecycle

Barcha Event'larning Lifecycle'ini kuzatuvchi komponent.

---

# Responsibilities

Event System:

✓ Publish Events

✓ Subscribe Events

✓ Route Events

✓ Notify Modules

✓ Synchronize Modules

✓ Decouple Components

✓ Event Lifecycle

✓ Internal Communication

---

# Not Responsible

Event System:

✗ Historical Download

✗ Live Stream

✗ Market Memory Storage

✗ Market Analysis

✗ Strategy Calculation

✗ Decision Engine

✗ Risk Engine

✗ Signal Generation

✗ Trade Execution

---

# Event Flow

Publisher

↓

EventBus

↓

Subscribers

↓

Module Response

---

# Golden Rules

1. Modullar bir-birini to'g'ridan-to'g'ri chaqirmaydi.

2. Har qanday ichki hodisa EventBus orqali uzatiladi.

3. Publisher Subscriber'ni bilmaydi.

4. Subscriber Publisher'ni bilmaydi.

5. EventBus faqat hodisalarni tarqatadi.

6. Eventlar immutable bo'lishi kerak.

7. Event nomlari standartlashtirilgan bo'lishi kerak.

8. Event System biznes logikasini bajarmaydi.

9. Event System modul bog'liqligini kamaytiradi.

10. Event System Data Layer va GoldBot Core o'rtasidagi ichki kommunikatsiyani standartlashtiradi.

---

# Repository Structure

Event_System/

├── README.md
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
├── Layer_Contracts.md
│
├── EventService/
├── EventPublisher/
├── EventBus/
├── EventDispatcher/
├── EventSubscriber/
└── EventLifecycle/

Har bir modul o'z README.md, Contracts.md, ModuleMap.md va SequenceDiagram.md hujjatlariga ega bo'lishi kerak.

---

# Refactoring Rule

Repository Event System blueprint'iga moslashtiriladi.

Kod blueprint'ga mos kelishi shart.

Blueprint kodga moslashtirilmaydi.

---

# Summary

Event System — GoldBot Data Layer ichidagi ichki kommunikatsiya markazi hisoblanadi.

Uning vazifasi:

• hodisalarni yaratish va tarqatish;

• modullarni mustaqil ishlashini ta'minlash;

• komponentlar o'rtasidagi bog'liqlikni kamaytirish;

• yagona EventBus orqali tizim ichidagi barcha Event almashinuvini boshqarish.

Event System hech qachon marketni tahlil qilmaydi va savdo qarorini hisoblamaydi. Uning vazifasi GoldBot ekotizimidagi modullarni bir-biriga bog'lamasdan, ishonchli va standart Event mexanizmi orqali ishlashini ta'minlashdir.
