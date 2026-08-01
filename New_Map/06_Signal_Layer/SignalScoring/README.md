# Signal Scoring
Status: CANONICAL
---
# Purpose
SignalScoring GoldBot Signal Layer ichidagi Canonical Signal Evaluation moduli hisoblanadi.
Uning asosiy vazifasi Technical Confluence va Valid Signal Result asosida Signal Score hamda Technical Confidence hisoblashdir.
SignalScoring signal yaratmaydi.
SignalScoring AI ishlatmaydi.
SignalScoring Decision qabul qilmaydi.
SignalScoring faqat texnik baholashni amalga oshiradi.
---
# Objective
SignalScoring quyidagi vazifalarni bajaradi.
• Technical Score Calculation
• Confidence Calculation
• Signal Ranking
• Score Normalization
• Quality Evaluation
• Technical Rating
---
# Layer Position
```text
Signal Validator
↓
SignalScoring
↓
Signal Formatter
```
---
# Responsibilities
SignalScoring
✓ Technical Score hisoblaydi
✓ Technical Confidence hisoblaydi
✓ Signal Quality baholaydi
✓ Score Normalization bajaradi
✓ Signal Rating yaratadi
✓ Score Metadata yaratadi
---
# Not Responsible
SignalScoring
✗ Signal Generation
✗ Signal Validation
✗ Signal Formatting
✗ AI Analysis
✗ Decision Making
✗ Risk Management
✗ Trade Execution
---
# Input
SignalScoring qabul qiladi.
• Valid Signal Result
• Technical Confluence
• Validation Result
---
# Output
SignalScoring yaratadi.
• Technical Score
• Technical Confidence
• Signal Rating
• Score Metadata
---
# Workflow
```text
Receive Valid Signal
↓
Load Technical Confluence
↓
Calculate Technical Score
↓
Calculate Confidence
↓
Normalize Score
↓
Generate Score Result
↓
Signal Formatter
```
---
# Golden Rules
1. SignalScoring faqat texnik baholashni bajaradi.
2. AI ishlatilmaydi.
3. Decision qabul qilinmaydi.
4. Score deterministik bo'lishi kerak.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
SignalScoring/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
SignalScoring GoldBot Signal Layer ichidagi barcha Signal Result obyektlari uchun Technical Score va Technical Confidence hisoblovchi Canonical modul hisoblanadi.
