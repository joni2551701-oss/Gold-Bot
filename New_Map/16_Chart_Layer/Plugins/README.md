# Plugins
Status: BLUEPRINT
---
# Purpose
Plugins GoldBot Chart Layer ichidagi Canonical Plugins moduli hisoblanadi.
Tashqi Indicator va Drawing kengaytmalarini boshqaruvchi Canonical Plugin System moduli.
Plugins Signal yaratmaydi.
Plugins BOS/CHoCH hisoblamaydi.
Plugins AI ishlatmaydi.
Plugins Risk hisoblamaydi.
---
# Objective
Plugins quyidagi vazifalarni bajaradi.
• Indicator Plugin Support
• Drawing Plugin Support
• Overlay Plugin Support
• Data Plugin Support
• Plugin Lifecycle Management
---
# Layer Position
```text
Chart_API
↓
Plugins
↓
Chart_Core
```
---
# Responsibilities
Plugins
✓ Tashqi Plugin'larni ro'yxatdan o'tkazadi
✓ Plugin Lifecycle'ni boshqaradi
✓ Plugin'lar uchun xavfsiz Sandbox taqdim etadi
---
# Not Responsible
Plugins
✗ Signal Generation
✗ AI Analysis
✗ Risk Calculation
✗ Trade Execution
✗ Rendering
---
# Input
Plugins qabul qiladi.
• Plugin Registration Request
• Plugin Configuration
---
# Output
Plugins yaratadi.
• Plugin Context
• Plugin Status
• Plugin Metadata
---
# Golden Rules
1. Plugins faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Plugins/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Plugins GoldBot Chart Layer ichidagi Plugins vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, implementatsiya uchun ichki papkalar (submodules) keyingi bosqichda qo'shiladi.
