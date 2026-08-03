# Signal Builder
Status: CANONICAL
---
# Purpose
SignalBuilder GoldBot Signal Layer ichidagi Canonical Signal Constructor hisoblanadi.
Uning asosiy vazifasi Strategy Result va Technical Confluence asosida yagona standart Signal Result obyektini yaratishdir.
SignalBuilder signalni baholamaydi.
SignalBuilder signalni tasdiqlamaydi.
SignalBuilder AI ishlatmaydi.
SignalBuilder faqat Signal obyektini yaratadi.
---
# Objective
SignalBuilder quyidagi vazifalarni bajaradi.
• Signal Construction
• Signal Object Generation
• Entry Building
• Stop Loss Building
• Take Profit Building
• Metadata Construction
• Standard Signal Format Generation
---
# Layer Position
```text
Strategy Result
↓
Confluence Engine
↓
SignalBuilder
↓
Signal Validator
```
---
# Responsibilities
SignalBuilder
✓ Signal Direction yaratadi
✓ Entry yaratadi
✓ Stop Loss yaratadi
✓ Take Profit yaratadi
✓ Metadata yaratadi
✓ Standard Signal Result yaratadi
---
# Not Responsible
SignalBuilder
✗ Signal Validation
✗ Signal Scoring
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Input
SignalBuilder qabul qiladi.
• Strategy Result
• Technical Confluence
• Strategy Metadata
---
# Output
SignalBuilder yaratadi.
• Signal Result
• Direction
• Entry
• Stop Loss
• Take Profit
• Metadata
---
# Workflow
```text
Receive Strategy Result
↓
Build Signal Object
↓
Build Entry
↓
Build SL
↓
Build TP
↓
Build Metadata
↓
Signal Result
↓
Signal Validator
```
---
# Golden Rules
1. SignalBuilder faqat Signal yaratadi.
2. Signal Result immutable hisoblanadi.
3. Validation SignalBuilder ichida bajarilmaydi.
4. AI ishlatilmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
SignalBuilder/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
SignalBuilder GoldBot Signal Layer ichidagi Canonical Signal Constructor hisoblanadi.
