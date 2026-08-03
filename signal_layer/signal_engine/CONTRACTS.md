# Signal Engine Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalEngine modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
SignalEngine quyidagilar uchun javobgar.
✓ Pipeline Orchestration
✓ Module Coordination
✓ Execution Order
✓ Runtime Control
✓ Signal Lifecycle Management
SignalEngine bajarmaydi.
✗ Technical Confluence (ConfluenceEngine vazifasi)
✗ Signal Build (SignalBuilder vazifasi)
✗ Signal Validation (SignalValidator vazifasi)
✗ Signal Scoring (SignalScoring vazifasi)
✗ Signal Formatting (SignalFormatter vazifasi)
✗ Market Analysis
✗ Context Analysis
✗ Indicator Calculation
✗ Strategy Analysis
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
Strategy Layer
↓
SignalEngine
↓
ConfluenceEngine → SignalBuilder → SignalValidator → SignalScoring → SignalFormatter
↓
SignalService
```
---
# Input Contract
• Strategy Result
• Strategy Metadata
---
# Output Contract
• Pipeline Execution Order
• Runtime Status
• Coordination Events
---
# Allowed Dependencies
✓ ConfluenceEngine
✓ SignalBuilder
✓ SignalValidator
✓ SignalScoring
✓ SignalFormatter
✓ Event System
---
# Forbidden Dependencies
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Runtime Contract
1. Strategy Result mavjud bo'lishi shart.
2. SignalEngine faqat pipeline bosqichlarini to'g'ri ketma-ketlikda ishga tushiradi.
3. SignalEngine hech qanday bosqichning ichki hisob-kitobini o'zi bajarmaydi.
4. Har bir bosqich natijasi keyingi bosqichga o'zgartirilmasdan uzatiladi.
5. AI ishlatilmaydi.
6. Decision qabul qilinmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Pipeline to'g'ri ketma-ketlikda ishga tushadi.
✓ Har bir bosqich muvaffaqiyatli chaqiriladi.
✓ Runtime Status kuzatiladi.
✓ Yakuniy natija SignalService'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
SignalEngine Contract GoldBot Signal Layer ichidagi Pipeline Orchestration, Module Coordination va Runtime Control'ni boshqaruvchi rasmiy Canonical Architecture Contract hisoblanadi. Confluence, Build, Validation, Scoring va Formatting har biri o'z modulida bajariladi.
