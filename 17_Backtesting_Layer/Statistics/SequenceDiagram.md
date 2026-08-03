# Statistics Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Statistics Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Statistics modulining Canonical Runtime Blueprint hisoblanadi.
---
# Initialization
```text
Backtesting Layer Boot
↓
Load Statistics Configuration
↓
Register Statistics
↓
Statistics Ready
```
---
# Runtime Sequence
```text
BacktestEngine
↓
Statistics
↓
Process Signal Performance Calculation
↓
BacktestReport
```
---
# Error Sequence
```text
Statistics Error Detected
↓
Log Error
↓
Emit Error Event
↓
Fallback / Safe State
```
---
# Recovery Sequence
```text
Safe State
↓
Reload Statistics Configuration
↓
Re-Register
↓
Statistics Ready
```
---
# Shutdown Sequence
```text
Shutdown Signal
↓
Flush Statistics State
↓
Unregister
↓
Dispose
```
---
# Runtime Rules
1. BacktestEngine natijasi mavjud bo'lishi shart.
2. Statistics faqat o'z mas'uliyat doirasida ishlaydi.
3. Output BacktestReport'ga uzatiladi.
4. Xatolik yuz berganda Error Sequence ishga tushadi, keyin Recovery Sequence orqali tiklanadi.
5. Backtesting Isolation Rule buzilmaydi — real Broker yoki Execution Layer chaqirilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# State Machine
```text
Idle
↓
Initializing
↓
Ready
↓
Receiving
↓
Processing
↓
Completed
     │
     ├──→ Error ──→ Recovering ──→ Ready
     │
     └──→ Shutting Down ──→ Disposed
```
---
# Summary
```text
BacktestEngine
↓
Statistics
↓
BacktestReport
```
