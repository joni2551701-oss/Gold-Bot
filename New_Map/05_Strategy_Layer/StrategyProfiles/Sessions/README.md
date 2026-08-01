# Sessions
Status: CANONICAL
---
# Purpose
Sessions GoldBot Strategy Layer ichidagi barcha Trading Session konfiguratsiyalarini boshqaruvchi Canonical modul hisoblanadi.
Session strategiyani o'zgartirmaydi.
Session strategiyaning qachon ishlashini belgilaydi.
---
# Objective
Sessions quyidagi vazifalarni bajaradi.
• Trading Session Selection
• Session Filtering
• Session Validation
• Session Configuration
• Session Profile Generation
---
# Available Sessions
• Asia
• London
• New York
• London + New York Overlap
• Custom Session
---
# Responsibilities
Sessions:
✓ Trading Session tanlaydi
✓ Session vaqtlarini boshqaradi
✓ Session Filter yaratadi
✓ Strategy Configuration'ni to'ldiradi
✓ Strategy Profile yaratadi
---
# Not Responsible
Sessions:
✗ Strategy Logic
✗ Indicator Calculation
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
• Session Selection
---
# Output
• Session Configuration
• Session Profile
---
# Workflow
```text
User Settings
↓
Select Session
↓
Load Session Configuration
↓
Apply Session Filter
↓
StrategyEngine
```
---
# Golden Rules
1. Session strategiyani o'zgartirmaydi.
2. Session faqat qachon trade qilishni belgilaydi.
3. Har qanday Strategy istalgan Session bilan ishlashi mumkin.
4. Session Configuration immutable hisoblanadi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Sessions/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Sessions GoldBot ichidagi barcha Trading Session konfiguratsiyalarini boshqaruvchi Canonical modul hisoblanadi.
