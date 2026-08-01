# Signal Engine
Status: CANONICAL
---
# Purpose
SignalEngine GoldBot Signal Layer ichidagi barcha Signal Generation jarayonini boshqaruvchi Canonical Engine hisoblanadi.
Uning asosiy vazifasi Confluence natijasidan standart Signal Result yaratish va Signal Layer ichidagi barcha modullarni orchestration qilishdir.
SignalEngine AI ishlatmaydi.
SignalEngine yakuniy trading qarorini qabul qilmaydi.
SignalEngine trade ochmaydi.
SignalEngine faqat texnik Signal Pipeline'ni boshqaradi.
---
# Objective
SignalEngine quyidagi vazifalarni bajaradi.
• Signal Pipeline Management
• Confluence Processing
• Signal Generation
• Signal Validation
• Signal Scoring
• Signal Formatting
• Signal Lifecycle Management
---
# Layer Position
```text
Strategy Layer
↓
SignalEngine
↓
Signal Service
```
---
# Responsibilities
SignalEngine
✓ Signal Pipeline boshqaradi
✓ SignalBuilder'ni ishga tushiradi
✓ SignalValidator'ni boshqaradi
✓ SignalScoring'ni ishga tushiradi
✓ SignalFormatter'ni boshqaradi
✓ Signal Result yaratadi
---
# Not Responsible
SignalEngine
✗ Market Analysis
✗ Context Analysis
✗ Indicator Calculation
✗ Strategy Analysis
✗ AI Analysis
✗ Decision Making
✗ Risk Management
✗ Trade Execution
---
# Input
SignalEngine qabul qiladi.
• Strategy Result
• Technical Confluence
• Strategy Metadata
---
# Output
SignalEngine yaratadi.
• Signal Result
• Technical Score
• Technical Confidence
• Signal Metadata
---
# Workflow
```text
Receive Strategy Result
↓
Load Confluence
↓
Build Signal
↓
Validate Signal
↓
Calculate Score
↓
Format Signal
↓
Signal Service
```
---
# Golden Rules
1. SignalEngine faqat Signal Layer ichida ishlaydi.
2. Har bir Signal Validation'dan o'tishi shart.
3. Signal Result immutable hisoblanadi.
4. AI ishlatilmaydi.
5. Decision qabul qilinmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
SignalEngine/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
SignalEngine GoldBot Signal Layer ichidagi barcha Signal Generation Pipeline'ni boshqaruvchi Canonical Engine hisoblanadi.
