# Replay Controller
Status: CANONICAL
---
# Purpose
ReplayController GoldBot Backtesting Layer ichidagi Canonical Replay Session Management moduli hisoblanadi.
Uning asosiy vazifasi bir nechta Replay sessiyasini session_id bo'yicha ochish, boshqarish va yopishdir.
ReplayController candle'larni o'zi uzatmaydi — bu ReplayEngine vazifasi.
---
# Objective
ReplayController quyidagi vazifalarni bajaradi.
• Session Lifecycle Management
• Multi Session Isolation
• Session State Tracking
• Playback Control (start/pause/resume/stop/restart/step)
• Session Status Reporting
---
# Layer Position
```text
BacktestService
↓
ReplayController
↓
ReplayEngine
```
---
# Responsibilities
ReplayController
✓ Replay sessiyalarini session_id bo'yicha ochadi va yopadi
✓ Har bir sessiya uchun alohida ReplayEngine yuritadi
✓ start/pause/resume/stop/restart/step buyruqlarini bajaradi
✓ Sessiya holatini qaytaradi
---
# Not Responsible
ReplayController
✗ Candle Traversal (ReplayEngine vazifasi)
✗ Market Analysis
✗ Trade Simulation
✗ Report Formatting
---
# Input
ReplayController qabul qiladi.
• Session Command
• Session Identifier
• Replay Configuration
---
# Output
ReplayController yaratadi.
• Session Status
• Replay Result
• Session Metadata
---
# Workflow
```text
BacktestService
↓
ReplayController
↓
ReplayEngine
```
---
# Internal Modules (Planned — implementatsiya bosqichida to'ldiriladi)
```text
ReplayController
├── SessionManager
├── SessionRegistry
└── PlaybackCommands
```
---
# Golden Rules
1. Har bir Replay sessiyasi session_id bilan izolyatsiya qilinadi.
2. Bir sessiya boshqasining holatiga ta'sir qilmaydi.
3. ReplayController candle uzatmaydi — faqat sessiyani boshqaradi.
4. Sessiya yopilganda resurslar bo'shatiladi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
ReplayController/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
ReplayController Replay sessiyalarini boshqaruvchi Canonical Session Management moduli hisoblanadi.
