# Chart Renderer
Status: BLUEPRINT
---
# Purpose
Chart_Renderer GoldBot Chart Layer ichidagi Canonical Chart Renderer moduli hisoblanadi.
Canvas/WebGL orqali Chart'ni chizuvchi Canonical Rendering moduli. Hisob-kitob bajarmaydi, faqat chizadi.
Chart_Renderer Signal yaratmaydi.
Chart_Renderer BOS/CHoCH hisoblamaydi.
Chart_Renderer AI ishlatmaydi.
Chart_Renderer Risk hisoblamaydi.
---
# Objective
Chart_Renderer quyidagi vazifalarni bajaradi.
• Canvas Rendering
• WebGL Rendering
• Layer Rendering
• Viewport Rendering
• Render Pipeline Management
---
# Layer Position
```text
Chart_Data
↓
Chart_Renderer
↓
Chart_Interaction
```
---
# Responsibilities
Chart_Renderer
✓ Candle'larni chizadi
✓ Overlay'larni chizadi
✓ Object'larni chizadi
✓ Render Pipeline'ni boshqaradi
✓ Frame'larni yangilaydi
---
# Not Responsible
Chart_Renderer
✗ Data Calculation
✗ Indicator Calculation
✗ Signal Generation
✗ BOS/CHoCH Calculation
✗ AI Analysis
✗ Risk Calculation
---
# Input
Chart_Renderer qabul qiladi.
• Candle Data
• Object List
• Overlay Data
• Theme
• Viewport Context
---
# Output
Chart_Renderer yaratadi.
• Rendered Frame
• Render Report
• Render Metadata
---
# Golden Rules
1. Chart_Renderer faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Chart_Renderer/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Chart_Renderer GoldBot Chart Layer ichidagi Chart Renderer vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, implementatsiya uchun ichki papkalar (submodules) keyingi bosqichda qo'shiladi.
