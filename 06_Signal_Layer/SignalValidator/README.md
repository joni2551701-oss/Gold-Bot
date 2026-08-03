# Signal Validator
Status: CANONICAL
---
# Purpose
SignalValidator GoldBot Signal Layer ichidagi Canonical Signal Validation moduli hisoblanadi.
Uning asosiy vazifasi SignalBuilder tomonidan yaratilgan Signal Result obyektini texnik va arxitektura qoidalari asosida tekshirishdir.
SignalValidator signal yaratmaydi.
SignalValidator signalni baholamaydi.
SignalValidator AI ishlatmaydi.
SignalValidator faqat Signal Validation bajaradi.
---
# Objective
SignalValidator quyidagi vazifalarni bajaradi.
• Signal Validation
• Signal Integrity Check
• Required Field Validation
• Technical Rule Validation
• Boundary Validation
• Signal Approval
• Signal Rejection
---
# Layer Position
```text
Signal Builder
↓
Signal Validator
↓
Signal Scoring
```
---
# Responsibilities
SignalValidator
✓ Signal Result tekshiradi
✓ Required maydonlarni tekshiradi
✓ Entry / SL / TP ni tekshiradi
✓ Direction ni tekshiradi
✓ Technical Rule tekshiradi
✓ Validation Result yaratadi
---
# Not Responsible
SignalValidator
✗ Signal Generation
✗ Signal Formatting
✗ Signal Scoring
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Input
SignalValidator qabul qiladi.
• Signal Result
• Technical Metadata
---
# Output
SignalValidator yaratadi.
• Validation Result
• Validation Status
• Validation Errors
• Valid Signal Result
---
# Workflow
```text
Receive Signal
↓
Validate Fields
↓
Validate Technical Rules
↓
Validate Integrity
↓
Approve / Reject
↓
Signal Scoring
```
---
# Golden Rules
1. Har bir Signal Validation'dan o'tishi shart.
2. Validation deterministik bo'lishi kerak.
3. Validation Signal Result'ni o'zgartirmaydi.
4. AI ishlatilmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
SignalValidator/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
SignalValidator GoldBot Signal Layer ichidagi barcha Signal Result obyektlarini tekshiruvchi Canonical Validation modulidir.
