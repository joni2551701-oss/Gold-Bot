# Chart Rendering Guide
Status: BLUEPRINT — Canonical Rendering Source
---
# Purpose
Ushbu hujjat Chart Layer'ning barcha vizual modullari (Chart_Renderer, Objects, Drawing_Tools, Indicators, Analysis_Overlay, Crosshair, Theme) bir-birini to'g'ri va bashorat qilinadigan tartibda chizishi uchun rasmiy Canonical Rendering qoidalarini belgilaydi.
Bu implementatsiya emas — bu Rendering Architecture uchun Blueprint hisoblanadi.
Director Ruling (Chart Runtime Model, Option 1) bo'yicha ushbu hujjat Chart Layer'ning **Canonical Rendering Source** hisoblanadi — Render Loop, Frame Lifecycle, Shared Render State va Invalidation qoidalari birinchi navbatda shu yerda belgilanadi; boshqa hujjatlar (`Layer_DataFlow.md`, `Layer_SequenceDiagram.md`, modul Contracts.md'lari) shu qoidalarga mos bo'lishi shart.
---
# Render Loop
Chart_Renderer pipeline emas — **render loop** modelida ishlaydi:
```text
loop (har frame):
    Read Shared Render State
    ↓
    Determine Dirty Regions
    ↓
    Draw (Z-Index tartibida)
    ↓
    Present Frame
```
Chart_Renderer hech qachon "oldingi modul Output yubordimi" deb kutmaydi — u har doim joriy Shared Render State'ni o'qiydi va chizadi.
---
# Shared Render State
Shared Render State — Chart_Core tomonidan boshqariladigan, barcha vizual modullar (Chart_Data, Chart_Interaction, Objects, Drawing_Tools, Indicators, Analysis_Overlay) yozadigan va Chart_Renderer o'qiydigan markaziy holat.
```text
Shared Render State
├── Candle/Tick Data        (Chart_Data yozadi)
├── Interaction Context     (Chart_Interaction yozadi)
├── Object List             (Objects yozadi)
├── Drawing Objects         (Drawing_Tools yozadi)
├── Indicator Overlays      (Indicators yozadi)
└── Analysis Overlays       (Analysis_Overlay yozadi)
```
Modullar bir-birining Output'ini to'g'ridan-to'g'ri iste'mol qilmaydi — faqat Shared Render State orqali muloqot qiladi (Chart Shared State Rule).
---
# Frame Lifecycle
```text
Frame Start
↓
Input Collection (Chart_Interaction)
↓
State Update (Objects, Drawing_Tools, Indicators, Analysis_Overlay → Shared Render State)
↓
Invalidation Check (Dirty Region)
↓
Render (Chart_Renderer)
↓
Present
↓
Frame End
```
---
# Invalidation
* Har qanday modul Shared Render State'ning biror qismini o'zgartirsa, tegishli hudud "Dirty" deb belgilanadi.
* Chart_Renderer faqat Dirty deb belgilangan hududlarni qayta chizadi (qarang: Dirty Region Tracking, Performance Rules).
* Full Invalidation faqat Resize, Theme almashtirish yoki Layout o'zgarishida yuz beradi.
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
7. Bu hujjat Render Loop, Frame Lifecycle, Shared Render State va Invalidation uchun Canonical Source hisoblanadi — boshqa hujjatlar shu qoidalarga zid bo'lmasligi kerak.
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
