# Optimization Sequence Diagram
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Optimization Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Optimization modulining Canonical Runtime Blueprint hisoblanadi.
---
# Initialization
```text
Backtesting Layer Boot
↓
Load Optimization Configuration
↓
Register Optimization
↓
Optimization Ready
```
---
# Runtime Sequence
```text
BacktestService
↓
Optimization
↓
Process Parameter Sweep
↓
BacktestEngine
```
---
# Error Sequence
```text
Optimization Error Detected
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
Reload Optimization Configuration
↓
Re-Register
↓
Optimization Ready
```
---
# Shutdown Sequence
```text
Shutdown Signal
↓
Flush Optimization State
↓
Unregister
↓
Dispose
```
---
# Runtime Rules
1. BacktestService natijasi mavjud bo'lishi shart.
2. Optimization faqat o'z mas'uliyat doirasida ishlaydi.
3. Output BacktestEngine'ga uzatiladi.
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
Optimization
↓
BacktestEngine
```
