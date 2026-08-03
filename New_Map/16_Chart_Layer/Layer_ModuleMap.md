# Chart Layer Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart Layer ichidagi barcha modullarning Canonical xaritasini tavsiflaydi.
---
# Layer Architecture
```text
Chart Layer
        │
        ├── Chart_Core
        ├── Chart_API
        ├── Chart_Data
        ├── Chart_Renderer
        ├── Chart_Interaction
        ├── Drawing_Tools
        ├── Indicators
        ├── Analysis_Overlay
        ├── Replay
        ├── Templates
        ├── Alerts
        ├── Screenshot
        ├── Layout
        ├── Crosshair
        ├── Timeframe
        ├── Symbols
        ├── Theme
        ├── Settings
        ├── Objects
        └── Plugins
```
---
# Module Numbering vs Runtime Order
Repository'dagi modul raqamlanishi (01-20) implementatsiya/hujjat tartibini bildiradi, Runtime Execution tartibini emas. Haqiqiy ishga tushirish tartibi uchun `Layer_SequenceDiagram.md`ga qarang.
---
# Module Responsibilities
| Module | Responsibility |
|---|---|
| Chart_Core | Chart Engine, Lifecycle, State, Camera, Coordinate System, Viewport |
| Chart_API | Public API, Event API, Plugin API Boundary Gateway |
| Chart_Data | Candle, Tick, OHLCV, Session, Symbol Cache |
| Chart_Renderer | Canvas/WebGL Rendering |
| Chart_Interaction | Mouse, Keyboard, Touch, Zoom, Pan, Drag, Selection |
| Drawing_Tools | Trend Line, Ray, Rectangle, Fibonacci, Text, Brush |
| Indicators | Chart darajasidagi vizual indikatorlar (EMA, RSI, MACD va h.k.) |
| Analysis_Overlay | BOS/CHoCH/OB/FVG/Liquidity/Wyckoff/AMD vizualizatsiyasi |
| Replay | Historical Replay, Simulation, Playback |
| Templates | Layouts, Workspaces, Presets |
| Alerts | Price, Indicator, Drawing, Time Alerts |
| Screenshot | PNG, JPG, PDF Export |
| Layout | Multi-chart (1/2/4/6/8/16) |
| Crosshair | Cursor, OHLC Tooltip, Magnet |
| Timeframe | M1, M5, M15, H1, H4, D1, W1 |
| Symbols | XAUUSD, BTCUSD, EURUSD boshqaruvi |
| Theme | Dark, Light, Custom Theme |
| Settings | Grid, Scale, Price Axis, Time Axis, Behavior |
| Objects | Candle, Line, Label, Shape, Overlay obyektlari |
| Plugins | External indicator & drawing extensions |
---
# Dependency Structure
Har bir modulning Allowed/Forbidden Dependencies ro'yxati o'z `Contracts.md`/`ModuleMap.md` hujjatida belgilangan. Umumiy qoida:
* Barcha modullar GoldBot'ning Signal/AI/Decision/Risk/Execution/Database/Platform Layer'lariga to'g'ridan-to'g'ri bog'lana olmaydi (Forbidden).
* GoldBot Core natijalari faqat Chart_API orqali kiradi.
---
# Summary
Chart Layer 20 modulning Canonical xaritasi ushbu hujjatda belgilangan. Bu Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi.
