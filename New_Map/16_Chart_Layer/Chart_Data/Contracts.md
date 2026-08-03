# Chart Data Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_Data modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Chart_Data quyidagilar uchun javobgar.
✓ Candle Data Management
✓ Tick Data Management
✓ OHLCV Aggregation
✓ Volume Data Management
✓ Session Data Management
✓ Symbol Data Cache
Chart_Data bajarmaydi.
✗ Rendering
✗ Indicator Calculation
✗ Signal Generation
✗ BOS/CHoCH Calculation
✗ Historical Data Fetching (GoldBot Core vazifasi)
---
# Module Boundary
```text
Chart_Core
↓
Chart_Data
↓
Chart_Renderer
```
---
# Input Contract
• Historical Candles (GoldBot Core'dan)
• Live Candle Stream
• Symbol Info
• Timeframe
---
# Output Contract
• Candle Data
• Tick Data
• OHLCV
• Session Data
• Symbol Cache
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
# Runtime Contract
1. Chart_Data faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Chart_Data Signal yoki Decision yaratmaydi.
5. Chart_Data BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Candle Data Management bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Chart_Data Contract GoldBot Chart Layer ichidagi Chart Data jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
