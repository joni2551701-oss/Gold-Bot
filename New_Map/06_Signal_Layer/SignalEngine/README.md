# Signal Engine
Status: CANONICAL
---
# Purpose
SignalEngine GoldBot Signal Layer ichidagi Pipeline Orchestrator hisoblanadi, xuddi Core Layer'dagi CoreEngine, Context Layer'dagi ContextEngine va Indicator Layer'dagi IndicatorEngine kabi.
Uning asosiy vazifasi Strategy Result kelganidan so'ng ConfluenceEngine, SignalBuilder, SignalValidator, SignalScoring va SignalFormatter'ni to'g'ri ketma-ketlikda ishga tushirish va Runtime'ni boshqarishdir.
SignalEngine Confluence hisoblamaydi, Signal Build qilmaydi, Validation, Scoring yoki Formatting bajarmaydi — bularning har biri o'z modulining vazifasi.
SignalEngine AI ishlatmaydi.
SignalEngine yakuniy trading qarorini qabul qilmaydi.
SignalEngine faqat Pipeline Orchestration, Module Coordination, Execution Order va Runtime Control bilan shug'ullanadi.
---
# Objective
SignalEngine quyidagi vazifalarni bajaradi.
• Pipeline Orchestration
• Module Coordination
• Execution Order Management
• Runtime Control
• Signal Lifecycle Management
---
# Layer Position
```text
Strategy Layer
↓
SignalEngine
↓
ConfluenceEngine → SignalBuilder → SignalValidator → SignalScoring → SignalFormatter
↓
Signal Service
```
---
# Responsibilities
SignalEngine
✓ Pipeline bosqichlarini to'g'ri ketma-ketlikda ishga tushiradi
✓ ConfluenceEngine, SignalBuilder, SignalValidator, SignalScoring, SignalFormatter'ni muvofiqlashtiradi
✓ Runtime holatini boshqaradi
✓ Execution Order'ni belgilaydi
✓ Signal Lifecycle'ni boshqaradi
---
# Not Responsible
SignalEngine
✗ Technical Confluence yaratish (ConfluenceEngine vazifasi)
✗ Signal Build qilish (SignalBuilder vazifasi)
✗ Signal Validation (SignalValidator vazifasi)
✗ Signal Scoring (SignalScoring vazifasi)
✗ Signal Formatting (SignalFormatter vazifasi)
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
• Strategy Metadata
---
# Output
SignalEngine yaratadi.
• Pipeline Execution Order
• Runtime Status
• Coordination Events
---
# Workflow
```text
Receive Strategy Result
↓
Initiate Pipeline
↓
Invoke ConfluenceEngine
↓
Invoke SignalBuilder
↓
Invoke SignalValidator
↓
Invoke SignalScoring
↓
Invoke SignalFormatter
↓
Forward Result to SignalService
```
---
# Golden Rules
1. SignalEngine faqat Signal Layer ichida ishlaydi.
2. SignalEngine hech qanday bosqichning ichki hisob-kitobini o'zi bajarmaydi — faqat ketma-ketlikni boshqaradi.
3. Har bir bosqich natijasi keyingisiga o'zgartirilmasdan uzatiladi.
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
SignalEngine GoldBot Signal Layer ichidagi Pipeline Orchestration, Module Coordination va Runtime Control'ni boshqaruvchi Canonical Engine hisoblanadi. Confluence, Build, Validation, Scoring va Formatting har biri o'z modulida bajariladi, SignalEngine faqat ularning bajarilish ketma-ketligini boshqaradi.
