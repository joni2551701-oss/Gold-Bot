# Rule Engine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat RuleEngine ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
DecisionConfidence
↓
RuleEngine
↓
ApprovalEngine
```
---
# Module Architecture
```text
RuleEngine
        │
        ├── Rule Loader
        ├── Trading Rule Validator
        ├── Risk Rule Validator
        ├── Session Rule Validator
        ├── Safety Rule Validator
        ├── Rule Report Builder
        └── Metadata Generator
```
---
# Internal Components
## Rule Loader
Faol Rule to'plamini yuklaydi.
---
## Trading Rule Validator
Trading qoidalarini tekshiradi.
---
## Risk Rule Validator
Risk bilan bog'liq qoidalarni tekshiradi.
---
## Session Rule Validator
Session va vaqt qoidalarini tekshiradi.
---
## Safety Rule Validator
Xavfsizlik va Business Rule'larni tekshiradi.
---
## Rule Report Builder
Yakuniy Rule Report yaratadi.
---
## Metadata Generator
Rule Metadata yaratadi.
---
# Typical Rules
• News Lock
• Spread Filter
• Session Filter
• Weekend Filter
• Holiday Filter
• RR Filter
• Max Drawdown
• Daily Loss Limit
• Max Open Trades
• Symbol Permission
---
# Allowed Dependencies
✓ DecisionConfidence
✓ ApprovalEngine
---
# Forbidden Dependencies
✗ DecisionEngine
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
---
# Summary
RuleEngine GoldBot ichidagi barcha Trading Rule Validation jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
