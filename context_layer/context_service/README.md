# ContextService
Status: CANONICAL
---
# Purpose
ContextService Context Layer ichidagi barcha Context modullarining natijalarini birlashtiruvchi yagona Canonical Service hisoblanadi.
Uning asosiy vazifasi barcha Context modullaridan olingan ma'lumotlarni yagona Market Context obyektiga aylantirish va keyingi Layer'lar uchun taqdim etishdir.
ContextService Context hisoblamaydi.
ContextService signal yaratmaydi.
ContextService AI ishlatmaydi.
ContextService faqat Context Aggregation bajaradi.
---
# Objective
ContextService quyidagi vazifalarni bajaradi:
• Context Aggregation
• Context Validation
• Context Normalization
• Context Versioning
• Context State Management
• Context Publishing
• Context Lifecycle Management
• Context Distribution
---
# Layer Position
```text
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
↓
Indicator Layer
```
---
# Responsibilities
ContextService:
✓ Context modullarini birlashtiradi
✓ Market Context yaratadi
✓ Context Validation bajaradi
✓ Context State boshqaradi
✓ Context Version yaratadi
✓ Context Publish qiladi
---
# Not Responsible
ContextService:
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
ContextService qabul qiladi:
• Market Structure
• Liquidity State
• Order Block State
• Fair Value Gap State
• Wyckoff State
• AMD State
• Session State
• Trend State
• Volume Profile State
---
# Output
ContextService yaratadi:
• Market Context
• Context Metadata
• Context Version
• Context Status
---
# Workflow
```text
Context Modules
↓
Aggregate Results
↓
Validate Context
↓
Normalize Context
↓
Build Market Context
↓
Publish Context
↓
Indicator Layer
```
---
# Golden Rules
1. ContextService yagona Market Context yaratadi.
2. Context modullarini o'zgartirmaydi.
3. Validation majburiy.
4. Context immutable hisoblanadi.
5. Signal yaratmaydi.
6. AI ishlatmaydi.
7. Circular Dependency taqiqlanadi.
---
# Related Documents
```text
ContextService/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
ContextService GoldBot Context Layer ichidagi barcha Context natijalarini yagona Market Context obyektiga aylantiruvchi Canonical Service hisoblanadi.
