# Backtest Report Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat BacktestReport Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu BacktestReport modulining Canonical Runtime Blueprint hisoblanadi.
---
# Initialization
```text
Backtesting Layer Boot
↓
Load BacktestReport Configuration
↓
Register BacktestReport
↓
BacktestReport Ready
```
---
# Runtime Sequence
```text
Statistics
↓
BacktestReport
↓
Process Report Assembly
↓
BacktestService (Exit)
```
---
# Error Sequence
```text
BacktestReport Error Detected
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
Reload BacktestReport Configuration
↓
Re-Register
↓
BacktestReport Ready
```
---
# Shutdown Sequence
```text
Shutdown Signal
↓
Flush BacktestReport State
↓
Unregister
↓
Dispose
```
---
# Runtime Rules
1. Statistics natijasi mavjud bo'lishi shart.
2. BacktestReport faqat o'z mas'uliyat doirasida ishlaydi.
3. Output BacktestService (Exit)'ga uzatiladi.
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
Statistics
↓
BacktestReport
↓
BacktestService (Exit)
```
