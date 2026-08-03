# Layout Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Layout modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Layout quyidagilar uchun javobgar.
✓ Single Chart Layout
✓ Split Chart Layout
✓ Grid Layout
✓ Chart Synchronization
✓ Workspace Layout Management
Layout bajarmaydi.
✗ Rendering
✗ Signal Generation
✗ Data Calculation
✗ AI Analysis
---
# Module Boundary
```text
Chart_API
↓
Layout
↓
Chart_Core
```
---
# Input Contract
• Layout Request
• Chart Instances
---
# Output Contract
• Layout Grid
• Sync State
• Layout Metadata
---
# Allowed Dependencies
✓ Chart_API
✓ Chart_Core
✓ Templates
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
1. Layout faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Layout Signal yoki Decision yaratmaydi.
5. Layout BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Single Chart Layout bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Layout Contract GoldBot Chart Layer ichidagi Layout jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
