# Chart Data Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_Data ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Internal Architecture (Planned)
```text
Chart_Data
        ├── CandleData
        ├── TickData
        ├── OHLCV
        ├── VolumeData
        ├── SessionData
        ├── SymbolData
        └── DataCache
```
---
# Module Position
```text
Chart_Core
↓
Chart_Data
↓
Chart_Renderer
```
---
# Processing Pipeline (Planned)
```text
CandleData → TickData → OHLCV → VolumeData → SessionData → SymbolData → DataCache
```
---
# Dependency Map
```text
Chart_Core
↓
Chart_Data
↓
Chart_Renderer
```
---
# Allowed Dependencies
✓ Chart_Core
✓ Chart_Renderer
✓ Replay
✓ Timeframe
✓ Symbols
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
Process (Chart_Data)
↓
Emit Output
↓
Chart_Renderer
```
---
# Summary
Chart_Data GoldBot Chart Layer ichidagi Chart Data moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
