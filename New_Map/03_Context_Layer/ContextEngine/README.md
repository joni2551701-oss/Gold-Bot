# Context Engine
Status: CANONICAL
---
# Purpose
ContextEngine Context Layer ichidagi markaziy Orchestrator hisoblanadi.
U barcha Context modullarini boshqaradi va yakuniy Market Context obyektini yaratadi.
ContextEngine Context hisoblamaydi.
Har bir modul o'z Context qismini yaratadi.
ContextEngine ularni birlashtiradi.
---
# Objective
ContextEngine quyidagi vazifalarni bajaradi:
• Context Orchestration
• Module Coordination
• Context Aggregation
• Runtime Coordination
• Context Lifecycle
• Context Validation
• Context State Management
---
# Layer Position
```text
Context Layer
↓
ContextEngine
↓
MarketStructure
Liquidity
OrderBlock
FairValueGap
Wyckoff
AMD
Session
Trend
VolumeProfile
↓
ContextService
```
---
# Responsibilities
ContextEngine:
✓ Context modullarini boshqaradi
✓ Context yaratadi
✓ Context Validation
✓ Context Lifecycle
✓ Runtime Coordination
✓ Module Coordination
---
# Not Responsible
ContextEngine:
✗ Indicator Calculation
✗ Strategy
✗ Signal
✗ AI
✗ Decision
✗ Risk
✗ Execution
---
# Input
ContextEngine qabul qiladi:
• Runtime Data
• Context Request
• Module Results
• Market Events
---
# Output
ContextEngine yaratadi:
• Market Context
• Context Events
• Context Status
• Runtime Context
---
# Managed Modules
• MarketStructure
• Liquidity
• OrderBlock
• FairValueGap
• Wyckoff
• AMD
• Session
• Trend
• VolumeProfile
• ContextService
---
# Workflow
```text
Runtime Data
↓
ContextEngine
↓
Run Context Modules
↓
Collect Results
↓
Build Market Context
↓
ContextService
```
---
# Golden Rules
1. ContextEngine Context Layer ichidagi yagona Orchestrator.
2. Har bir Context modul mustaqil ishlaydi.
3. ContextEngine barcha natijalarni birlashtiradi.
4. ContextEngine Indicator hisoblamaydi.
5. ContextEngine Signal yaratmaydi.
6. Circular Dependency taqiqlanadi.
---
# Related Documents
```text
ContextEngine/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
ContextEngine GoldBot Context Layer ichidagi barcha Context modullarini boshqaruvchi yagona Canonical Orchestrator hisoblanadi.
