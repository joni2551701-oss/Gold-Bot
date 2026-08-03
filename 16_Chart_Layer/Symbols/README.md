# Symbols
Status: BLUEPRINT
---
# Purpose
Symbols GoldBot Chart Layer ichidagi Canonical Symbols moduli hisoblanadi.
XAUUSD, BTCUSD, EURUSD kabi Symbol'larni boshqaruvchi Canonical Symbol moduli.
Symbols Signal yaratmaydi.
Symbols BOS/CHoCH hisoblamaydi.
Symbols AI ishlatmaydi.
Symbols Risk hisoblamaydi.
---
# Objective
Symbols quyidagi vazifalarni bajaradi.
• Symbol Management
• Watchlist Management
• Favorites Management
• Symbol Search
• Symbol Info
---
# Layer Position
```text
Chart_API
↓
Symbols
↓
Chart_Data
```
---
# Responsibilities
Symbols
✓ Symbol ro'yxatini boshqaradi
✓ Watchlist va Favorites'ni saqlaydi
✓ Symbol qidiruvini bajaradi
---
# Not Responsible
Symbols
✗ Rendering
✗ Signal Generation
✗ Data Calculation
✗ AI Analysis
---
# Input
Symbols qabul qiladi.
• Symbol Request
• Symbol Metadata
---
# Output
Symbols yaratadi.
• Symbol Context
• Watchlist
• Symbol Info
---
# Workflow
```text
Chart_API
↓
Symbols
↓
Chart_Data
```
---
# Internal Modules (Planned — Foundation Freeze'dan keyin implementatsiya qilinadi)
```text
Symbols
├── SymbolManager/
├── Watchlist/
├── Favorites/
├── Search/
└── SymbolInfo/
```
---
# Golden Rules
1. Symbols faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Modules
```text
Symbols/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
Predecessor: Chart_API · Successor: Chart_Data
---
# Summary
Symbols GoldBot Chart Layer ichidagi Symbols vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, yuqoridagi Internal Modules ro'yxati Foundation Freeze'dan keyin haqiqiy implementatsiya bilan to'ldiriladi.
