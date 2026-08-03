# Layout
Status: BLUEPRINT
---
# Purpose
Layout GoldBot Chart Layer ichidagi Canonical Layout moduli hisoblanadi.
Multi-Chart (1/2/4/6/8/16) Layout'larni boshqaruvchi Canonical Layout moduli.
Layout Signal yaratmaydi.
Layout BOS/CHoCH hisoblamaydi.
Layout AI ishlatmaydi.
Layout Risk hisoblamaydi.
---
# Objective
Layout quyidagi vazifalarni bajaradi.
• Single Chart Layout
• Split Chart Layout
• Grid Layout
• Chart Synchronization
• Workspace Layout Management
---
# Layer Position
```text
Chart_API
↓
Layout
↓
Chart_Core
```
---
# Responsibilities
Layout
✓ Bir nechta Chart'ni Grid ko'rinishida joylashtiradi
✓ Chart'lar orasidagi Sync'ni boshqaradi
---
# Not Responsible
Layout
✗ Rendering
✗ Signal Generation
✗ Data Calculation
✗ AI Analysis
---
# Input
Layout qabul qiladi.
• Layout Request
• Chart Instances
---
# Output
Layout yaratadi.
• Layout Grid
• Sync State
• Layout Metadata
---
# Workflow
```text
Chart_API
↓
Layout
↓
Chart_Core
```
---
# Internal Modules (Planned — Foundation Freeze'dan keyin implementatsiya qilinadi)
```text
Layout
├── SingleChart/
├── SplitChart/
├── Grid/
├── Sync/
└── WorkspaceManager/
```
---
# Golden Rules
1. Layout faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Modules
```text
Layout/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
Predecessor: Chart_API · Successor: Chart_Core
---
# Summary
Layout GoldBot Chart Layer ichidagi Layout vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, yuqoridagi Internal Modules ro'yxati Foundation Freeze'dan keyin haqiqiy implementatsiya bilan to'ldiriladi.
