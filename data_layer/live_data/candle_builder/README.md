# Candle Builder

Status: CANONICAL

---

# Purpose

CandleBuilder — Live Data modulining Tick ma'lumotlaridan OHLC Candle yaratish va yangilash uchun javobgar komponentidir.

Uning asosiy vazifasi CurrentPriceProvider tomonidan uzatilgan tasdiqlangan narxlarni Timeframe qoidalariga muvofiq Candle ko'rinishiga o'tkazishdir.

CandleBuilder faqat Candle yaratadi va yangilaydi.

U Trading Logic, Market Analysis yoki Signal Generation bilan shug'ullanmaydi.

---

# Objective

CandleBuilder quyidagi vazifalarni bajaradi:

• OHLC Candle Generation

• Candle Update

• Candle Close

• New Candle Creation

• Multi-Timeframe Candle Building

• Candle State Management

• Candle Publishing

---

# Layer Position

```text
Live Provider

↓

PriceStreamService

↓

CurrentPriceProvider

↓

Stream Validator

↓

CandleBuilder

↓

Market Memory

↓

GoldBot Core
```

---

# Responsibilities

CandleBuilder:

✓ Tick'dan OHLC Candle yaratish

✓ Open narxini belgilash

✓ High narxini yangilash

✓ Low narxini yangilash

✓ Close narxini yangilash

✓ Candle yopish

✓ Yangi Candle ochish

✓ Multi-Timeframe Candle yaratish

---

# Not Responsible

CandleBuilder:

✗ Live Stream Management

✗ Provider Connection

✗ Current Price Management

✗ Stream Validation

✗ Historical Data

✗ Market Calendar

✗ Context Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal Generation

✗ AI Analysis

---

# Input

CandleBuilder quyidagilarni qabul qiladi:

• Validated Tick

• Current Price

• Timestamp

• Symbol

• Timeframe

---

# Output

CandleBuilder quyidagilarni yaratadi:

• Current Candle

• Closed Candle

• New Candle

• OHLC Data

• Candle Update Event

---

# Managed Data

CandleBuilder quyidagi ma'lumotlarni boshqaradi:

• Open

• High

• Low

• Close

• Volume (agar mavjud bo'lsa)

• Timestamp

• Timeframe

• Symbol

• Candle Status

---

# Workflow

```text
Live Provider

↓

PriceStreamService

↓

CurrentPriceProvider

↓

Stream Validator

↓

CandleBuilder

↓

Market Memory

↓

GoldBot Core
```

---

# Golden Rules

1. CandleBuilder faqat Validation'dan o'tgan Tick bilan ishlaydi.

2. Har bir Tick faqat bitta Candle'ni yangilaydi.

3. Har bir Candle faqat bitta Timeframe'ga tegishli bo'ladi.

4. Candle yopilgandan keyin qayta o'zgartirilmaydi.

5. Yangi Candle oldingi Candle yopilgandan keyin yaratiladi.

6. CandleBuilder History saqlamaydi.

7. CandleBuilder Market Memory'ga faqat tayyor Candle uzatadi.

8. CandleBuilder Trading Logic'dan mustaqil bo'lishi shart.

---

# Related Documents

```text
CandleBuilder/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

CandleBuilder — Live Data modulining OHLC Candle yaratish komponentidir.

Uning vazifasi:

• Validated Tick asosida Candle yaratish;

• Open, High, Low va Close qiymatlarini boshqarish;

• Candle yopish va yangi Candle ochish;

• Tayyor Candle'ni Market Memory'ga uzatish.

CandleBuilder Live Data Pipeline ichidagi yagona Canonical Candle Generation moduli hisoblanadi.
