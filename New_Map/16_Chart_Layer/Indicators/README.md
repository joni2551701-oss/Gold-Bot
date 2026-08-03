# Indicators
Status: BLUEPRINT
---
# Purpose
Indicators GoldBot Chart Layer ichidagi Canonical Indicators moduli hisoblanadi.
EMA, SMA, RSI, MACD, ATR, Volume, VWAP kabi Chart darajasidagi vizual indikatorlarni boshqaruvchi Canonical modul.
Indicators Signal yaratmaydi.
Indicators BOS/CHoCH hisoblamaydi.
Indicators AI ishlatmaydi.
Indicators Risk hisoblamaydi.
---
# Objective
Indicators quyidagi vazifalarni bajaradi.
• Trend Indicator Rendering Support
• Momentum Indicator Rendering Support
• Volume Indicator Rendering Support
• Volatility Indicator Rendering Support
• Custom Indicator Support
---
# Layer Position
```text
Drawing_Tools
↓
Indicators
↓
Analysis_Overlay
```
---
# Responsibilities
Indicators
✓ Chart uchun tanlangan indikatorlarni boshqaradi
✓ Indikator Overlay ma'lumotlarini tayyorlaydi
✓ Custom Indicator qo'shishni qo'llab-quvvatlaydi
---
# Not Responsible
Indicators
✗ Trading Indicator Calculation (GoldBot Indicator Layer vazifasi)
✗ Signal Generation
✗ BOS/CHoCH Calculation
✗ AI Analysis
✗ Rendering
---
# Input
Indicators qabul qiladi.
• Drawing Context
• Candle Data
• Indicator Selection
• Indicator Settings
---
# Output
Indicators yaratadi.
• Indicator Overlay Data
• Indicator State
• Indicator Metadata
---
# Golden Rules
1. Indicators faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Indicators/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Indicators GoldBot Chart Layer ichidagi Indicators vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, implementatsiya uchun ichki papkalar (submodules) keyingi bosqichda qo'shiladi.
