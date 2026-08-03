# Context Layer
Status: CANONICAL
---
# Purpose
Context Layer GoldBot Trading Engine ichidagi Market Context yaratish uchun javobgar yagona Layer hisoblanadi.
Bu Layer bozorni tahlil qiladi va barcha Strategy hamda AI modullari foydalanadigan yagona Market Context obyektini yaratadi.
Context Layer signal yaratmaydi.
Context Layer trade qarorini chiqarmaydi.
Context Layer AI ishlatmaydi.
Context Layer faqat bozor holatini aniqlaydi.
---
# Objective
Context Layer quyidagi vazifalarni bajaradi:
• Market Structure Analysis
• Liquidity Analysis
• Order Block Detection
• Fair Value Gap Detection
• Wyckoff Analysis
• AMD Analysis
• Session Analysis
• Trend Analysis
• Volume Profile Analysis
• Market Context Generation
---
# Layer Position
```text
Data Layer
↓
Core Layer
↓
Context Layer
↓
Indicator Layer
```
---
# Responsibilities
Context Layer:
✓ Market Context yaratadi
✓ Market Structure hisoblaydi
✓ Liquidity aniqlaydi
✓ Order Block aniqlaydi
✓ Fair Value Gap aniqlaydi
✓ Wyckoff holatini aniqlaydi
✓ AMD Phase aniqlaydi
✓ Session holatini aniqlaydi
✓ Trend aniqlaydi
✓ Volume Profile yaratadi
---
# Not Responsible
Context Layer:
✗ Indicator hisoblamaydi
✗ Strategy ishlatmaydi
✗ Signal yaratmaydi
✗ AI Analysis bajarmaydi
✗ Decision chiqarmaydi
✗ Risk hisoblamaydi
✗ Trade ochmaydi
---
# Input
Context Layer qabul qiladi:
• Validated Market Data
• Current Candle
• Historical Candle Data
• Session Information
---
# Output
Context Layer yaratadi:
• Market Context
• Context Events
• Structure State
• Liquidity State
• Trend State
---
# Internal Modules
• ContextEngine
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
Validated Market Data
↓
Market Structure
↓
Liquidity
↓
Order Block
↓
Fair Value Gap
↓
Wyckoff
↓
AMD
↓
Session
↓
Trend
↓
Volume Profile
↓
Market Context
↓
Indicator Layer
```
---
# Golden Rules
1. Context Layer Market Context yaratadi.
2. Indicator hisoblamaydi.
3. Signal yaratmaydi.
4. Strategy bajarmaydi.
5. AI ishlatmaydi.
6. Market Context yagona Source of Truth hisoblanadi.
7. Circular Dependency taqiqlanadi.
---
# Related Documents
```text
03_Context_Layer/
├── README.md
├── ContextEngine/
├── MarketStructure/
├── Liquidity/
├── OrderBlock/
├── FairValueGap/
├── Wyckoff/
├── AMD/
├── Session/
├── Trend/
├── VolumeProfile/
├── ContextService/
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
└── Layer_Contracts.md
```
---
# Summary
Context Layer GoldBot Trading Engine uchun yagona Canonical Market Context Layer hisoblanadi.
