# Errors Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Errors ichki arxitekturasini tavsiflaydi.
---
# Internal Files
```text
base.py · codes.py · exceptions.py
```
---
# Module Position
```text
Barcha Layer'lar
↓
Errors
↓
Logger / Caller
```
---
# Allowed Dependencies
✓ Configuration
✓ Logger
✓ Errors
---
# Forbidden Dependencies
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
✗ Platform Layer
---
# Runtime Flow
```text
Receive Input
↓
Process (Errors)
↓
Emit Output
↓
Logger / Caller
```
---
# Summary
Errors GoldBot Core Layer ichidagi Errors moduli hisoblanadi. Hujjat va kod shu papkada birga saqlanadi.
