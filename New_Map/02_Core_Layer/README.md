# Core Layer

Status: CANONICAL

---

# Purpose

Core Layer — GoldBot Runtime'ning markaziy boshqaruv qatlami hisoblanadi.

Uning yagona vazifasi GoldBot tizimini ishga tushirish, barcha Layer'lar orasidagi Runtime Pipeline'ni boshqarish, Service'larni ro'yxatga olish, tizim sog'ligini kuzatish va tizimni xavfsiz to'xtatishdir.

Core Layer marketni tahlil qilmaydi, savdo qarorini chiqarmaydi va Trading Logic bilan ishlamaydi.

---

# Objective

Core Layer quyidagi vazifalarni bajaradi:

• Runtime Orchestration

• Startup Coordination

• Configuration Management

• Service Registration

• Runtime Scheduling

• Runtime Pipeline Management

• Health Monitoring

• Shutdown Coordination

---

# Layer Position

```text
System Runtime

↓

CORE LAYER

↓

All GoldBot Layers (Data, Context, Strategy, Signal, AI, Decision, Risk, Execution, Monitoring, Database, Platform)
```

---

# Internal Structure

Core_Layer/

├── README.md
│
├── Startup/
│
├── Configuration/
│
├── ServiceRegistry/
│
├── CoreEngine/
│
├── CoreService/
│
├── Scheduler/
│
├── Pipeline/
│
├── HealthMonitor/
│
└── Shutdown/

---

# Module Overview

## Startup

Tizimni ishga tushirish jarayonini boshqaradi.

Runtime Initialization.

---

## Configuration

Yagona Configuration manbai.

Barcha Runtime sozlamalarini yuklaydi va taqdim etadi.

---

## ServiceRegistry

Barcha Runtime Service'larini ro'yxatga oladi va topib beradi.

---

## CoreEngine

GoldBot Runtime'ning yagona yuragi.

Runtime Management, Layer Orchestration, Module Coordination, Recovery Coordination.

---

## CoreService

Core modullarni koordinatsiya qiluvchi Service Orchestrator.

---

## Scheduler

Runtime Trigger va vaqt asosidagi jarayonlarni boshqaradi.

---

## Pipeline

Barcha Layer'lar orasidagi Runtime Flow'ni boshqaradi.

---

## HealthMonitor

Runtime sog'ligini kuzatadi.

Performance, Health, Diagnostics.

---

## Shutdown

Tizimni xavfsiz va tartibli to'xtatadi.

Runtime Finalization.

---

# Responsibilities

Core Layer:

✓ Runtime Orchestration

✓ Startup Coordination

✓ Configuration Management

✓ Service Registration

✓ Runtime Scheduling

✓ Runtime Pipeline Management

✓ Health Monitoring

✓ Shutdown Coordination

---

# Not Responsible

Core Layer:

✗ Market Analysis

✗ Context Analysis

✗ Strategy

✗ Signal Generation

✗ AI Analysis

✗ Decision

✗ Risk

✗ Execution

✗ Monitoring Logic (Trade Monitoring)

✗ Database

---

# Core Flow

```text
System Boot

↓

Startup

↓

Configuration

↓

ServiceRegistry

↓

CoreEngine

↓

CoreService

↓

Scheduler

↓

Pipeline

↓

Target Layer

↓

HealthMonitor

↓

Shutdown
```

---

# Golden Rules

1. Core Layer faqat Runtime'ni boshqaradi.

2. Core Layer Business Logic bajarmaydi.

3. Core Layer Trading qarori chiqarmaydi.

4. Startup har doim birinchi ishlaydi, Shutdown har doim oxirgi bosqich hisoblanadi.

5. CoreEngine GoldBot Runtime'ning yagona yuragi hisoblanadi.

6. Barcha Layer'lar CoreEngine va Pipeline orqali ishga tushadi hamda muvofiqlashtiriladi.

7. Configuration yagona sozlama manbai hisoblanadi.

8. ServiceRegistry yagona Service Registry hisoblanadi.

9. HealthMonitor Runtime sog'ligini uzluksiz kuzatadi.

10. Circular Dependency qat'iyan taqiqlanadi.

---

# Repository Structure

Core_Layer/

├── README.md
├── Startup/
├── Configuration/
├── ServiceRegistry/
├── CoreEngine/
├── CoreService/
├── Scheduler/
├── Pipeline/
├── HealthMonitor/
└── Shutdown/

Har bir papka o'z README.md, SequenceDiagram.md, ModuleMap.md va Contracts.md fayllariga ega bo'lishi kerak.

---

# Refactoring Rule

Repository Core Layer blueprint'iga moslashtiriladi.

Kod blueprint'ga mos kelishi shart.

Blueprint kodga moslashtirilmaydi.

---

# Summary

Core Layer — GoldBot Runtime'ning markaziy boshqaruv qatlami hisoblanadi.

Uning vazifasi:

• tizimni ishga tushirish;

• Configuration'ni yuklash;

• Service'larni ro'yxatga olish;

• Runtime Pipeline'ni barcha Layer'lar bo'ylab boshqarish;

• tizim sog'ligini kuzatish;

• tizimni xavfsiz to'xtatish.

Core Layer marketni tahlil qilmaydi, signal yaratmaydi, savdo qarori chiqarmaydi va risk hisoblamaydi. Uning yagona vazifasi GoldBot Runtime'ining ishonchli va izchil ishlashini ta'minlashdir.
