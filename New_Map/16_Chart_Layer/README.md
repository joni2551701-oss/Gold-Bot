# Chart Layer
Status: BLUEPRINT
---
# Purpose
Chart Layer GoldBot ekotizimidagi Canonical Chart/Visualization Layer hisoblanadi.
TradingView, Bookmap va boshqa professional terminal arxitekturalaridan ilhomlangan, lekin GoldBot'ning 15 Layer falsafasiga (Data → Context → Strategy → Signal → AI → Decision → Risk → Telegram → Database) to'liq mos qurilgan.
Uning asosiy vazifasi GoldBot Core tomonidan hisoblangan Market Context, Indicator Context, Signal, Decision va Trade natijalarini foydalanuvchiga professional grafik ko'rinishda taqdim etishdir.
Chart Layer hech qachon Signal yaratmaydi.
Chart Layer hech qachon BOS/CHoCH/FVG/Liquidity/Wyckoff/AMD hisoblamaydi.
Chart Layer hech qachon AI ishlatmaydi.
Chart Layer hech qachon Risk hisoblamaydi.
Chart Layer faqat GoldBot Core'dan kelgan natijalarni vizual ko'rinishda aks ettiradi.
---
# Objective
Chart Layer quyidagi vazifalarni bajaradi.
• Chart Engine, Lifecycle, State, Camera, Coordinate System boshqaruvi
• Public API, Event API, Plugin API taqdim etish
• Candle, Tick, OHLCV, Session, Symbol ma'lumotlarini keshlash
• Canvas/WebGL orqali Rendering
• Mouse, Keyboard, Touch, Zoom, Pan, Drag, Selection boshqaruvi
• Drawing Tools (Trend Line, Fibonacci, Rectangle va h.k.)
• Chart darajasidagi vizual Indikatorlar
• GoldBot Core natijalarining Analysis Overlay orqali vizualizatsiyasi
• Historical Replay va Simulation
• Templates, Layout, Theme, Settings boshqaruvi
• Alerts va Screenshot Export
• Plugin System orqali kengaytirilishi
---
# Internal Structure
```text
Chart/
├── 01_Chart_Core/
├── 02_Chart_API/
├── 03_Chart_Data/
├── 04_Chart_Renderer/
├── 05_Chart_Interaction/
├── 06_Drawing_Tools/
├── 07_Indicators/
├── 08_Analysis_Overlay/
├── 09_Replay/
├── 10_Templates/
├── 11_Alerts/
├── 12_Screenshot/
├── 13_Layout/
├── 14_Crosshair/
├── 15_Timeframe/
├── 16_Symbols/
├── 17_Theme/
├── 18_Settings/
├── 19_Objects/
└── 20_Plugins/
```
---
# Module Overview
## Chart_Core
Chart Engine, Lifecycle, State, Camera, Coordinate System va Viewport'ni boshqaruvchi Canonical Orchestrator.
---
## Chart_API
Chart Layer uchun yagona Public API, Event API va Plugin API Boundary Gateway.
---
## Chart_Data
Candle, Tick, OHLCV, Session va Symbol ma'lumotlarini boshqaruvchi Cache moduli.
---
## Chart_Renderer
Canvas/WebGL orqali chizuvchi Rendering moduli. Hisob-kitob bajarmaydi.
---
## Chart_Interaction
Mouse, Keyboard, Touch, Zoom, Pan, Drag, Selection boshqaruvi.
---
## Drawing_Tools
Trend Line, Ray, Rectangle, Fibonacci, Text, Brush kabi chizish vositalari.
---
## Indicators
EMA, SMA, RSI, MACD, ATR, Volume, VWAP kabi Chart darajasidagi vizual indikatorlar.
---
## Analysis_Overlay
GoldBot Core hisoblagan BOS, CHoCH, OB, FVG, Liquidity, Wyckoff, AMD'ni vizualizatsiya qiladi. Hisoblamaydi — faqat chizadi.
---
## Replay
Historical Replay, Simulation va Playback.
---
## Templates
Layout, Workspace va Preset'lar.
---
## Alerts
Price, Indicator, Drawing, Time Alert'lar.
---
## Screenshot
PNG, JPG, PDF Export.
---
## Layout
Multi-chart (1/2/4/6/8/16) joylashuv.
---
## Crosshair
Cursor, OHLC Tooltip, Magnet.
---
## Timeframe
M1, M5, M15, H1, H4, D1, W1 va h.k.
---
## Symbols
XAUUSD, BTCUSD, EURUSD kabi Symbol boshqaruvi.
---
## Theme
Dark, Light, Custom Theme.
---
## Settings
Grid, Scale, Price Axis, Time Axis, Behavior.
---
## Objects
Candle, Line, Label, Shape, Overlay obyektlari — Renderer shu obyektlarni chizadi.
---
## Plugins
Tashqi Indicator va Drawing kengaytmalari uchun Plugin System.
---
# Responsibilities
Chart Layer
✓ Chart Rendering
✓ Chart Data Management
✓ User Interaction
✓ Drawing Tools
✓ Chart-level Indicators
✓ GoldBot Core natijalarining vizualizatsiyasi (Analysis Overlay orqali)
✓ Replay/Simulation
✓ Templates/Layout/Theme/Settings
✓ Alerts va Export
✓ Plugin Ecosystem
---
# Not Responsible
Chart Layer
✗ Signal Generation
✗ BOS/CHoCH/Order Block/FVG/Liquidity/Wyckoff/AMD Calculation
✗ AI Analysis
✗ Trading Decision
✗ Risk Calculation
✗ Trade Execution
✗ Historical Data Fetching (Data Layer vazifasi)
---
# Chart Runtime
```text
Chart_Data
↓
Chart_Core
↓
Chart_Renderer
↓
Chart_Interaction
↓
Objects
↓
Drawing_Tools
↓
Indicators
↓
Analysis_Overlay
↓
Alerts
↓
Screenshot
```
---
# GoldBot Bilan Bog'lanish
```text
GoldBot Core
        │
        │  Market Context
        │  Indicator Context
        │  Signal
        │  Decision
        │  Trade
        ▼
Chart_API
        │
        ▼
Analysis_Overlay
        │
        ▼
Chart_Renderer
```
Chart hech qachon:
* Signal yaratmaydi.
* BOS hisoblamaydi.
* AI ishlatmaydi.
* Risk hisoblamaydi.

