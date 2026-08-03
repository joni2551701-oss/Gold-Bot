# Drawing Tools
Status: BLUEPRINT
---
# Purpose
Drawing_Tools GoldBot Chart Layer ichidagi Canonical Drawing Tools moduli hisoblanadi.
Trend Line, Ray, Rectangle, Fibonacci, Text, Brush va boshqa chizish vositalarini boshqaruvchi Canonical Drawing moduli.
Drawing_Tools Signal yaratmaydi.
Drawing_Tools BOS/CHoCH hisoblamaydi.
Drawing_Tools AI ishlatmaydi.
Drawing_Tools Risk hisoblamaydi.
---
# Objective
Drawing_Tools quyidagi vazifalarni bajaradi.
• Trend Line Drawing
• Shape Drawing
• Fibonacci Drawing
• Text Annotation
• Brush Drawing
• Drawing Persistence
---
# Layer Position
```text
Objects
↓
Drawing_Tools
↓
Indicators
```
---
# Responsibilities
Drawing_Tools
✓ Foydalanuvchi chizgan Drawing Tool'larni yaratadi
✓ Drawing Object'larni boshqaradi
✓ Drawing State'ni saqlaydi
---
# Not Responsible
Drawing_Tools
✗ Rendering
✗ Signal Generation
✗ BOS/CHoCH Calculation
✗ AI Analysis
✗ Object Rendering (Chart_Renderer vazifasi)
---
# Input
Drawing_Tools qabul qiladi.
• Drawing Request
• Interaction Context
• Coordinate Data
---
# Output
Drawing_Tools yaratadi.
• Drawing Object
• Drawing State
• Drawing Metadata
---
# Workflow
```text
Objects
↓
Drawing_Tools
↓
Indicators
```
---
# Internal Modules (Planned — Foundation Freeze'dan keyin implementatsiya qilinadi)
```text
Drawing_Tools
├── TrendLine/
├── HorizontalLine/
├── VerticalLine/
├── Ray/
├── Rectangle/
├── Circle/
├── Path/
├── Brush/
├── Arrow/
├── Text/
├── Fibonacci/
├── Pitchfork/
└── Gann/
```
---
# Golden Rules
1. Drawing_Tools faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Modules
```text
Drawing_Tools/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
Predecessor: Objects · Successor: Indicators
---
# Summary
Drawing_Tools GoldBot Chart Layer ichidagi Drawing Tools vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, yuqoridagi Internal Modules ro'yxati Foundation Freeze'dan keyin haqiqiy implementatsiya bilan to'ldiriladi.
