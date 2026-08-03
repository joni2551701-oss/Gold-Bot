# Templates Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Templates modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Templates quyidagilar uchun javobgar.
✓ Workspace Management
✓ Layout Presets
✓ Indicator Set Presets
✓ Drawing Set Presets
Templates bajarmaydi.
✗ Rendering
✗ Signal Generation
✗ Data Calculation
✗ AI Analysis
---
# Module Boundary
```text
Chart_API
↓
Templates
↓
Chart_Core
```
---
# Input Contract
• Template Request
• Workspace Configuration
---
# Output Contract
• Template
• Workspace State
• Preset Metadata
---
# Allowed Dependencies
✓ Chart_API
✓ Chart_Core
✓ Layout
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
1. Templates faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Templates Signal yoki Decision yaratmaydi.
5. Templates BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Workspace Management bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Templates Contract GoldBot Chart Layer ichidagi Templates jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
