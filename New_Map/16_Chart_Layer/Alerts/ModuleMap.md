# Alerts Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Alerts ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Internal Architecture (Planned)
```text
Alerts
        ├── PriceAlerts
        ├── IndicatorAlerts
        ├── DrawingAlerts
        ├── TimeAlerts
        └── AlertManager
```
---
# Module Position
```text
Analysis_Overlay
↓
Alerts
↓
Screenshot
```
---
# Processing Pipeline (Planned)
```text
PriceAlerts → IndicatorAlerts → DrawingAlerts → TimeAlerts → AlertManager
```
---
# Dependency Map
```text
Analysis_Overlay
↓
Alerts
↓
Screenshot
```
---
# Allowed Dependencies
✓ Analysis_Overlay
✓ Screenshot
✓ Drawing_Tools
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
Process (Alerts)
↓
Emit Output
↓
Screenshot
```
---
# Summary
Alerts GoldBot Chart Layer ichidagi Alerts moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
