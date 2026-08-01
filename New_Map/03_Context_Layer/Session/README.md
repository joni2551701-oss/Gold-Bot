# Session
Status: CANONICAL
---
# Purpose
Session Context Layer ichidagi Trading Session holatini aniqlovchi Canonical modul hisoblanadi.
Uning asosiy vazifasi bozorning qaysi sessiyada ishlayotganini aniqlash, Session Context yaratish va vaqtga bog'liq Market Behavior'ni tavsiflashdir.
Session signal yaratmaydi.
Session trade ochmaydi.
Session AI ishlatmaydi.
Session faqat Trading Session holatini aniqlaydi.
---
# Objective
Session quyidagi vazifalarni bajaradi:
• Session Detection
• Session Open Detection
• Session Close Detection
• Kill Zone Detection
• Session Overlap Detection
• Session Volatility Analysis
• Trading Day Classification
• Session State Generation
---
# Layer Position
```text
Market Data
↓
ContextEngine
↓
Session
↓
ContextService
```
---
# Responsibilities
Session:
✓ Asia Session aniqlaydi
✓ London Session aniqlaydi
✓ New York Session aniqlaydi
✓ Kill Zone aniqlaydi
✓ Session Overlap aniqlaydi
✓ Session Volatility aniqlaydi
✓ Trading Day Classification
✓ Session State yaratadi
---
# Not Responsible
Session:
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
Session qabul qiladi:
• Current Time
• Market Calendar
• Market Data
---
# Output
Session yaratadi:
• Current Session
• Session Open
• Session Close
• Kill Zone
• Session Overlap
• Session State
---
# Workflow
```text
Current Time
↓
Trading Calendar
↓
Detect Session
↓
Detect Kill Zone
↓
Detect Overlap
↓
Analyze Volatility
↓
Generate Session State
↓
ContextService
```
---
# Golden Rules
1. Session vaqt asosida aniqlanadi.
2. Kill Zone Session ichida aniqlanadi.
3. Session State har bir yangi Candle bilan yangilanadi.
4. Signal yaratilmaydi.
5. AI ishlatilmaydi.
6. Circular Dependency taqiqlanadi.
---
# Related Documents
```text
Session/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Session GoldBot Context Layer ichidagi Trading Session holatini aniqlovchi yagona Canonical modul hisoblanadi.
