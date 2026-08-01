# TradingStyles Module Map
Status: CANONICAL
---
# Module Position
```text
Platform Layer
↓
TradingStyles
↓
StrategyEngine
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
✓ StrategyEngine
---
# Forbidden Dependencies
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
TradingStyles foydalanuvchi tanlagan Trading Style konfiguratsiyasini StrategyEngine uchun tayyorlaydi.
