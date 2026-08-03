# Paper Trading Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat PaperTrading modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
PaperTrading quyidagilar uchun javobgar.
✓ Tasdiqlangan Decision asosida virtual pozitsiya ochadi
✓ Virtual Balance'ni yuritadi
✓ Paper Order'larni simulyatsiya qiladi
✓ Paper Trade Lifecycle'ni (CREATED → OPEN → CLOSED/CANCELLED) boshqaradi
✓ Trade Replay imkonini beradi
✓ Simulyatsiya natijasini qaytaradi
PaperTrading bajarmaydi.
✗ Real Trade Execution (10_Execution_Layer vazifasi)
✗ Broker Communication
✗ Risk Calculation (09_Risk_Layer vazifasi)
✗ Signal Generation
✗ Trading Decision
✗ AI Analysis
---
# Module Boundary
```text
MonitoringService
↓
PaperTrading
↓
MonitoringService
```
---
# Input Contract
• Approved Decision
• Risk Policy
• Live Price Data
• Paper Trading Configuration
---
# Output Contract
• Virtual Position
• Virtual Balance
• Paper Trade State
• Simulation Result
---
# Allowed Dependencies
✓ MonitoringService
✓ PositionMonitor
✓ TradeLifecycleManager
---
# Forbidden Dependencies
✗ Execution Layer
✗ Broker Gateway
✗ Risk Layer (to'g'ridan-to'g'ri)
✗ Decision Layer
✗ Signal Layer
✗ AI Layer
✗ Database Layer
✗ Platform Layer
---
# Runtime Contract
1. PaperTrading hech qachon real order joylashtirmaydi va Broker'ga murojaat qilmaydi.
2. PaperTrading faqat Risk Policy ruxsat bergan doirada ishlaydi va Risk'ni qayta hisoblamaydi.
3. Virtual Balance real hisobga hech qachon ta'sir qilmaydi.
4. Paper Trade Lifecycle: CREATED → OPEN → CLOSED (yoki CANCELLED).
5. Simulyatsiya natijasi real Trade natijasi bilan aralashtirilmaydi.
6. PaperTrading Layer tashqarisiga chiqmaydi — natija MonitoringService orqali uzatiladi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Approved Decision qabul qilinadi.
✓ Virtual Position ochiladi.
✓ Paper Trade Lifecycle boshqariladi.
✓ Simulation Result yaratiladi.
✓ Hech qanday real order joylashtirilmaydi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
PaperTrading Contract PaperTrading GoldBot Trade Monitoring Layer ichidagi Canonical Paper Trading moduli hisoblanadi. U real execution emas — pozitsiya hayot aylanishini simulyatsiya qiladi va Broker'ga hech qachon murojaat qilmaydi.
