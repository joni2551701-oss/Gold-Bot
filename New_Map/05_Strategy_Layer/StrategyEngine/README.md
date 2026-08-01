# Strategy Engine
Status: CANONICAL
---
# Purpose
StrategyEngine Strategy Layer ichidagi barcha Strategy modullarini boshqaruvchi Canonical Engine hisoblanadi.
Uning asosiy vazifasi Strategy Library ichidagi strategiyalarni ishga tushirish, Strategy Profile'larni qo'llash va Strategy Result yaratishdir.
StrategyEngine signal yaratmaydi.
StrategyEngine trade ochmaydi.
StrategyEngine AI ishlatmaydi.
StrategyEngine faqat Strategy Execution boshqaruvini amalga oshiradi.
---
# Objective
StrategyEngine quyidagi vazifalarni bajaradi.
• Strategy Discovery
• Strategy Selection
• Strategy Execution
• Strategy Profile Loading
• Strategy Validation
• Strategy Orchestration
• Strategy Result Generation
---
# Layer Position
```text
Context Layer
↓
Indicator Layer
↓
StrategyEngine
↓
Strategy Service
```
---
# Responsibilities
StrategyEngine:
✓ Strategy tanlaydi
✓ Strategy ishga tushiradi
✓ Strategy Profile yuklaydi
✓ Strategy bajarilishini boshqaradi
✓ Strategy Result yaratadi
✓ Strategy Lifecycle boshqaradi
---
# Not Responsible
StrategyEngine:
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
• Market Context
• Indicator Context
• Strategy Configuration
• Strategy Profile
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
Receive Context
↓
Load Strategy
↓
Load Strategy Profile
↓
Execute Strategy
↓
Validate Result
↓
Generate Strategy Result
↓
StrategyService
```
---
# Golden Rules
1. StrategyEngine faqat Strategy Layer ichida ishlaydi.
2. Strategy tanlash deterministik bo'lishi kerak.
3. Strategy Result immutable hisoblanadi.
4. Signal yaratish taqiqlanadi.
5. AI ishlatilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
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
StrategyEngine GoldBot Strategy Layer ichidagi barcha strategiyalarni boshqaruvchi Canonical Engine hisoblanadi.
