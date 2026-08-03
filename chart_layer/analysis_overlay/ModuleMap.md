# Analysis Overlay Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Analysis_Overlay ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Internal Architecture (Planned)
```text
Analysis_Overlay
        ├── MarketStructure
        ├── BOS
        ├── CHoCH
        ├── Liquidity
        ├── OrderBlock
        ├── FVG
        ├── Wyckoff
        ├── AMD
        ├── PremiumDiscount
        └── Sessions
```
---
# Module Position
```text
Indicators
↓
Analysis_Overlay
↓
Alerts
```
---
# Processing Pipeline (Planned)
```text
MarketStructure → BOS → CHoCH → Liquidity → OrderBlock → FVG → Wyckoff → AMD → PremiumDiscount → Sessions
```
---
# Dependency Map
```text
Indicators
↓
Analysis_Overlay
↓
Alerts
```
---
# Allowed Dependencies
✓ Indicators
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
Process (Analysis_Overlay)
↓
Emit Output
↓
Alerts
```
---
# Summary
Analysis_Overlay GoldBot Chart Layer ichidagi Analysis Overlay moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
