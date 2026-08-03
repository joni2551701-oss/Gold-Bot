# Screenshot Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Screenshot modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Screenshot quyidagilar uchun javobgar.
✓ PNG Export
✓ JPG Export
✓ PDF Export
✓ Export Management
Screenshot bajarmaydi.
✗ Rendering Logic
✗ Signal Generation
✗ Data Calculation
✗ AI Analysis
---
# Module Boundary
```text
Alerts
↓
Screenshot
↓
Chart_API
```
---
# Input Contract
• Rendered Frame
• Export Configuration
---
# Output Contract
• Export File
• Export Status
• Export Metadata
---
# Allowed Dependencies
✓ Alerts
✓ Chart_API
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
1. Screenshot faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Screenshot Signal yoki Decision yaratmaydi.
5. Screenshot BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ PNG Export bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Screenshot Contract GoldBot Chart Layer ichidagi Screenshot jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
