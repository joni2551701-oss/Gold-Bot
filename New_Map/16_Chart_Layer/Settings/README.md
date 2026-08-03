# Settings
Status: BLUEPRINT
---
# Purpose
Settings GoldBot Chart Layer ichidagi Canonical Settings moduli hisoblanadi.
Grid, Scale, Price Axis, Time Axis va Behavior sozlamalarini boshqaruvchi Canonical Settings moduli.
Settings Signal yaratmaydi.
Settings BOS/CHoCH hisoblamaydi.
Settings AI ishlatmaydi.
Settings Risk hisoblamaydi.
---
# Objective
Settings quyidagi vazifalarni bajaradi.
• Grid Settings
• Price Scale Settings
• Time Scale Settings
• Behaviour Settings
• Magnet Settings
• Auto Scale Settings
---
# Layer Position
```text
Chart_API
↓
Settings
↓
Chart_Core
```
---
# Responsibilities
Settings
✓ Chart sozlamalarini boshqaradi
✓ Grid/Scale/Axis konfiguratsiyasini taqdim etadi
---
# Not Responsible
Settings
✗ Rendering Logic
✗ Signal Generation
✗ Data Calculation
✗ AI Analysis
---
# Input
Settings qabul qiladi.
• Settings Request
• User Preferences
---
# Output
Settings yaratadi.
• Settings Context
• Scale Configuration
• Behaviour Configuration
---
# Golden Rules
1. Settings faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Settings/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Settings GoldBot Chart Layer ichidagi Settings vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, implementatsiya uchun ichki papkalar (submodules) keyingi bosqichda qo'shiladi.
