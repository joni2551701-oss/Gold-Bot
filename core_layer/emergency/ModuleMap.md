# Emergency Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Emergency ichki arxitekturasini tavsiflaydi.
---
# Internal Files
```text
circuit_breaker.py · emergency_manager.py · emergency_state.py · maintenance.py
```
---
# Module Position
```text
Owner Command
↓
Emergency
↓
Pipeline / Runtime
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
Process (Emergency)
↓
Emit Output
↓
Pipeline / Runtime
```
---
# Summary
Emergency GoldBot Core Layer ichidagi Emergency moduli hisoblanadi. Hujjat va kod shu papkada birga saqlanadi.
