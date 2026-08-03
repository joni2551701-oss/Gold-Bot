# Crosshair
Status: BLUEPRINT
---
# Purpose
Crosshair GoldBot Chart Layer ichidagi Canonical Crosshair moduli hisoblanadi.
Cursor, OHLC Tooltip va Magnet funksiyasini boshqaruvchi Canonical Crosshair moduli.
Crosshair Signal yaratmaydi.
Crosshair BOS/CHoCH hisoblamaydi.
Crosshair AI ishlatmaydi.
Crosshair Risk hisoblamaydi.
---
# Objective
Crosshair quyidagi vazifalarni bajaradi.
• Cursor Tracking
• Magnet Snapping
• OHLC Tooltip
• Price Label
• Time Label
---
# Layer Position
```text
Chart_Interaction
↓
Crosshair
↓
Chart_Renderer
```
---
# Responsibilities
Crosshair
✓ Cursor pozitsiyasini kuzatadi
✓ Magnet orqali eng yaqin Candle'ga tortadi
✓ OHLC Tooltip ko'rsatadi
---
# Not Responsible
Crosshair
✗ Rendering Logic
✗ Signal Generation
✗ Data Calculation
✗ AI Analysis
---
# Input
Crosshair qabul qiladi.
• Interaction Context
• Candle Data
---
# Output
Crosshair yaratadi.
• Crosshair Position
• Tooltip Content
• Price Label
• Time Label
---
# Workflow
```text
Chart_Interaction
↓
Crosshair
↓
Chart_Renderer
```
---
# Internal Modules (Planned — Foundation Freeze'dan keyin implementatsiya qilinadi)
```text
Crosshair
├── Cursor/
├── Magnet/
├── Tooltip/
├── PriceLabel/
└── TimeLabel/
```
---
# Golden Rules
1. Crosshair faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Modules
```text
Crosshair/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
Predecessor: Chart_Interaction · Successor: Chart_Renderer
---
# Summary
Crosshair GoldBot Chart Layer ichidagi Crosshair vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, yuqoridagi Internal Modules ro'yxati Foundation Freeze'dan keyin haqiqiy implementatsiya bilan to'ldiriladi.
