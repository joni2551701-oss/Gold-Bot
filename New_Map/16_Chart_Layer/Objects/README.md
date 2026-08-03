# Objects
Status: BLUEPRINT
---
# Purpose
Objects GoldBot Chart Layer ichidagi Canonical Objects moduli hisoblanadi.
Candle, Line, Label, Shape va Overlay obyektlarini boshqaruvchi Canonical Object Model moduli.
Objects Signal yaratmaydi.
Objects BOS/CHoCH hisoblamaydi.
Objects AI ishlatmaydi.
Objects Risk hisoblamaydi.
---
# Objective
Objects quyidagi vazifalarni bajaradi.
• Candle Object Management
• Shape Object Management
• Text Object Management
• Drawing Object Management
• Overlay Object Management
• Object Lifecycle
---
# Layer Position
```text
Chart_Interaction
↓
Objects
↓
Shared Render State
```
Objects execution order jihatidan Chart_Interaction'dan keyin keladi, lekin Drawing_Tools/Indicators/Analysis_Overlay'ning natijasini Input sifatida olmaydi — bu modullar bilan ownership yoki token-passing bog'liqligi yo'q (qarang: Chart Shared State Rule, `Layer_Contracts.md`).
---
# Responsibilities
Objects
✓ Barcha Chart obyektlarini (Candle, Line, Shape, Text, Overlay) yagona Object Model sifatida boshqaradi
✓ Object Lifecycle'ni nazorat qiladi
✓ Shared Render State'ni o'z Object Model bilan yangilaydi
---
# Not Responsible
Objects
✗ Rendering (Chart_Renderer vazifasi)
✗ Signal Generation
✗ Data Calculation
✗ AI Analysis
---
# Input
Objects qabul qiladi.
• Interaction Context (Chart_Interaction)
• Chart Data (Chart_Data)
• Chart State (Chart_Core)
---
# Output
Objects yaratadi (Shared Render State'ga yozadi).
• Object List
• Object State
• Object Metadata
---
# Workflow
```text
Chart_Interaction
↓
Objects
↓
Shared Render State
```
---
# Internal Modules (Planned — Foundation Freeze'dan keyin implementatsiya qilinadi)
```text
Objects
├── CandleObject/
├── ShapeObject/
├── TextObject/
├── DrawingObject/
├── OverlayObject/
└── ObjectManager/
```
---
# Golden Rules
1. Objects faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Modules
```text
Objects/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
Execution Order: after Chart_Interaction · writes to Shared Render State (read by Drawing_Tools, Indicators, Analysis_Overlay, Chart_Renderer)
---
# Summary
Objects GoldBot Chart Layer ichidagi Objects vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, yuqoridagi Internal Modules ro'yxati Foundation Freeze'dan keyin haqiqiy implementatsiya bilan to'ldiriladi.
