# Chart Rendering Guide
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart Layer'ning barcha vizual modullari (Chart_Renderer, Objects, Drawing_Tools, Indicators, Analysis_Overlay, Crosshair, Theme) bir-birini to'g'ri va bashorat qilinadigan tartibda chizishi uchun rasmiy Canonical Rendering qoidalarini belgilaydi.
Bu implementatsiya emas — bu Rendering Architecture uchun Blueprint hisoblanadi.
---
# Render Order (Z-Index)
Chart_Renderer quyidagi qat'iy Z-Index tartibida chizadi — pastdan yuqoriga:
```text
0. Background / Grid           (Settings, Theme)
1. Candle / Price Data         (Chart_Data → Objects: CandleObject)
2. Volume Panel                (Indicators: Volume)
3. Indicators (Overlay-type)   (Indicators: MovingAverage, VWAP)
4. Drawing Tools                (Drawing_Tools: TrendLine, Rectangle, Fibonacci...)
5. Analysis Overlay              (Analysis_Overlay: BOS, CHoCH, OB, FVG, Liquidity, Wyckoff, AMD)
6. Alerts Markers                (Alerts)
7. Crosshair / Tooltip            (Crosshair)
8. UI Chrome (Toolbar, Legend)     (Chart_API / Templates)
```
Yuqori raqamli qatlam har doim pastki qatlamning ustidan chiziladi.
---
# Layer Rendering Priority
| Layer | Priority | Update Frequency |
|---|---|---|
| Background / Grid | Low | On resize / theme change only |
| Candle / Price Data | High | Every tick / new candle |
| Volume Panel | High | Every tick / new candle |
| Indicators (Overlay) | Medium | On candle close (yoki real-time, indikatorga bog'liq) |
| Drawing Tools | Medium | On user interaction only |
| Analysis Overlay | Medium | On GoldBot Core update (Chart_API orqali) |
| Alerts Markers | Low | On alert trigger only |
| Crosshair / Tooltip | Highest | Every mouse move (throttled) |
| UI Chrome | Low | On layout/theme change only |
---
# Object Priority
Bitta Z-Index qatlami ichida bir nechta Object mavjud bo'lsa, chizish tartibi:
1. Selected/Active Object'lar oxirida chiziladi (eng ustida ko'rinishi uchun).
2. Yangi yaratilgan Object eskisidan keyin chiziladi.
3. Locked Object'lar birinchi bo'lib chiziladi (o'zgartirib bo'lmaydigan fon sifatida).
---
# Overlay Priority
Analysis_Overlay ichida bir nechta tahlil turi bir vaqtda ko'rsatilishi mumkin (masalan BOS va Liquidity bir vaqtda). Ustuvorlik tartibi:
```text
MarketStructure (BOS/CHoCH)
↓
OrderBlock / FVG
↓
Liquidity
↓
Wyckoff / AMD
↓
PremiumDiscount / Sessions
```
Konflikt holatida (ikkita Overlay bir hududni egallasa) — keyingi ustuvorlikdagi Overlay avvalgisining ustidan yarim shaffof (opacity) tarzda chiziladi, hech biri o'chirilmaydi.
---
# Performance Rules
## Virtualization
Faqat Viewport ichida ko'rinadigan Candle/Object'lar chiziladi. Viewport tashqarisidagi elementlar Render Pipeline'ga kiritilmaydi.
## Batching
Bir xil turdagi Object'lar (masalan barcha Candle'lar, barcha TrendLine'lar) bitta Draw Call'da guruhlab chiziladi — har bir Object uchun alohida chaqiruv qilinmaydi.
## Dirty Region Tracking
Faqat o'zgargan hudud (Dirty Region) qayta chiziladi; butun Canvas har frame'da to'liq qayta chizilmaydi.
## Debounce / Throttle
Crosshair va Tooltip yangilanishi throttle qilinadi (masalan 16ms — 60 FPS chegarasida); Resize/Zoom hodisalari debounce qilinadi.
---
# FPS Target
| Rejim | Target FPS | Minimal FPS |
|---|---|---|
| Static Chart (harakatsiz) | 60 | 30 |
| Live Candle Update | 60 | 30 |
| Zoom / Pan (Interaction) | 60 | 45 |
| Replay (Playback) | 60 | 30 |
| Multi-Chart Layout (4-16 chart) | 30 | 15 (per chart) |
---
# Canvas / WebGL Switching
* **Canvas 2D** — standart rejim, kam sonli Candle/Object (< ~5,000 vizual element) uchun ishlatiladi.
* **WebGL** — katta hajmdagi tarixiy ma'lumot, Tick-level Rendering yoki bir nechta parallel Chart (Layout) uchun avtomatik yoqiladi.
* Switching mezoni: vizual element soni, Layout'dagi Chart soni va qurilma imkoniyati (GPU mavjudligi) asosida Chart_Renderer tomonidan avtomatik aniqlanadi.
* Foydalanuvchi qo'lda Canvas/WebGL rejimini Settings orqali majburlab tanlashi mumkin.
---
# Caching Strategy
* **Candle Cache** — Chart_Data tomonidan saqlanadi, Renderer har frame'da qayta so'ramaydi.
* **Indicator Cache** — Indicator natijalari yangi Candle kelmaguncha qayta hisoblanmaydi (Indicators moduli tomonidan boshqariladi, Rendering emas).
* **Overlay Cache** — Analysis_Overlay GoldBot Core'dan yangi natija kelmaguncha oldingi Overlay Object'larini qayta ishlatadi.
* **Render Cache (Offscreen Canvas)** — o'zgarmagan qatlamlar (masalan Background/Grid) Offscreen Canvas'da keshlanadi va faqat kerak bo'lganda qayta chiziladi.
---
# Golden Rules
1. Render Order (Z-Index) hech qachon buzilmaydi.
2. Faqat Viewport ichidagi elementlar chiziladi (Virtualization majburiy).
3. Crosshair har doim eng yuqori qatlamda chiziladi.
4. FPS Target'dan pastga tushganda avtomatik ravishda soddalashtirilgan Rendering rejimiga (masalan kamroq Object, past aniqlik) o'tiladi.
5. Rendering hech qachon hisob-kitob bajarmaydi — u faqat oldindan tayyorlangan Object/Overlay ma'lumotlarini chizadi.
6. Bu hujjat faqat Chart_Renderer, Objects, Drawing_Tools, Indicators, Analysis_Overlay va Crosshair modullariga tegishli qoidalarni belgilaydi — boshqa modullarning o'z Contracts.md hujjatlari o'zgarmaydi.
---
# Related Documents
```text
16_Chart_Layer/
├── README.md
├── Layer_ModuleMap.md
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_Contracts.md
└── Rendering_Guide.md   ← ushbu hujjat
```
---
# Summary
Rendering_Guide.md Chart Layer'ning vizual modullari (Chart_Renderer, Objects, Drawing_Tools, Indicators, Analysis_Overlay, Crosshair, Theme) o'rtasidagi chizish tartibi, ustuvorlik, performance va caching qoidalarini belgilaydigan qo'shimcha Canonical hujjat hisoblanadi. Bu hujjat Blueprint bosqichida — real Render Pipeline implementatsiyasi Foundation Freeze'dan keyin boshlanadi.
