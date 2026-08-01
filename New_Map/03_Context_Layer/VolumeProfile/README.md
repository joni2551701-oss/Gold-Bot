# Volume Profile
Status: CANONICAL
---
# Purpose
VolumeProfile Context Layer ichidagi Volume Profile va Auction Market Structure'ni aniqlovchi Canonical modul hisoblanadi.
Uning asosiy vazifasi bozordagi hajm taqsimotini tahlil qilish, muhim narx darajalarini aniqlash va Market Context uchun Volume Profile State yaratishdir.
VolumeProfile signal yaratmaydi.
VolumeProfile trade ochmaydi.
VolumeProfile AI ishlatmaydi.
VolumeProfile faqat hajm asosidagi Market Context yaratadi.
---
# Objective
VolumeProfile quyidagi vazifalarni bajaradi:
• Volume Profile Generation
• Point of Control (POC) Detection
• Value Area Calculation
• VAH Detection
• VAL Detection
• HVN Detection
• LVN Detection
• Volume Distribution Analysis
• Volume Profile State Generation
---
# Layer Position
```text
Market Data
↓
ContextEngine
↓
VolumeProfile
↓
ContextService
```
---
# Responsibilities
VolumeProfile:
✓ Volume Profile yaratadi
✓ Point of Control aniqlaydi
✓ Value Area hisoblaydi
✓ VAH aniqlaydi
✓ VAL aniqlaydi
✓ HVN aniqlaydi
✓ LVN aniqlaydi
✓ Volume Distribution tahlil qiladi
✓ Volume Profile State yaratadi
---
# Not Responsible
VolumeProfile:
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
VolumeProfile qabul qiladi:
• OHLC Data
• Volume Data
• Historical Data
• Session State
---
# Output
VolumeProfile yaratadi:
• Volume Profile
• POC
• VAH
• VAL
• HVN
• LVN
• Volume Profile State
---
# Workflow
```text
Market Data
↓
Load Volume
↓
Build Volume Profile
↓
Calculate POC
↓
Calculate Value Area
↓
Detect HVN/LVN
↓
Generate Volume Profile State
↓
ContextService
```
---
# Golden Rules
1. Volume Profile faqat Volume Data asosida hisoblanadi.
2. POC doimo hisoblanadi.
3. Value Area har doim yangilanadi.
4. HVN/LVN Profile'dan olinadi.
5. Signal yaratilmaydi.
6. AI ishlatilmaydi.
7. Circular Dependency taqiqlanadi.
---
# Related Documents
```text
VolumeProfile/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
VolumeProfile GoldBot Context Layer ichidagi Auction Market va Volume Distribution holatini aniqlovchi yagona Canonical modul hisoblanadi.
