# Backtest Engine Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat BacktestEngine Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu BacktestEngine modulining Canonical Runtime Blueprint hisoblanadi.
---
# Initialization
```text
Backtesting Layer Boot
↓
Load BacktestEngine Configuration
↓
Register BacktestEngine
↓
BacktestEngine Ready
```
---
# Runtime Sequence
```text
BacktestService
↓
BacktestEngine
↓
Process Full Chain Simulation
↓
DataFeed
```
---
# Error Sequence
```text
BacktestEngine Error Detected
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
Reload BacktestEngine Configuration
↓
Re-Register
↓
BacktestEngine Ready
```
---
# Shutdown Sequence
```text
Shutdown Signal
↓
Flush BacktestEngine State
↓
Unregister
↓
Dispose
```
---
# Runtime Rules
1. BacktestService natijasi mavjud bo'lishi shart.
2. BacktestEngine faqat o'z mas'uliyat doirasida ishlaydi.
3. Output DataFeed'ga uzatiladi.
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
BacktestService
↓
BacktestEngine
↓
DataFeed
```
