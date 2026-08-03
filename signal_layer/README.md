# Signal Layer
Status: CANONICAL
---
# Purpose
Signal Layer GoldBot arxitekturasidagi texnik Signal Generation qatlami hisoblanadi.
Uning asosiy vazifasi Context Layer, Indicator Layer va Strategy Layer natijalarini birlashtirib, standart Signal Result yaratishdir.
Signal Layer AI ishlatmaydi.
Signal Layer yakuniy trading qarorini qabul qilmaydi.
Signal Layer trade ochmaydi.
Signal Layer faqat texnik signal ishlab chiqaradi.
---
# Objective
Signal Layer quyidagi vazifalarni bajaradi.
• Strategy natijalarini qabul qilish
• Technical Confluence yaratish
• Signal Generation
• Signal Validation
• Signal Scoring
• Signal Formatting
• Signal Delivery
---
# Layer Position
```text
03_Context_Layer
↓
04_Indicator_Layer
↓
05_Strategy_Layer
↓
06_Signal_Layer
↓
07_AI_Layer
```
---
# Internal Modules
```text
Signal Layer
├── SignalEngine
├── SignalBuilder
├── SignalValidator
├── ConfluenceEngine
├── SignalScoring
├── SignalFormatter
└── SignalService
```
---
# Responsibilities
Signal Layer
✓ Strategy natijalarini qabul qiladi
✓ Technical Confluence yaratadi
✓ BUY / SELL / NONE Signal yaratadi
✓ Signal Validation bajaradi
✓ Signal Score hisoblaydi
✓ Signal Confidence hisoblaydi
✓ Signal Format yaratadi
✓ Signal Result uzatadi
---
# Not Responsible
Signal Layer
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
Signal Layer qabul qiladi.
• Market Context
• Indicator Context
• Strategy Result
• Strategy Metadata
---
# Output
Signal Layer yaratadi.
• Signal Result
• Signal Direction
• Entry Price
• Stop Loss
• Take Profit
• Technical Score
• Technical Confidence
• Signal Metadata
---
# Workflow
```text
Strategy Result
↓
Signal Engine (Pipeline Orchestration)
↓
Confluence Engine
↓
Signal Builder
↓
Signal Validator
↓
Signal Scoring
↓
Signal Formatter
↓
Signal Service
↓
AI Layer
```
---
# Golden Rules
1. Signal Layer faqat texnik signal yaratadi.
2. AI Signal yaratmaydi.
3. Decision Signal Layer ichida qabul qilinmaydi.
4. Signal Result immutable hisoblanadi.
5. Har bir Signal Validation'dan o'tishi shart.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
06_Signal_Layer/
├── README.md
├── SignalEngine/
├── SignalBuilder/
├── SignalValidator/
├── ConfluenceEngine/
├── SignalScoring/
├── SignalFormatter/
├── SignalService/
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
└── Layer_Contracts.md
```
---
# Summary
Signal Layer GoldBot arxitekturasidagi texnik Signal Generation qatlami bo'lib, Strategy Layer natijalaridan standart Signal Result yaratadi va uni AI Layer'ga uzatadi.
