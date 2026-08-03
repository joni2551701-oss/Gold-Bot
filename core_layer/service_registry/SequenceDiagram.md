# ServiceRegistry Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ServiceRegistry modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu ServiceRegistry modulining Canonical Runtime Blueprint hisoblanadi.
---
# Startup Sequence
```text
System Start
↓
ServiceRegistry
↓
Initialize Registry
↓
Register Core Services
↓
Ready
```
---
# Registration Sequence
```text
Service
↓
Register Request
↓
Validate Registration
↓
Store Metadata
↓
Registered
```
---
# Resolution Sequence
```text
Resolve Request
↓
Lookup Registry
↓
Resolve Service
↓
Return Reference
```
---
# Unregister Sequence
```text
Shutdown
↓
Remove Service
↓
Update Registry
↓
Completed
```
---
# Runtime Rules
1. Registration Registry orqali amalga oshiriladi.
2. Resolve Registry orqali bajariladi.
3. Har bir Service noyob bo'lishi kerak.
4. Registry State yangilanadi.
5. Circular Registration taqiqlanadi.
---
# State Flow
```text
Idle
↓
Initializing
↓
Ready
↓
Registering
↓
Resolving
↓
Updating
↓
Completed
or
Failed
```
---
# Summary
Canonical Runtime Sequence:
Register
↓
Registry
↓
Resolve
↓
Runtime
