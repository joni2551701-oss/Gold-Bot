# Strategy Manager
Status: CANONICAL
---
# Purpose
StrategyManager GoldBot Strategy Layer ichidagi barcha Strategy modullarini boshqaruvchi Canonical Manager hisoblanadi.
Uning asosiy vazifasi Strategy Library, Strategy Profiles va Strategy Engine o'rtasidagi boshqaruvni amalga oshirishdir.
StrategyManager strategiya hisoblamaydi.
StrategyManager signal yaratmaydi.
StrategyManager AI ishlatmaydi.
StrategyManager faqat Strategy Lifecycle va Configuration Management bilan shug'ullanadi.
---
# Objective
StrategyManager quyidagi vazifalarni bajaradi.
• Strategy Registration
• Strategy Discovery
• Strategy Selection
• Strategy Configuration Management
• Strategy Profile Management
• Strategy Version Management
• Strategy Lifecycle Management
• Strategy Validation
---
# Layer Position
```text
Strategy Library
↓
Strategy Profiles
↓
Strategy Manager
↓
Strategy Engine
```
---
# Responsibilities
StrategyManager
✓ Strategy ro'yxatdan o'tkazadi
✓ Strategy tanlaydi
✓ Strategy Profile yuklaydi
✓ Strategy Configuration boshqaradi
✓ Strategy Lifecycle boshqaradi
✓ Strategy Version boshqaradi
✓ Strategy Validation bajaradi
---
# Not Responsible
StrategyManager
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
• Strategy Profile
---
# Output
• Active Strategy
• Active Configuration
• Active Strategy Profile
---
# Workflow
```text
Receive Request
↓
Select Strategy
↓
Load Profile
↓
Validate Configuration
↓
Activate Strategy
↓
StrategyEngine
```
---
# Golden Rules
1. StrategyManager strategiyani hisoblamaydi.
2. StrategyManager faqat boshqaradi.
3. Strategy Configuration immutable hisoblanadi.
4. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
StrategyManager/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
StrategyManager GoldBot Strategy Layer ichidagi barcha Strategy va Strategy Profile boshqaruvini amalga oshiruvchi Canonical Manager hisoblanadi.
