# MarketCalendar Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat MarketCalendar modulining Runtime Sequence (ishlash ketma-ketligi) ni tavsiflaydi.

MarketCalendar Live Data Pipeline ichida bozor holatini (Market Status) nazorat qiladi va PriceStreamService'ga Live Stream qachon boshlanishi yoki to'xtatilishini bildiradi.

Bu implementatsiya emas.

Bu MarketCalendar modulining Canonical Runtime Blueprint hisoblanadi.

---

# Complete Runtime Sequence

```text
System Clock

        │
        ▼
MarketCalendar

        │
        ▼
Load Trading Schedule

        │
        ▼
Check Market Status

        │
        ▼
Publish Market Status

        │
        ▼
PriceStreamService

        │
        ▼
Live Providers

        │
        ▼
Live Data Pipeline
```

---

# Market Open Sequence

```text
System Time

↓

MarketCalendar

↓

Check Trading Hours

↓

Market Open

↓

Publish Open Event

↓

PriceStreamService

↓

Start Live Stream
```

---

# Market Close Sequence

```text
System Time

↓

MarketCalendar

↓

Trading Session End

↓

Market Closed

↓

Publish Close Event

↓

PriceStreamService

↓

Stop Live Stream
```

---

# Session Change Sequence

```text
Current Session

↓

MarketCalendar

↓

Session End

↓

Load Next Session

↓

Publish Session Update

↓

PriceStreamService
```

---

# Holiday Sequence

```text
System Date

↓

MarketCalendar

↓

Holiday Calendar

↓

Holiday Detected

↓

Market Closed

↓

Publish Holiday Event
```

---

# Weekend Sequence

```text
System Date

↓

Weekend Check

↓

Weekend Detected

↓

Market Closed

↓

Wait Next Trading Day
```

---

# Time Zone Sequence

```text
System Clock

↓

Convert Time Zone

↓

Exchange Time

↓

Check Session

↓

Update Market Status
```

---

# Restart Sequence

```text
GoldBot Start

↓

MarketCalendar

↓

Load Calendar

↓

Load Trading Sessions

↓

Determine Current Status

↓

Publish Market Status
```

---

# Error Sequence

```text
Calendar Load Failed

↓

MarketCalendar

↓

Retry

↓

Retry Failed

↓

Use Safe State

↓

Notify PriceStreamService
```

---

# Runtime Rules

1. MarketCalendar tizim vaqti asosida ishlaydi.

2. Har bir Session almashishi avtomatik aniqlanadi.

3. Market Open bo'lsa Open Event yaratiladi.

4. Market Close bo'lsa Close Event yaratiladi.

5. Holiday kunlari Market Closed hisoblanadi.

6. Weekend kunlari Market Closed hisoblanadi (bozor konfiguratsiyasiga qarab).

7. PriceStreamService faqat Market Open holatida Live Stream'ni boshlaydi.

8. MarketCalendar narx ma'lumotlari bilan ishlamaydi.

---

# State Flow

```text
Idle

↓

Loading Calendar

↓

Checking Schedule

↓

Market Open

or

Market Closed

↓

Publishing Status

↓

Waiting

↓

Next Session
```

---

# Golden Rules

• MarketCalendar yagona Market Status manbai hisoblanadi.

• Live Stream faqat Market Open holatida ishlaydi.

• Session almashishi avtomatik boshqariladi.

• Holiday va Weekend hisobga olinadi.

• Time Zone hisoblash majburiy.

• PriceStreamService faqat Market Status asosida ishlaydi.

• MarketCalendar narxlarni qayta ishlamaydi.

• Circular Sequence taqiqlanadi.

---

# Summary

MarketCalendar Sequence Diagram Live Data Pipeline ichidagi bozor sessiyalari va Market Status boshqaruvi ketma-ketligini belgilaydi.

Canonical Runtime Sequence:

System Clock

↓

MarketCalendar

↓

Trading Schedule

↓

Market Status

↓

PriceStreamService

↓

Live Providers

↓

Live Data Pipeline

Ushbu ketma-ketlik MarketCalendar moduli uchun yagona rasmiy Runtime Sequence hisoblanadi.
