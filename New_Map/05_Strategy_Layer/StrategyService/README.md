# Strategy Service
Status: CANONICAL
---
# Purpose
StrategyService GoldBot Strategy Layer uchun rasmiy Service Boundary hisoblanadi.
Uning asosiy vazifasi Strategy Layer'ni boshqa Layer'lar bilan bog'lash va Strategy natijalarini tashqi modullarga taqdim etishdir.
StrategyService strategiya hisoblamaydi.
StrategyService signal yaratmaydi.
StrategyService AI ishlatmaydi.
StrategyService faqat Strategy Layer API sifatida ishlaydi.
---
# Objective
StrategyService quyidagi vazifalarni bajaradi.
• Strategy Request Processing
• Strategy Execution Request
• Strategy Result Delivery
• Strategy Status Management
• Strategy Event Publishing
• Layer Communication
---
# Layer Position
```text
Signal Layer
↓
StrategyService
↓
StrategyEngine
↓
StrategyManager
↓
Strategy Library
```
---
# Responsibilities
StrategyService
✓ Strategy Request qabul qiladi
✓ StrategyEngine'ga uzatadi
✓ Strategy Result qaytaradi
✓ Strategy Status boshqaradi
✓ Strategy Event yuboradi
✓ Layer Communication bajaradi
---
# Not Responsible
StrategyService
✗ Strategy Analysis
✗ Indicator Calculation
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
• Strategy Request
• Strategy Configuration
• Context
• Indicator Context
---
# Output
• Strategy Result
• Strategy Status
• Strategy Metadata
---
# Workflow
```text
Receive Request
↓
Validate Request
↓
StrategyEngine
↓
Receive Strategy Result
↓
Publish Result
↓
Signal Layer
```
---
# Golden Rules
1. StrategyService faqat Service Boundary hisoblanadi.
2. Strategy Logic bajarmaydi.
3. Strategy natijasini o'zgartirmaydi.
4. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
StrategyService/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
StrategyService GoldBot Strategy Layer uchun yagona Canonical Service Boundary hisoblanadi.
