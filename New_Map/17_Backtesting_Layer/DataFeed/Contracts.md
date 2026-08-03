# Data Feed Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat DataFeed modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
DataFeed quyidagilar uchun javobgar.
✓ Candle manbasini yagona Contract ortiga yashiradi
✓ Replay va Live manbalar uchun bir xil interfeys taqdim etadi
✓ So'ralgan miqdordagi candle'ni qaytaradi
DataFeed bajarmaydi.
✗ Candle Storage
✗ Market Analysis
✗ Signal Generation
✗ Indicator Calculation
✗ Data Validation (01_Data_Layer vazifasi)
---
# Module Boundary
```text
BacktestEngine
↓
DataFeed
↓
ReplayEngine
```
---
# Input Contract
• Candle Request
• Feed Configuration
---
# Output Contract
• Candle List
• Feed Status
• Feed Metadata
---
# Allowed Dependencies
✓ BacktestEngine
✓ ReplayEngine
---
# Forbidden Dependencies
✗ Execution Layer (real order — Backtesting Isolation Rule)
✗ Broker Gateway
✗ Platform Layer (to'g'ridan-to'g'ri)
✗ Live Data (real vaqt oqimi)
✗ Signal Layer
✗ Strategy Layer
✗ AI Layer
---
# Runtime Contract
1. Candle iste'molchisi Live yoki Replay rejimini aniqlay olmasligi shart.
2. Hech qanday joyda 'if backtest ... else ...' shoxlanishi bo'lmaydi.
3. DataFeed candle mazmunini o'zgartirmaydi.
4. DataFeed tahlil bajarmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Candle Request qabul qilinadi.
✓ Yagona Contract orqali candle qaytariladi.
✓ Iste'molchi rejimni ajrata olmaydi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
DataFeed Contract DataFeed candle manbasi bilan qolgan barcha mantiq o'rtasidagi yagona Canonical seam hisoblanadi.
