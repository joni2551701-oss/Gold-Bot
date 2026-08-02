# TwelveData Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat TwelveData Runtime Sequence'ni tavsiflaydi.

---

# Runtime Sequence

```text
HistoricalProviders So'rovi
↓
ProviderInterface
↓
TwelveData
↓
Historical Candle / OHLC Qaytariladi
↓
HistoricalDatabase'ga Uzatiladi
```

---

# Runtime Rules

1. So'rov Symbol va Timeframe bilan birga kelishi shart.
2. TwelveData ProviderInterface Contract'iga mos javob qaytaradi.
3. Xato holatida ProviderLifecycle orqali Retry ishga tushadi.

---

# State Flow

```text
Idle
↓
Requesting
↓
Fetching
↓
Returning Data
↓
Completed
```

---

# Summary

HistoricalProviders
↓
TwelveData
↓
Historical Candle / OHLC
