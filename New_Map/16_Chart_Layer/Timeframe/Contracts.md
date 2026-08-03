# Timeframe Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Timeframe modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Timeframe quyidagilar uchun javobgar.
✓ Timeframe Management
✓ Timeframe Aggregation
✓ Custom Timeframe
✓ Timeframe Synchronization
Timeframe bajarmaydi.
✗ Rendering
✗ Signal Generation
✗ Data Calculation (aggregation'dan boshqa)
✗ AI Analysis
---
# Module Boundary
```text
Chart_API
↓
Timeframe
↓
Chart_Data
```
---
# Input Contract
• Timeframe Request
• Raw Candle Data
---
# Output Contract
• Timeframe Context
• Aggregated Candles
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
# Runtime Contract
1. Timeframe faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Timeframe Signal yoki Decision yaratmaydi.
5. Timeframe BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Timeframe Management bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Timeframe Contract GoldBot Chart Layer ichidagi Timeframe jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
