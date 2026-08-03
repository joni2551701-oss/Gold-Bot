# Indicators Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Indicators modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Indicators quyidagilar uchun javobgar.
✓ Trend Indicator Rendering Support
✓ Momentum Indicator Rendering Support
✓ Volume Indicator Rendering Support
✓ Volatility Indicator Rendering Support
✓ Custom Indicator Support
Indicators bajarmaydi.
✗ Trading Indicator Calculation (GoldBot Indicator Layer vazifasi)
✗ Signal Generation
✗ BOS/CHoCH Calculation
✗ AI Analysis
✗ Rendering
---
# Module Boundary
```text
Drawing_Tools
↓
Indicators
↓
Analysis_Overlay
```
---
# Input Contract
• Drawing Context
• Candle Data
• Indicator Selection
• Indicator Settings
---
# Output Contract
• Indicator Overlay Data
• Indicator State
• Indicator Metadata
---
# Allowed Dependencies
✓ Drawing_Tools
✓ Analysis_Overlay
✓ Plugins
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
1. Indicators faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Indicators Signal yoki Decision yaratmaydi.
5. Indicators BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Trend Indicator Rendering Support bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Indicators Contract GoldBot Chart Layer ichidagi Indicators jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
