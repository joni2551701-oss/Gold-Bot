# Context Engine
Status: CANONICAL
---
# Purpose
ContextEngine barcha Context Analysis modullarining ishlash tartibini boshqaradi va ularning natijalarini ContextService'ga uzatadi. U yakuniy Market Context obyektini yaratmaydi.
ContextEngine Context hisoblamaydi.
Har bir modul o'z Context qismini yaratadi.
Yakuniy Market Context obyektini faqat ContextService yaratadi.
---
# Objective
ContextEngine quyidagi vazifalarni bajaradi:
• Context Orchestration
• Module Coordination
• Result Forwarding (ContextService'ga)
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
✓ Module Execution Order'ni belgilaydi
✓ Context Validation
✓ Context Lifecycle
✓ Runtime Coordination
✓ Module Coordination
✓ Natijalarni ContextService'ga uzatadi
---
# Not Responsible
ContextEngine:
✗ Yakuniy Market Context obyektini yaratish (ContextService vazifasi)
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
• Module Execution Order
• Context Events
• Context Status
• Runtime Context
• Module Results (ContextService uchun)
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
Forward Results
↓
ContextService (Builds Final Market Context)
```
---
# Golden Rules
1. ContextEngine Context Layer ichidagi yagona Orchestrator.
2. Har bir Context modul mustaqil ishlaydi.
3. ContextEngine faqat orchestration va coordination bilan shug'ullanadi; yakuniy Market Context obyektini yaratmaydi.
4. Yakuniy Market Context obyektini faqat ContextService yaratadi.
5. ContextEngine Indicator hisoblamaydi.
6. ContextEngine Signal yaratmaydi.
7. Circular Dependency taqiqlanadi.
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
ContextEngine GoldBot Context Layer ichidagi barcha Context modullarining ishlash tartibini boshqaruvchi yagona Canonical Orchestrator hisoblanadi. Yakuniy Market Context obyektini u emas, ContextService yaratadi.
