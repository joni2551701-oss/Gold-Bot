# Replay
Status: BLUEPRINT
---
# Purpose
Replay GoldBot Chart Layer ichidagi Canonical Replay moduli hisoblanadi.
Historical Replay, Simulation va Playback'ni boshqaruvchi Canonical Chart Replay moduli.
Replay Signal yaratmaydi.
Replay BOS/CHoCH hisoblamaydi.
Replay AI ishlatmaydi.
Replay Risk hisoblamaydi.
---
# Objective
Replay quyidagi vazifalarni bajaradi.
• Historical Replay
• Playback Control
• Replay Speed Management
• Simulation Support
---
# Layer Position
```text
Chart_API
↓
Replay
↓
Chart_Data
```
---
# Responsibilities
Replay
✓ Tarixiy ma'lumotlarni Replay rejimida qayta ijro etadi
✓ Playback tezligini boshqaradi
✓ Simulation Session yaratadi
---
# Not Responsible
Replay
✗ Live Trading
✗ Signal Generation
✗ Decision Making
✗ Trade Execution
✗ Real Order Placement
---
# Input
Replay qabul qiladi.
• Historical Candles
• Replay Configuration
• Playback Command
---
# Output
Replay yaratadi.
• Replay Candle Stream
• Replay State
• Playback Metadata
---
# Workflow
```text
Chart_API
↓
Replay
↓
Chart_Data
```
---
# Internal Modules (Planned — Foundation Freeze'dan keyin implementatsiya qilinadi)
```text
Replay
├── Playback/
├── ReplayEngine/
├── ReplayControls/
├── Speed/
└── Simulation/
```
---
# Golden Rules
1. Replay faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Modules
```text
Replay/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
Predecessor: Chart_API · Successor: Chart_Data
---
# Summary
Replay GoldBot Chart Layer ichidagi Replay vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, yuqoridagi Internal Modules ro'yxati Foundation Freeze'dan keyin haqiqiy implementatsiya bilan to'ldiriladi.