U faqat GoldBot Core'dan kelgan natijalarni vizual ko'rinishda aks ettiradi.
---
# Golden Rules
1. Chart faqat GoldBot Core'dan kelgan natijalarni vizualizatsiya qiladi.
2. Chart hech qachon Signal/BOS/CHoCH/FVG/Liquidity hisoblamaydi.
3. Chart hech qachon AI yoki Risk logikasi bilan shug'ullanmaydi.
4. Chart_API Chart Layer'ning yagona tashqi kirish/chiqish nuqtasi hisoblanadi.
5. Chart_Renderer faqat chizadi — hisoblamaydi.
6. Analysis_Overlay faqat vizualizatsiya qiladi — tahlil qilmaydi.
7. Har bir modul mustaqil rivojlantirilishi mumkin (Plugin orqali kengaytiriladi).
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Repository Structure
```text
Chart/
├── README.md
├── Layer_ModuleMap.md
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_Contracts.md
│
├── 01_Chart_Core/ ... 20_Plugins/
│   ├── README.md
│   ├── Contracts.md
│   ├── ModuleMap.md
│   └── SequenceDiagram.md
```
Har bir modul hozircha Blueprint bosqichida — faqat 4 ta standart hujjat mavjud. Ichki submodullar (masalan TrendLine/, CanvasRenderer/, ReplayEngine/) Foundation Freeze'dan keyin, implementatsiya bosqichida real kod bilan to'ldiriladi.
---
# Blueprint Status Note
Bu Layer hozircha **Blueprint** bosqichida. 20 ta modulning har biri o'zining README.md/Contracts.md/ModuleMap.md/SequenceDiagram.md hujjatlariga ega, ammo ichki submodul papkalari (TrendLine/, CanvasRenderer/, ReplayEngine/ va h.k.) hali yaratilmagan. Bular implementatsiya bosqichida, real kod bilan birga qo'shiladi.
---
# Summary
Chart Layer GoldBot ekotizimidagi Canonical Visualization Layer bo'lib, GoldBot Core'ning Market Context, Indicator Context, Signal, Decision va Trade natijalarini professional, TradingView darajasidagi grafik interfeys orqali foydalanuvchiga yetkazadi. Chart hech qachon tahlil, qaror yoki risk hisoblamaydi — faqat vizual taqdimot bilan shug'ullanadi.
