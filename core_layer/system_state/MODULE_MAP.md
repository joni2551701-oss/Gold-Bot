# System State Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat SystemState ichki arxitekturasini tavsiflaydi.
---
# Internal Files
```text
system_state.py
```
---
# Module Position
```text
Owner Command / Emergency
↓
SystemState
↓
Runtime Consumers
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
Process (SystemState)
↓
Emit Output
↓
Runtime Consumers
```
---
# Summary
SystemState GoldBot Core Layer ichidagi System State moduli hisoblanadi. Hujjat va kod shu papkada birga saqlanadi.
