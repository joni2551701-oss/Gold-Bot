# Gateway Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Gateway ichki arxitekturasini tavsiflaydi.
---
# Internal Files
```text
authentication.py · authorization.py · dependency_graph.py · gateway.py · gateway_context.py · gateway_events.py · gateway_request.py · health_service.py · metrics_service.py · rate_limiter.py · router.py · service.py · service_breaker.py · service_manifest.py · service_registry.py · service_state.py · version_service.py
```
---
# Module Position
```text
Platform Layer
↓
Gateway
↓
GoldBot Core Services
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
Process (Gateway)
↓
Emit Output
↓
GoldBot Core Services
```
---
# Summary
Gateway GoldBot Core Layer ichidagi Gateway moduli hisoblanadi. Hujjat va kod shu papkada birga saqlanadi.
