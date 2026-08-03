# Replay Engine Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat ReplayEngine modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
ReplayEngine quyidagilar uchun javobgar.
✓ Tarixiy candle oynasini bir marta yuklaydi
✓ ReplayClock orqali play/pause/stop/speed/seek holatini boshqaradi
✓ ReplayFeed orqali candle'larni birma-bir uzatadi
✓ Replay holatini (State) saqlaydi
ReplayEngine bajarmaydi.
✗ Market Analysis
✗ Signal Generation
✗ Trade Simulation (BacktestEngine vazifasi)
✗ Session Management (ReplayController vazifasi)
✗ Real Data Writing
---
# Module Boundary
```text
DataFeed
↓
ReplayEngine
↓
Historical Data (Database Layer, read-only)
```
---
# Input Contract
• Replay Configuration
• Historical Candles (Database Layer'dan, read-only)
---
# Output Contract
• Candle Stream
• Replay State
• Replay Position
• Replay Metadata
---
# Allowed Dependencies
✓ DataFeed
✓ ReplayController
---
# Forbidden Dependencies
✗ Execution Layer (real order — Backtesting Isolation Rule)
✗ Broker Gateway
✗ Platform Layer (to'g'ridan-to'g'ri)
✗ Live Data (real vaqt oqimi)
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
---
# Runtime Contract
1. ReplayEngine tarixiy ma'lumotni faqat o'qiydi — hech qachon yozmaydi.
2. Candle oynasi bir marta yuklanadi.
3. Replay bosqichma-bosqich (step) bajariladi.
4. ReplayEngine tahlil bajarmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Tarixiy candle yuklanadi.
✓ Clock holati boshqariladi.
✓ Candle birma-bir uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
ReplayEngine Contract ReplayEngine tarixiy candle'larni bosqichma-bosqich uzatuvchi Canonical Replay moduli hisoblanadi.
