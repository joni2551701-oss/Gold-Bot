# Chart Interaction Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_Interaction modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Chart_Interaction quyidagilar uchun javobgar.
✓ Mouse Handling
✓ Keyboard Handling
✓ Touch Handling
✓ Zoom Management
✓ Pan Management
✓ Drag Management
✓ Selection Management
✓ Hotkey Management
Chart_Interaction bajarmaydi.
✗ Rendering
✗ Data Calculation
✗ Signal Generation
✗ BOS/CHoCH Calculation
✗ Drawing Tool Logic (Drawing_Tools vazifasi)
---
# Module Boundary
```text
Chart_Renderer
↓
Chart_Interaction
↓
Objects
```
---
# Input Contract
• Mouse Event
• Keyboard Event
• Touch Event
• Gesture Event
---
# Output Contract
• Interaction Context
• Zoom State
• Pan State
• Selection State
---
# Allowed Dependencies
✓ Chart_Renderer
✓ Objects
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
1. Chart_Interaction faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Chart_Interaction Signal yoki Decision yaratmaydi.
5. Chart_Interaction BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Mouse Handling bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Chart_Interaction Contract GoldBot Chart Layer ichidagi Chart Interaction jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
