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
Shared Render State / Chart State
↓
Alerts
↓
Chart_API (Exit)
```
---
# Processing Pipeline (Planned)
```text
PriceAlerts → IndicatorAlerts → DrawingAlerts → TimeAlerts → AlertManager
```
---
# Dependency Map
```text
Shared Render State / Chart State
↓
Alerts
↓
Chart_API (Exit)
```
---
# Allowed Dependencies
✓ Analysis_Overlay
✓ Drawing_Tools
✓ Chart_Data
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
Watch Render State / Chart State
↓
Process (Alerts)
↓
Emit Output
↓
Chart_API (Exit)
```
---
# Summary
Alerts GoldBot Chart Layer ichidagi Alerts moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
