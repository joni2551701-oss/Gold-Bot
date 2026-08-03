# Replay Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Replay modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Replay quyidagilar uchun javobgar.
✓ Historical Replay
✓ Playback Control
✓ Replay Speed Management
✓ Simulation Support
Replay bajarmaydi.
✗ Live Trading
✗ Signal Generation
✗ Decision Making
✗ Trade Execution
✗ Real Order Placement
---
# Module Boundary
```text
Chart_API
↓
Replay
↓
Chart_Data
```
---
# Input Contract
• Historical Candles
• Replay Configuration
• Playback Command
---
# Output Contract
• Replay Candle Stream
• Replay State
• Playback Metadata
---
# Allowed Dependencies
✓ Chart_API
✓ Chart_Data
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
# Public API (Blueprint — imzolar implementatsiya bosqichida aniqlanadi)
```text
getReplayState()
subscribeReplayEvent(callback)
configureReplay(options)
disposeReplay()
```
---
# Architecture Rules
Replay:
✓ Historical Replay bajaradi.
✓ Module Boundary'ni saqlaydi.
Replay:
✗ Signal yoki Decision yaratmaydi.
✗ BOS/CHoCH/FVG/Liquidity hisoblamaydi.
✗ AI ishlatmaydi.
---
# Runtime Rules
1. Replay faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Replay Signal yoki Decision yaratmaydi.
5. Replay BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Historical Replay bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Replay Contract GoldBot Chart Layer ichidagi Replay jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
