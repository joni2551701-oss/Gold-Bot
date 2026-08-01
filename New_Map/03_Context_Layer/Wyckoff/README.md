# Wyckoff
Status: CANONICAL
---
# Purpose
Wyckoff Context Layer ichidagi Wyckoff Market Cycle va Composite Operator faoliyatini aniqlovchi Canonical modul hisoblanadi.
Uning asosiy vazifasi bozordagi Accumulation, Distribution va Re-Accumulation / Re-Distribution jarayonlarini aniqlash hamda Market Context uchun Wyckoff State yaratishdir.
Wyckoff signal yaratmaydi.
Wyckoff trade ochmaydi.
Wyckoff AI ishlatmaydi.
Wyckoff faqat Wyckoff Market Cycle'ni aniqlaydi.
---
# Objective
Wyckoff quyidagi vazifalarni bajaradi:
• Market Phase Detection
• Accumulation Detection
• Distribution Detection
• Re-Accumulation Detection
• Re-Distribution Detection
• Composite Operator Analysis
• Spring Detection
• Upthrust Detection
• SOS Detection
• SOW Detection
• Wyckoff State Generation
---
# Layer Position
```text
Market Data
↓
MarketStructure
↓
Liquidity
↓
Wyckoff
↓
ContextService
```
---
# Responsibilities
Wyckoff:
✓ Market Phase aniqlaydi
✓ Accumulation aniqlaydi
✓ Distribution aniqlaydi
✓ Re-Accumulation aniqlaydi
✓ Re-Distribution aniqlaydi
✓ Spring aniqlaydi
✓ Upthrust aniqlaydi
✓ SOS aniqlaydi
✓ SOW aniqlaydi
✓ Wyckoff State yaratadi
---
# Not Responsible
Wyckoff:
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
Wyckoff qabul qiladi:
• OHLC Data
• Market Structure
• Liquidity State
• Volume Profile
---
# Output
Wyckoff yaratadi:
• Market Phase
• Spring Events
• Upthrust Events
• SOS Events
• SOW Events
• Wyckoff State
---
# Workflow
```text
Market Data
↓
Market Structure
↓
Liquidity
↓
Volume Profile
↓
Detect Market Phase
↓
Detect Wyckoff Events
↓
Generate Wyckoff State
↓
ContextService
```
---
# Golden Rules
1. Wyckoff faqat Market Context asosida aniqlanadi.
2. Market Phase doimo aniqlanadi.
3. Spring va Upthrust Phase ichida tekshiriladi.
4. Wyckoff State doimo yangilanadi.
5. Signal yaratilmaydi.
6. AI ishlatilmaydi.
7. Circular Dependency taqiqlanadi.
---
# Related Documents
```text
Wyckoff/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Wyckoff GoldBot Context Layer ichidagi Wyckoff Market Cycle'ni aniqlovchi yagona Canonical modul hisoblanadi.
