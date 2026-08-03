# Paper Trading
Status: CANONICAL
---
# Purpose
PaperTrading GoldBot Trade Monitoring Layer ichidagi Canonical Paper Trading moduli hisoblanadi.
Uning asosiy vazifasi tasdiqlangan Decision'ni real order yubormasdan simulyatsiya qilish va virtual pozitsiyaning hayot aylanishini kuzatishdir.
PaperTrading hech qachon Broker'ga murojaat qilmaydi.
PaperTrading hech qachon real order joylashtirmaydi.
PaperTrading hech qachon Risk sizing'ni o'zgartirmaydi.
---
# Objective
PaperTrading quyidagi vazifalarni bajaradi.
• Virtual Position Management
• Virtual Balance Management
• Paper Order Simulation
• Paper Trade Lifecycle
• Trade Replay
• Simulation Result Generation
---
# Layer Position
```text
MonitoringService
↓
PaperTrading
↓
MonitoringService
```
---
# Responsibilities
PaperTrading
✓ Tasdiqlangan Decision asosida virtual pozitsiya ochadi
✓ Virtual Balance'ni yuritadi
✓ Paper Order'larni simulyatsiya qiladi
✓ Paper Trade Lifecycle'ni (CREATED → OPEN → CLOSED/CANCELLED) boshqaradi
✓ Trade Replay imkonini beradi
✓ Simulyatsiya natijasini qaytaradi
---
# Not Responsible
PaperTrading
✗ Real Trade Execution (10_Execution_Layer vazifasi)
✗ Broker Communication
✗ Risk Calculation (09_Risk_Layer vazifasi)
✗ Signal Generation
✗ Trading Decision
✗ AI Analysis
---
# Input
PaperTrading qabul qiladi.
• Approved Decision
• Risk Policy
• Live Price Data
• Paper Trading Configuration
---
# Output
PaperTrading yaratadi.
• Virtual Position
• Virtual Balance
• Paper Trade State
• Simulation Result
---
# Workflow
```text
MonitoringService
↓
PaperTrading
↓
MonitoringService
```
---
# Internal Modules (Planned — implementatsiya bosqichida to'ldiriladi)
```text
PaperTrading
├── PaperTrade
├── PaperTradeMonitor
├── VirtualPosition
├── VirtualBalance
└── TradeState
```
---
# Golden Rules
1. PaperTrading hech qachon real order joylashtirmaydi va Broker'ga murojaat qilmaydi.
2. PaperTrading faqat Risk Policy ruxsat bergan doirada ishlaydi va Risk'ni qayta hisoblamaydi.
3. Virtual Balance real hisobga hech qachon ta'sir qilmaydi.
4. Paper Trade Lifecycle: CREATED → OPEN → CLOSED (yoki CANCELLED).
5. Simulyatsiya natijasi real Trade natijasi bilan aralashtirilmaydi.
6. PaperTrading Layer tashqarisiga chiqmaydi — natija MonitoringService orqali uzatiladi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
PaperTrading/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
PaperTrading GoldBot Trade Monitoring Layer ichidagi Canonical Paper Trading moduli hisoblanadi. U real execution emas — pozitsiya hayot aylanishini simulyatsiya qiladi va Broker'ga hech qachon murojaat qilmaydi.
