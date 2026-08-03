# Chart Core
Status: BLUEPRINT
---
# Purpose
Chart_Core GoldBot Chart Layer ichidagi Canonical Chart Core moduli hisoblanadi.
ChartEngine, Lifecycle, State, Camera, Coordinate System va Viewport'ni boshqaruvchi Canonical Chart Orchestrator moduli.
Chart_Core Signal yaratmaydi.
Chart_Core BOS/CHoCH hisoblamaydi.
Chart_Core AI ishlatmaydi.
Chart_Core Risk hisoblamaydi.
---
# Objective
Chart_Core quyidagi vazifalarni bajaradi.
• Chart Lifecycle Management
• Chart State Management
• Camera Control
• Coordinate System Management
• Viewport Management
• Module Coordination
---
# Layer Position
```text
Chart_API
↓
Chart_Core
↓
Chart_Data
```
---
# Responsibilities
Chart_Core
✓ Chart Engine'ni ishga tushiradi
✓ Chart State'ni boshqaradi
✓ Camera pozitsiyasini boshqaradi
✓ Coordinate System'ni hisoblaydi
✓ Viewport chegaralarini boshqaradi
✓ Ichki modullarni koordinatsiya qiladi
---
# Not Responsible
Chart_Core
✗ Rendering
✗ Data Fetching
✗ Signal Generation
✗ BOS/CHoCH Calculation
✗ AI Analysis
✗ Risk Calculation
---
# Input
Chart_Core qabul qiladi.
• Chart Request
• Chart Configuration
• Symbol
• Timeframe
---
# Output
Chart_Core yaratadi.
• Chart Instance
• Chart State
• Viewport Context
• Camera Context
---
# Golden Rules
1. Chart_Core faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Chart_Core/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Chart_Core GoldBot Chart Layer ichidagi Chart Core vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, implementatsiya uchun ichki papkalar (submodules) keyingi bosqichda qo'shiladi.
