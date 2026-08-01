Document Information

Document Name
02_Bootstrap.md
Layer
02_Data_Layer
Module
Historical Data
Component
Bootstrap
Status
Canonical
Priority
Critical

⸻

Purpose

Bootstrap — GoldBot ishga tushganda tizimni savdo uchun tayyor holatga keltirish jarayoni.

Bootstrap vazifasi — barcha kerakli tarixiy market ma’lumotlarini yuklash, tekshirish va Market Memory’ni to’ldirish.

Bootstrap tugamasdan GoldBot Core ish boshlamaydi.

⸻

Goal

GoldBot ish boshlashidan oldin:

* Historical Data tayyor bo’lishi.
* Market Memory to’ldirilishi.
* Candle ketma-ketligi tekshirilishi.
* Core ishlashga tayyor bo’lishi.

⸻

Responsibilities

Bootstrap quyidagilarni bajaradi:

* Asset ro’yxatini olish.
* Timeframe ro’yxatini olish.
* Provider bilan ulanish.
* Historical candles yuklash.
* Validation bajarish.
* Market Memory’ni to’ldirish.
* Historical Database’ni yangilash.
* Bootstrap holatini tekshirish.

⸻

Not Responsible

Bootstrap quyidagilarni bajarmaydi:

* Live Tick qabul qilish.
* Stream ochish.
* Current Price hisoblash.
* Candle yaratish.
* Context hisoblash.
* Strategy hisoblash.
* Signal yaratish.
* Trade ochish.

⸻

Bootstrap Trigger

Bootstrap quyidagi holatlarda ishga tushadi:

* GoldBot Start
* Cold Start
* Full Restart
* Manual Bootstrap
* Empty Market Memory

⸻

Preconditions

Bootstrap boshlanishidan oldin:

* Configuration yuklangan bo’lishi.
* ProviderFactory tayyor bo’lishi.
* Asset List tayyor bo’lishi.
* Timeframe List tayyor bo’lishi.
* API konfiguratsiyasi tekshirilgan bo’lishi.

⸻

Input

Configuration
        │
        ▼
Provider Factory
        │
        ▼
Assets
        │
        ▼
Timeframes

⸻

Output

Historical Candles
        │
        ▼
Validated Candles
        │
        ▼
Market Memory
        │
        ▼
Historical Database
        │
        ▼
Bootstrap Complete

⸻

Bootstrap Sequence

GoldBot Start
        │
        ▼
Load Configuration
        │
        ▼
Initialize ProviderFactory
        │
        ▼
Load Assets
        │
        ▼
Load Timeframes
        │
        ▼
HistoricalDataService
        │
        ▼
Download Historical Candles
        │
        ▼
Validate Data
        │
        ▼
Fill Market Memory
        │
        ▼
Update Historical Database
        │
        ▼
Bootstrap Finished
        │
        ▼
GoldBot Core Enabled

⸻

State Machine

IDLE
↓
INITIALIZING
↓
CONNECTING
↓
DOWNLOADING
↓
VALIDATING
↓
LOADING_MEMORY
↓
COMPLETED

⸻

Failure States

IDLE
↓
CONNECTING
↓
FAILED
↓
RETRY
↓
CONNECTING

⸻

Validation Rules

Har bir candle tekshiriladi:

* Asset
* Timeframe
* Timestamp
* OHLC
* Volume (agar mavjud bo’lsa)
* Duplicate
* Missing Candle
* Candle Order

Validationdan o’tmagan candle Market Memory’ga yozilmaydi.

⸻

Retry Policy

Provider javob bermasa:

* Retry 1
* Retry 2
* Retry 3

Agar baribir muvaffaqiyatsiz bo’lsa:

* Bootstrap FAILED holatiga o’tadi.
* GoldBot Core ishga tushmaydi.
* Xatolik log qilinadi.

⸻

Success Criteria

Bootstrap muvaffaqiyatli hisoblanadi agar:

* Barcha kerakli assetlar yuklangan.
* Barcha timeframe’lar yuklangan.
* Validation muvaffaqiyatli o’tgan.
* Market Memory tayyor.
* Historical Database sinxron.
* Critical xatolik yo’q.

⸻

Performance Requirements

* Batch Download ishlatiladi.
* Parallel yuklash kelajakda qo’llab-quvvatlanadi.
* Keraksiz so’rovlar yuborilmaydi.
* Duplicate yuklash bo’lmaydi.
* Market Memory faqat bir marta to’ldiriladi.

⸻

Dependencies

Bootstrap quyidagi modullarga bog’liq:

* Configuration
* ProviderFactory
* HistoricalDataService
* DataValidation
* MarketMemory
* HistoricalDatabase

⸻

Forbidden

Bootstrap quyidagilarni bajarmaydi:

* Live Stream boshlash.
* Current Price yaratish.
* Decision hisoblash.
* Strategy ishlatish.
* Signal yaratish.
* Telegram yuborish.
* AI bilan ishlash.

⸻

Architecture Position

GoldBot Start
        │
        ▼
Configuration
        │
        ▼
Provider Factory
        │
        ▼
Bootstrap
        │
        ▼
HistoricalDataService
        │
        ▼
Market Memory
        │
        ▼
GoldBot Core

⸻

Future Expansion

Kelajakda qo’shilishi mumkin:

* Incremental Bootstrap.
* Multi Provider Bootstrap.
* Parallel Bootstrap.
* Bootstrap Progress Monitoring.
* Resume Bootstrap.
* Distributed Bootstrap.

⸻

Summary

Bootstrap — GoldBot ishga tushishidagi birinchi va majburiy bosqich.

Uning asosiy vazifasi:

* tarixiy ma’lumotlarni yuklash;
* ularni tekshirish;
* Market Memory’ni tayyorlash;
* GoldBot Core ishlashi uchun ishonchli boshlang’ich holat yaratish.

Bootstrap muvaffaqiyatli yakunlanmaguncha GoldBot Core va undan yuqori qatlamlar ishga tushirilmaydi.
