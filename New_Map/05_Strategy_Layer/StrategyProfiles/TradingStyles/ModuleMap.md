# TradingStyles Module Map
Status: CANONICAL
---
# Module Position
```text
Platform Layer
↓
TradingStyles
↓
StrategyManager
```
---
# Module Architecture
```text
TradingStyles
        │
        ├── Scalping
        ├── Intraday
        ├── Swing
        ├── Position
        ├── Configuration Loader
        └── Profile Builder
```
---
# Internal Components
## Scalping
Scalping konfiguratsiyasi.
---
## Intraday
Intraday konfiguratsiyasi.
---
## Swing
Swing konfiguratsiyasi.
---
## Position
Position konfiguratsiyasi.
---
## Configuration Loader
Trading Style konfiguratsiyasini yuklaydi.
---
## Profile Builder
Strategy Profile yaratadi.
---
# Allowed Dependencies
✓ StrategyProfiles
✓ StrategyManager
---
# Forbidden Dependencies
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer Logic
---
# Summary
TradingStyles foydalanuvchi tanlagan Trading Style konfiguratsiyasini StrategyManager uchun tayyorlaydi.
