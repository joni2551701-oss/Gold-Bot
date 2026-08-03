# Analysis Overlay
Status: BLUEPRINT
---
# Purpose
Analysis_Overlay GoldBot Chart Layer ichidagi Canonical Analysis Overlay moduli hisoblanadi.
GoldBot Core hisoblagan BOS, CHoCH, Order Block, FVG, Liquidity, Wyckoff, AMD natijalarini vizual tarzda chizuvchi Canonical Overlay moduli. Hech qanday tahlil hisoblamaydi — faqat chizadi.
Analysis_Overlay Signal yaratmaydi.
Analysis_Overlay BOS/CHoCH hisoblamaydi.
Analysis_Overlay AI ishlatmaydi.
Analysis_Overlay Risk hisoblamaydi.
---
# Objective
Analysis_Overlay quyidagi vazifalarni bajaradi.
• Market Structure Visualization
• BOS/CHoCH Visualization
• Order Block Visualization
• FVG Visualization
• Liquidity Visualization
• Wyckoff Visualization
• AMD Visualization
• Premium/Discount Visualization
• Session Visualization
---
# Layer Position
```text
Indicators
↓
Analysis_Overlay
↓
Alerts
```
---
# Responsibilities
Analysis_Overlay
✓ Chart_API orqali GoldBot Core'dan kelgan Context/Signal/Decision natijalarini qabul qiladi
✓ Ularni vizual Overlay obyektlariga aylantiradi
✓ Chart_Renderer'ga uzatadi
---
# Not Responsible
Analysis_Overlay
✗ BOS/CHoCH Calculation
✗ Order Block Calculation
✗ FVG Calculation
✗ Liquidity Calculation
✗ Signal Generation
✗ AI Analysis
✗ Risk Calculation
✗ Trade Execution
---
# Input
Analysis_Overlay qabul qiladi.
• Indicator Overlay Data
• Market Context (Chart_API'dan)
• Signal (Chart_API'dan)
• Decision (Chart_API'dan)
---
# Output
Analysis_Overlay yaratadi.
• Overlay Object
• Overlay State
• Overlay Metadata
---
# Golden Rules
1. Analysis_Overlay faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Analysis_Overlay/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Analysis_Overlay GoldBot Chart Layer ichidagi Analysis Overlay vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, implementatsiya uchun ichki papkalar (submodules) keyingi bosqichda qo'shiladi.
