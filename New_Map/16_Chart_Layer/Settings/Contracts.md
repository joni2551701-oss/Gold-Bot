# Settings Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Settings modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Settings quyidagilar uchun javobgar.
✓ Grid Settings
✓ Price Scale Settings
✓ Time Scale Settings
✓ Behaviour Settings
✓ Magnet Settings
✓ Auto Scale Settings
Settings bajarmaydi.
✗ Rendering Logic
✗ Signal Generation
✗ Data Calculation
✗ AI Analysis
---
# Module Boundary
```text
Chart_API
↓
Settings
↓
Chart_Core
```
---
# Input Contract
• Settings Request
• User Preferences
---
# Output Contract
• Settings Context
• Scale Configuration
• Behaviour Configuration
---
# Allowed Dependencies
✓ Chart_API
✓ Chart_Core
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
1. Settings faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Settings Signal yoki Decision yaratmaydi.
5. Settings BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Grid Settings bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Settings Contract GoldBot Chart Layer ichidagi Settings jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
