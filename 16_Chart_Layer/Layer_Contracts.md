# Chart Layer Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart Layer uchun rasmiy Architecture Contract hisoblanadi.
---
# Layer Responsibility
Chart Layer quyidagilar uchun javobgar.
✓ Chart Rendering
✓ Chart Data Caching
✓ User Interaction
✓ Drawing Tools
✓ Chart-level Indicators
✓ GoldBot Core natijalarining vizualizatsiyasi (Analysis Overlay)
✓ Replay/Simulation
✓ Templates/Layout/Theme/Settings
✓ Alerts va Export
✓ Plugin Ecosystem
---
# Layer Does NOT
✗ Signal Generation
✗ BOS/CHoCH/Order Block/FVG/Liquidity/Wyckoff/AMD Calculation
✗ AI Analysis
✗ Trading Decision
✗ Risk Calculation
✗ Trade Execution
✗ Historical Data Fetching
---
# Input Contract
Chart Layer qabul qiladi.
• Market Context (GoldBot Core'dan, Chart_API orqali)
• Indicator Context (GoldBot Core'dan, Chart_API orqali)
• Signal (GoldBot Core'dan, Chart_API orqali)
• Decision (GoldBot Core'dan, Chart_API orqali)
• Trade (GoldBot Core'dan, Chart_API orqali)
• Historical Candles (Data Layer'dan)
• User Interaction Event
---
# Output Contract
Chart Layer yaratadi.
• Rendered Chart Frame
• Drawing Objects
• Overlay Visualization
• Alert Trigger
• Exported File (PNG/JPG/PDF)
---
# Chart Execution Flow (Processing Order — NOT a token-passing Pipeline)
```text
GoldBot Core
↓
Chart_API (Entry)
↓
Chart_Core
↓
Chart_Data · Chart_Interaction · Objects        (parallel)
↓
Shared Render State
↓
Drawing_Tools · Indicators · Analysis_Overlay   (parallel)
↓
Chart_Renderer   (har frame Shared Render State'ni o'qiydi)
↓
Screenshot · Alerts                              (parallel)
↓
Chart_API (Exit)
↓
User
```
---
# Layer Rules
1. Chart Layer'ga barcha tashqi kirish va chiqishlar Chart_API orqali amalga oshiriladi (Entry va Exit).
2. Chart_Core barcha ichki modullarni boshqaradi.
3. Chart_Renderer faqat chizadi — hisoblamaydi, va ketma-ket modul Output'ini emas, joriy Shared Render State'ni o'qiydi (Render Loop Rule).
4. Analysis_Overlay faqat vizualizatsiya qiladi — tahlil qilmaydi.
5. Chart hech qachon Signal/BOS/CHoCH/FVG/Liquidity/Wyckoff/AMD hisoblamaydi.
6. Chart hech qachon AI yoki Risk logikasi bilan shug'ullanmaydi.
7. Chart hech qachon Trade Execution qilmaydi.
8. Chart modullari Chart State/Render State orqali muloqot qiladi — ownership yoki strict Input→Output zanjiri emas (Chart Shared State Rule).
9. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ GoldBot Core natijalari Chart_API orqali qabul qilinadi.
✓ Chart Data keshlanadi.
✓ Chart Render qilinadi.
✓ User Interaction ishlaydi.
✓ Drawing Tools ishlaydi.
✓ Analysis Overlay vizualizatsiya qiladi.
✓ Alert va Export ishlaydi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Chart Layer Contract GoldBot arxitekturasidagi Canonical Visualization Layer sifatida ishlashni, GoldBot Core natijalarini Chart_API orqali qabul qilishni, professional Chart Rendering, Drawing Tools va Analysis Overlay taqdim etishni, hamda hech qachon tahlil, qaror yoki risk hisoblamaslikni belgilovchi rasmiy Architecture Contract hisoblanadi. Bu hujjat Blueprint bosqichida — implementatsiya Foundation Freeze'dan keyin boshlanadi.
