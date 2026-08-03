# Replay Engine Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ReplayEngine Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu ReplayEngine modulining Canonical Runtime Blueprint hisoblanadi.
---
# Initialization
```text
Backtesting Layer Boot
↓
Load ReplayEngine Configuration
↓
Register ReplayEngine
↓
ReplayEngine Ready
```
---
# Runtime Sequence
```text
DataFeed
↓
ReplayEngine
↓
Process Historical Candle Loading
↓
Historical Data (Database Layer, read-only)
```
---
# Error Sequence
```text
ReplayEngine Error Detected
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
Reload ReplayEngine Configuration
↓
Re-Register
↓
ReplayEngine Ready
```
---
# Shutdown Sequence
```text
Shutdown Signal
↓
Flush ReplayEngine State
↓
Unregister
↓
Dispose
```
---
# Runtime Rules
1. DataFeed natijasi mavjud bo'lishi shart.
2. ReplayEngine faqat o'z mas'uliyat doirasida ishlaydi.
3. Output Historical Data (Database Layer, read-only)'ga uzatiladi.
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
DataFeed
↓
ReplayEngine
↓
Historical Data (Database Layer, read-only)
```
