# Replay Controller Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat ReplayController modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
ReplayController quyidagilar uchun javobgar.
✓ Replay sessiyalarini session_id bo'yicha ochadi va yopadi
✓ Har bir sessiya uchun alohida ReplayEngine yuritadi
✓ start/pause/resume/stop/restart/step buyruqlarini bajaradi
✓ Sessiya holatini qaytaradi
ReplayController bajarmaydi.
✗ Candle Traversal (ReplayEngine vazifasi)
✗ Market Analysis
✗ Trade Simulation
✗ Report Formatting
---
# Module Boundary
```text
BacktestService
↓
ReplayController
↓
ReplayEngine
```
---
# Input Contract
• Session Command
• Session Identifier
• Replay Configuration
---
# Output Contract
• Session Status
• Replay Result
• Session Metadata
---
# Allowed Dependencies
✓ BacktestService
✓ ReplayEngine
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
1. Har bir Replay sessiyasi session_id bilan izolyatsiya qilinadi.
2. Bir sessiya boshqasining holatiga ta'sir qilmaydi.
3. ReplayController candle uzatmaydi — faqat sessiyani boshqaradi.
4. Sessiya yopilganda resurslar bo'shatiladi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Sessiya ochiladi.
✓ Playback buyruqlari bajariladi.
✓ Sessiya holati qaytariladi.
✓ Sessiya yopiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
ReplayController Contract ReplayController Replay sessiyalarini boshqaruvchi Canonical Session Management moduli hisoblanadi.
