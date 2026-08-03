# Chart Renderer Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_Renderer modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Chart_Renderer quyidagilar uchun javobgar.
✓ Canvas Rendering
✓ WebGL Rendering
✓ Layer Rendering
✓ Viewport Rendering
✓ Render Pipeline Management
Chart_Renderer bajarmaydi.
✗ Data Calculation
✗ Indicator Calculation
✗ Signal Generation
✗ BOS/CHoCH Calculation
✗ AI Analysis
✗ Risk Calculation
---
# Module Boundary
```text
Shared Render State
↓
Chart_Renderer
↓
Screenshot / Alerts / Chart_API
```
Chart_Renderer ketma-ket modul Output'larini emas, joriy Shared Render State'ni har frame o'qiydi (Render Loop Rule).
---
# Input Contract
• Shared Render State (Chart_Data, Objects, Drawing_Tools, Indicators, Analysis_Overlay yozgan)
• Theme
• Viewport Context
---
# Output Contract
• Rendered Frame
• Render Report
• Render Metadata
---
# Allowed Dependencies
✓ Chart_Data
✓ Chart_Interaction
✓ Objects
✓ Drawing_Tools
✓ Indicators
✓ Analysis_Overlay
✓ Theme
✓ Crosshair
---
# Forbidden Dependencies
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
✗ Platform Layer
---
# Public API (Blueprint — imzolar implementatsiya bosqichida aniqlanadi)
```text
getChart_RendererState()
subscribeChart_RendererEvent(callback)
configureChart_Renderer(options)
disposeChart_Renderer()
```
---
# Architecture Rules
Chart_Renderer:
✓ Canvas Rendering bajaradi.
✓ Module Boundary'ni saqlaydi.
Chart_Renderer:
✗ Signal yoki Decision yaratmaydi.
✗ BOS/CHoCH/FVG/Liquidity hisoblamaydi.
✗ AI ishlatmaydi.
---
# Runtime Rules
1. Chart_Renderer faqat o'z Module Boundary ichida ishlaydi.
2. Chart_Renderer har frame joriy Shared Render State'ni o'qiydi — ketma-ket modul Output'larini iste'mol qilmaydi (Render Loop Rule).
3. Output standart formatda yaratilishi shart.
4. Chart_Renderer Signal yoki Decision yaratmaydi.
5. Chart_Renderer BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Canvas Rendering bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Chart_Renderer Contract GoldBot Chart Layer ichidagi Chart Renderer jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
