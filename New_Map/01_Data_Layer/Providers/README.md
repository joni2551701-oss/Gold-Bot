# Providers

Status: CANONICAL

---

# Purpose

Providers — Data Layer ichidagi tashqi market ma'lumotlari manbalarini (External Data Providers) boshqaruvchi bo'limdir.

Uning asosiy vazifasi GoldBot'ni turli market providerlari bilan bog'lash, ulanishlarni boshqarish va Historical hamda Live Data modullariga standart interfeys orqali ma'lumot yetkazishdir.

Providers hech qachon marketni tahlil qilmaydi va savdo qarorini hisoblamaydi.

---

# Objective

Providers quyidagi vazifalarni bajaradi:

• Provider Management

• Provider Factory

• Historical Providers

• Live Providers

• Provider Interface

• Connection Management

• Authentication

• Failover

• Health Monitoring

• Provider Lifecycle

---

# Layer Position

External Provider

↓

Provider Factory

↓

Providers

↓

Historical Data

+

Live Data

↓

Data Validation

↓

Market Memory

---

# Internal Structure

Providers/

├── README.md
│
├── ProviderFactory/
├── ProviderInterface/
├── TwelveData/
├── Bitget/
├── ProviderLifecycle/
├── ProviderFlow/
│
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
└── Layer_Contracts.md

Har bir modul o'z README.md, SequenceDiagram.md, ModuleMap.md va Contracts.md fayllariga ega.

---

# Module Overview

## ProviderFactory

Barcha providerlarni yaratish va boshqarish.

Historical va Live providerlarni konfiguratsiyaga qarab ishga tushiradi.

---

## ProviderInterface

Har bir provider bajarishi kerak bo'lgan yagona standart interfeys.

Barcha providerlar bir xil contract asosida ishlaydi.

---

## TwelveData

Historical market ma'lumotlarini taqdim etuvchi provider.

Bootstrap.

Recovery.

Historical Candle.

Historical OHLC.

---

## Bitget

Live market ma'lumotlarini taqdim etuvchi provider.

Tick Stream.

Current Price.

Live Candle.

WebSocket.

---

## ProviderLifecycle

Providerlarni ishga tushirish.

Reconnect.

Shutdown.

Health Check.

Monitoring.

---

## ProviderFlow

Providerlardan Historical_Data va Live_Data'ga ma'lumot qanday yo'naltirilishini tavsiflaydi.

---

# Responsibilities

Providers:

✓ Connect External Providers

✓ Manage Provider Lifecycle

✓ Historical Provider Management

✓ Live Provider Management

✓ Authentication

✓ Reconnection

✓ Health Monitoring

✓ Provider Failover

✓ Standard Provider Interface

---

# Not Responsible

Providers:

✗ Market Analysis

✗ Context Calculation

✗ Strategy

✗ Decision Engine

✗ Risk Engine

✗ Signal Generation

✗ Market Memory Storage

✗ Data Validation

✗ User Interface

✗ Business Logic

---

# Provider Flow

External Provider

↓

Provider Factory

↓

Provider Interface

↓

Historical Data

or

Live Data

↓

Data Validation

↓

Market Memory

---

# Golden Rules

1. Barcha providerlar Provider Interface orqali ishlaydi.

2. Providerlar bir-biridan mustaqil bo'lishi kerak.

3. Provider almashtirish GoldBot Core'ga ta'sir qilmasligi kerak.

4. Historical va Live providerlar alohida boshqariladi.

5. Provider Factory yagona provider yaratish nuqtasi hisoblanadi.

6. Providerlar faqat Data Layer bilan ishlaydi.

7. Providerlar marketni tahlil qilmaydi.

8. Providerlardan kelgan barcha ma'lumot Validation'dan o'tadi.

9. Provider nosozligi GoldBot Core ishlashini to'xtatmasligi kerak.

10. Yangi provider qo'shish mavjud arxitekturani buzmasligi kerak.

---

# Repository Structure

Providers/

├── README.md
├── ProviderFactory/
├── ProviderInterface/
├── TwelveData/
├── Bitget/
├── ProviderLifecycle/
├── ProviderFlow/
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
└── Layer_Contracts.md

Har bir provider modul (README.md, SequenceDiagram.md, ModuleMap.md, Contracts.md) o'z papkasida saqlanadi — boshqa 5 sub-guruh (Historical_Data, Live_Data, Market_Memory, Event_System, Data_Validation) bilan bir xil standartda.

---

# Refactoring Rule

Repository Providers blueprint'iga moslashtiriladi.

Kod blueprint'ga mos kelishi shart.

Blueprint kodga moslashtirilmaydi.

---

# Summary

Providers — Data Layer ichidagi tashqi market ma'lumotlari bilan ishlovchi integratsiya markazi hisoblanadi.

Uning vazifasi:

• tashqi providerlar bilan ulanishni boshqarish;

• Historical va Live ma'lumotlarni standart interfeys orqali qabul qilish;

• providerlarning hayotiy siklini boshqarish;

• GoldBot Data Layer'ni providerlardan mustaqil saqlash.

Providers hech qachon marketni tahlil qilmaydi va savdo qarorini hisoblamaydi. Uning vazifasi tashqi ma'lumot manbalari va GoldBot Data Layer o'rtasida ishonchli va standart integratsiyani ta'minlashdir.
