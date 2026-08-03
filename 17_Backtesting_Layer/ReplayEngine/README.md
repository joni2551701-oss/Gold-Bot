# Replay Engine
Status: CANONICAL
---
# Purpose
ReplayEngine GoldBot Backtesting Layer ichidagi Canonical Replay moduli hisoblanadi.
Uning asosiy vazifasi tarixiy candle'larni saqlanadigan manbadan yuklab, ularni bosqichma-bosqich (step) uzatishdir.
ReplayEngine Clock (play/pause/stop/speed/seek) va Feed (candle traversal) komponentlarini birlashtiradi.
ReplayEngine hech qanday tahlil bajarmaydi.
---
# Objective
ReplayEngine quyidagi vazifalarni bajaradi.
• Historical Candle Loading
• Replay Clock Management
• Candle Traversal
• Step Execution
• Replay State Management
---
# Layer Position
```text
DataFeed
↓
ReplayEngine
↓
Historical Data (Database Layer, read-only)
```
---
# Responsibilities
ReplayEngine
✓ Tarixiy candle oynasini bir marta yuklaydi
✓ ReplayClock orqali play/pause/stop/speed/seek holatini boshqaradi
✓ ReplayFeed orqali candle'larni birma-bir uzatadi
✓ Replay holatini (State) saqlaydi
---
# Not Responsible
ReplayEngine
✗ Market Analysis
✗ Signal Generation
✗ Trade Simulation (BacktestEngine vazifasi)
✗ Session Management (ReplayController vazifasi)
✗ Real Data Writing
---
# Input
ReplayEngine qabul qiladi.
• Replay Configuration
• Historical Candles (Database Layer'dan, read-only)
---
# Output
ReplayEngine yaratadi.
• Candle Stream
• Replay State
• Replay Position
• Replay Metadata
---
# Workflow
```text
DataFeed
↓
ReplayEngine
↓
Historical Data (Database Layer, read-only)
```
---
# Internal Modules (Planned — implementatsiya bosqichida to'ldiriladi)
```text
ReplayEngine
├── ReplayClock
├── ReplayFeed
├── ReplayLoader
└── ReplayState
```
---
# Golden Rules
1. ReplayEngine tarixiy ma'lumotni faqat o'qiydi — hech qachon yozmaydi.
2. Candle oynasi bir marta yuklanadi.
3. Replay bosqichma-bosqich (step) bajariladi.
4. ReplayEngine tahlil bajarmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
ReplayEngine/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
ReplayEngine tarixiy candle'larni bosqichma-bosqich uzatuvchi Canonical Replay moduli hisoblanadi.
