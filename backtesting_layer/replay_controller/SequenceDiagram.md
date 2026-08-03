# Replay Controller Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ReplayController Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu ReplayController modulining Canonical Runtime Blueprint hisoblanadi.
---
# Initialization
```text
Backtesting Layer Boot
↓
Load ReplayController Configuration
↓
Register ReplayController
↓
ReplayController Ready
```
---
# Runtime Sequence
```text
BacktestService
↓
ReplayController
↓
Process Session Lifecycle Management
↓
ReplayEngine
```
---
# Error Sequence
```text
ReplayController Error Detected
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
Reload ReplayController Configuration
↓
Re-Register
↓
ReplayController Ready
```
---
# Shutdown Sequence
```text
Shutdown Signal
↓
Flush ReplayController State
↓
Unregister
↓
Dispose
```
---
# Runtime Rules
1. BacktestService natijasi mavjud bo'lishi shart.
2. ReplayController faqat o'z mas'uliyat doirasida ishlaydi.
3. Output ReplayEngine'ga uzatiladi.
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
ReplayController
↓
ReplayEngine
```
