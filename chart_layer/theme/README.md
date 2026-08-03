# Theme
Status: BLUEPRINT
---
# Purpose
Theme GoldBot Chart Layer ichidagi Canonical Theme moduli hisoblanadi.
Dark, Light va Custom Theme'larni boshqaruvchi Canonical Theme moduli.
Theme Signal yaratmaydi.
Theme BOS/CHoCH hisoblamaydi.
Theme AI ishlatmaydi.
Theme Risk hisoblamaydi.
---
# Objective
Theme quyidagi vazifalarni bajaradi.
• Dark Theme
• Light Theme
• Custom Theme
• Font Management
• Color Management
---
# Layer Position
```text
Chart_API
↓
Theme
↓
Chart_Renderer
```
---
# Responsibilities
Theme
✓ Chart ko'rinishi uchun Theme'ni boshqaradi
✓ Rang va Font sozlamalarini taqdim etadi
---
# Not Responsible
Theme
✗ Rendering Logic
✗ Signal Generation
✗ Data Calculation
✗ AI Analysis
---
# Input
Theme qabul qiladi.
• Theme Request
• Theme Configuration
---
# Output
Theme yaratadi.
• Theme Context
• Color Palette
• Font Settings
---
# Workflow
```text
Chart_API
↓
Theme
↓
Chart_Renderer
```
---
# Internal Modules (Planned — Foundation Freeze'dan keyin implementatsiya qilinadi)
```text
Theme
├── Dark/
├── Light/
├── Custom/
├── Fonts/
└── Colors/
```
---
# Golden Rules
1. Theme faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Modules
```text
Theme/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
Predecessor: Chart_API · Successor: Chart_Renderer
---
# Summary
Theme GoldBot Chart Layer ichidagi Theme vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, yuqoridagi Internal Modules ro'yxati Foundation Freeze'dan keyin haqiqiy implementatsiya bilan to'ldiriladi.
