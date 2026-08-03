# Screenshot Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Screenshot ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Internal Architecture (Planned)
```text
Screenshot
        ├── PNG
        ├── JPG
        ├── PDF
        └── ExportManager
```
---
# Module Position
```text
Alerts
↓
Screenshot
↓
Chart_API
```
---
# Processing Pipeline (Planned)
```text
PNG → JPG → PDF → ExportManager
```
---
# Dependency Map
```text
Alerts
↓
Screenshot
↓
Chart_API
```
---
# Allowed Dependencies
✓ Alerts
✓ Chart_API
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
Process (Screenshot)
↓
Emit Output
↓
Chart_API
```
---
# Summary
Screenshot GoldBot Chart Layer ichidagi Screenshot moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
