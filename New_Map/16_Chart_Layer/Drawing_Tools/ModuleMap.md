# Drawing Tools Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Drawing_Tools ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Internal Architecture (Planned)
```text
Drawing_Tools
        ├── TrendLine
        ├── HorizontalLine
        ├── VerticalLine
        ├── Ray
        ├── Rectangle
        ├── Circle
        ├── Path
        ├── Brush
        ├── Arrow
        ├── Text
        ├── Fibonacci
        ├── Pitchfork
        └── Gann
```
---
# Module Position
```text
Objects
↓
Drawing_Tools
↓
Indicators
```
---
# Processing Pipeline (Planned)
```text
TrendLine → HorizontalLine → VerticalLine → Ray → Rectangle → Circle → Path → Brush → Arrow → Text → Fibonacci → Pitchfork → Gann
```
---
# Dependency Map
```text
Objects
↓
Drawing_Tools
↓
Indicators
```
---
# Allowed Dependencies
✓ Objects
✓ Indicators
✓ Templates
✓ Alerts
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
Process (Drawing_Tools)
↓
Emit Output
↓
Indicators
```
---
# Summary
Drawing_Tools GoldBot Chart Layer ichidagi Drawing Tools moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
