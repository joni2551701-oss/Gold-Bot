# Audit Log Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat AuditLog Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu AuditLog modulining Canonical Runtime Blueprint hisoblanadi.
---
# Initialization
```text
Boot
↓
Load AuditLog Configuration
↓
Register AuditLog
↓
AuditLog Ready
```
---
# Runtime Sequence
```text
DatabaseManager
↓
AuditLog
↓
Process Login Event Recording
↓
Database Storage
```
---
# Error Sequence
```text
AuditLog Error Detected
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
Reload AuditLog Configuration
↓
Re-Register
↓
AuditLog Ready
```
---
# Shutdown Sequence
```text
Shutdown Signal
↓
Flush AuditLog State
↓
Unregister
↓
Dispose
```
---
# Runtime Rules
1. DatabaseManager natijasi mavjud bo'lishi shart.
2. AuditLog faqat o'z mas'uliyat doirasida ishlaydi.
3. Output Database Storage'ga uzatiladi.
4. Xatolik yuz berganda Error Sequence ishga tushadi, keyin Recovery Sequence orqali tiklanadi.
5. Circular Dependency qat'iyan taqiqlanadi.
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
DatabaseManager
↓
AuditLog
↓
Database Storage
```
