# Chart Renderer Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_Renderer modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Chart_Renderer quyidagilar uchun javobgar.
✓ Canvas Rendering
✓ WebGL Rendering
✓ Layer Rendering
✓ Viewport Rendering
✓ Render Pipeline Management
Chart_Renderer bajarmaydi.
✗ Data Calculation
✗ Indicator Calculation
✗ Signal Generation
✗ BOS/CHoCH Calculation
✗ AI Analysis
✗ Risk Calculation
---
# Module Boundary
```text
Chart_Data
↓
Chart_Renderer
↓
Chart_Interaction
```
---
# Input Contract
• Candle Data
• Object List
• Overlay Data
• Theme
• Viewport Context
---
# Output Contract
• Rendered Frame
• Render Report
• Render Metadata
---
# Allowed Dependencies
✓ Chart_Data
✓ Chart_Interaction
✓ Objects
✓ Theme
✓ Crosshair
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
1. Chart_Renderer faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Chart_Renderer Signal yoki Decision yaratmaydi.
5. Chart_Renderer BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Canvas Rendering bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Chart_Renderer Contract GoldBot Chart Layer ichidagi Chart Renderer jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
