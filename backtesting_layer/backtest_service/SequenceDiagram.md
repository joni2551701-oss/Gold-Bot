# Backtest Service Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat BacktestService Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu BacktestService modulining Canonical Runtime Blueprint hisoblanadi.
---
# Initialization
```text
Backtesting Layer Boot
↓
Load BacktestService Configuration
↓
Register BacktestService
↓
BacktestService Ready
```
---
# Runtime Sequence
```text
Owner Command (Platform Layer)
↓
BacktestService
↓
Process Backtest Request Validation
↓
BacktestEngine / ReplayController
```
---
# Error Sequence
```text
BacktestService Error Detected
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
Reload BacktestService Configuration
↓
Re-Register
↓
BacktestService Ready
```
---
# Shutdown Sequence
```text
Shutdown Signal
↓
Flush BacktestService State
↓
Unregister
↓
Dispose
```
---
# Runtime Rules
1. Owner Command (Platform Layer) natijasi mavjud bo'lishi shart.
2. BacktestService faqat o'z mas'uliyat doirasida ishlaydi.
3. Output BacktestEngine / ReplayController'ga uzatiladi.
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
Owner Command (Platform Layer)
↓
BacktestService
↓
BacktestEngine / ReplayController
```
