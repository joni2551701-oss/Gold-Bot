# Strategy Engine
Status: CANONICAL
---
# Purpose
StrategyEngine Strategy Layer ichidagi barcha Strategy Execution jarayonini boshqaruvchi Canonical Engine hisoblanadi.
Uning asosiy vazifasi StrategyManager tomonidan faollashtirilgan strategiyani ishga tushirish, bajarilishini muvofiqlashtirish va Strategy Result yaratishdir.
StrategyEngine strategiya tanlamaydi va Profile yuklamaydi — bu StrategyManager vazifasi.
StrategyEngine signal yaratmaydi.
StrategyEngine trade ochmaydi.
StrategyEngine AI ishlatmaydi.
StrategyEngine faqat Strategy Execution, Coordination, Pipeline va Result Aggregation bilan shug'ullanadi.
---
# Objective
StrategyEngine quyidagi vazifalarni bajaradi.
• Strategy Execution
• Strategy Coordination
• Strategy Pipeline Management
• Strategy Result Collection
• Strategy Validation
• Strategy Result Aggregation
---
# Layer Position
```text
StrategyManager
↓
StrategyEngine
↓
StrategyService
```
---
# Responsibilities
StrategyEngine:
✓ Faollashtirilgan Strategiyani ishga tushiradi
✓ Strategy bajarilishini muvofiqlashtiradi (Coordination)
✓ Strategy Pipeline'ni boshqaradi
✓ Strategy natijalarini yig'adi (Result Collection)
✓ Strategy Result'ni tekshiradi (Validation)
✓ Strategy Result'ni birlashtiradi (Aggregation)
---
# Not Responsible
StrategyEngine:
✗ Strategy Discovery
✗ Strategy Selection
✗ Strategy Profile Loading
✗ Context Analysis
✗ Indicator Calculation
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
StrategyEngine qabul qiladi.
• Faollashtirilgan Strategiya (StrategyManager'dan)
• Market Context
• Indicator Context
---
# Output
StrategyEngine yaratadi.
• Strategy Result
• Strategy Score
• Strategy Confidence
• Strategy Metadata
---
# Workflow
```text
Receive Activated Strategy (StrategyManager)
↓
Receive Context
↓
Execute Strategy
↓
Coordinate Pipeline
↓
Collect Result
↓
Validate Result
↓
Aggregate Strategy Result
↓
StrategyService
```
---
# Golden Rules
1. StrategyEngine faqat Strategy Layer ichida ishlaydi.
2. Strategy tanlash va Profile yuklash StrategyManager vazifasi — StrategyEngine bu ishlarni bajarmaydi.
3. StrategyEngine faqat StrategyManager tomonidan faollashtirilgan strategiyani ishga tushiradi.
4. Strategy Result immutable hisoblanadi.
5. Signal yaratish taqiqlanadi.
6. AI ishlatilmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
StrategyEngine/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
StrategyEngine GoldBot Strategy Layer ichidagi Strategy Execution, Coordination va Result Aggregation'ni boshqaruvchi Canonical Engine hisoblanadi. Strategy tanlash va Profile yuklash StrategyManager vakolatida qoladi.
