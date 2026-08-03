# Templates
Status: BLUEPRINT
---
# Purpose
Templates GoldBot Chart Layer ichidagi Canonical Templates moduli hisoblanadi.
Layout, Workspace va Preset'larni boshqaruvchi Canonical Templates moduli.
Templates Signal yaratmaydi.
Templates BOS/CHoCH hisoblamaydi.
Templates AI ishlatmaydi.
Templates Risk hisoblamaydi.
---
# Objective
Templates quyidagi vazifalarni bajaradi.
• Workspace Management
• Layout Presets
• Indicator Set Presets
• Drawing Set Presets
---
# Layer Position
```text
Chart_API
↓
Templates
↓
Chart_Core
```
---
# Responsibilities
Templates
✓ Workspace'larni saqlaydi va yuklaydi
✓ Layout Preset'larni boshqaradi
✓ Indicator/Drawing Set'larini saqlaydi
---
# Not Responsible
Templates
✗ Rendering
✗ Signal Generation
✗ Data Calculation
✗ AI Analysis
---
# Input
Templates qabul qiladi.
• Template Request
• Workspace Configuration
---
# Output
Templates yaratadi.
• Template
• Workspace State
• Preset Metadata
---
# Workflow
```text
Chart_API
↓
Templates
↓
Chart_Core
```
---
# Internal Modules (Planned — Foundation Freeze'dan keyin implementatsiya qilinadi)
```text
Templates
├── Workspace/
├── Layouts/
├── IndicatorSets/
├── DrawingSets/
└── Presets/
```
---
# Golden Rules
1. Templates faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Modules
```text
Templates/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
Predecessor: Chart_API · Successor: Chart_Core
---
# Summary
Templates GoldBot Chart Layer ichidagi Templates vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, yuqoridagi Internal Modules ro'yxati Foundation Freeze'dan keyin haqiqiy implementatsiya bilan to'ldiriladi.
