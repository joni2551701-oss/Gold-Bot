# AMD
Status: CANONICAL
---
# Purpose
AMD Context Layer ichidagi Accumulation–Manipulation–Distribution (AMD) Market Cycle'ni aniqlovchi Canonical modul hisoblanadi.
Uning asosiy vazifasi bozordagi Institutional AMD siklini aniqlash va Market Context uchun AMD State yaratishdir.
AMD signal yaratmaydi.
AMD trade ochmaydi.
AMD AI ishlatmaydi.
AMD faqat Market Cycle holatini aniqlaydi.
---
# Objective
AMD quyidagi vazifalarni bajaradi:
• Accumulation Detection
• Manipulation Detection
• Distribution Detection
• Phase Transition Detection
• Range Detection
• Liquidity Manipulation Detection
• Breakout Confirmation
• AMD State Generation
---
# Layer Position
```text
Market Data
↓
MarketStructure
↓
Liquidity
↓
AMD
↓
ContextService
```
---
# Responsibilities
AMD:
✓ Accumulation aniqlaydi
✓ Manipulation aniqlaydi
✓ Distribution aniqlaydi
✓ Phase Transition aniqlaydi
✓ Range aniqlaydi
✓ Liquidity Manipulation aniqlaydi
✓ Breakout Confirmation
✓ AMD State yaratadi
---
# Not Responsible
AMD:
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
AMD qabul qiladi:
• OHLC Data
• Market Structure
• Liquidity State
---
# Output
AMD yaratadi:
• AMD Phase
• Accumulation Zone
• Manipulation Zone
• Distribution Zone
• Phase Events
• AMD State
---
# Workflow
```text
Market Data
↓
Market Structure
↓
Liquidity
↓
Detect Accumulation
↓
Detect Manipulation
↓
Detect Distribution
↓
Generate AMD State
↓
ContextService
```
---
# Golden Rules
1. AMD faqat Market Context asosida hisoblanadi.
2. Phase ketma-ketligi saqlanadi.
3. Manipulation Liquidity bilan tasdiqlanadi.
4. AMD State doimo yangilanadi.
5. Signal yaratilmaydi.
6. AI ishlatilmaydi.
7. Circular Dependency taqiqlanadi.
---
# Related Documents
```text
AMD/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
AMD GoldBot Context Layer ichidagi Institutional AMD Cycle'ni aniqlovchi yagona Canonical modul hisoblanadi.
