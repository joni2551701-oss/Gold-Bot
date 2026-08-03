# Screenshot
Status: BLUEPRINT
---
# Purpose
Screenshot GoldBot Chart Layer ichidagi Canonical Screenshot moduli hisoblanadi.
PNG, JPG va PDF formatida Chart Export qiluvchi Canonical Export moduli.
Screenshot Signal yaratmaydi.
Screenshot BOS/CHoCH hisoblamaydi.
Screenshot AI ishlatmaydi.
Screenshot Risk hisoblamaydi.
---
# Objective
Screenshot quyidagi vazifalarni bajaradi.
• PNG Export
• JPG Export
• PDF Export
• Export Management
---
# Layer Position
```text
Alerts
↓
Screenshot
↓
Chart_API
```
---
# Responsibilities
Screenshot
✓ Chart'ni rasm sifatida eksport qiladi
✓ Export formatlarini boshqaradi
---
# Not Responsible
Screenshot
✗ Rendering Logic
✗ Signal Generation
✗ Data Calculation
✗ AI Analysis
---
# Input
Screenshot qabul qiladi.
• Rendered Frame
• Export Configuration
---
# Output
Screenshot yaratadi.
• Export File
• Export Status
• Export Metadata
---
# Golden Rules
1. Screenshot faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Screenshot/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Screenshot GoldBot Chart Layer ichidagi Screenshot vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, implementatsiya uchun ichki papkalar (submodules) keyingi bosqichda qo'shiladi.
