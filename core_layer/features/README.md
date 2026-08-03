# Features
Status: CANONICAL
---
# Purpose
Features — GoldBot Core Layer ichidagi Canonical Feature Standardization komponentidir.
Uning asosiy vazifasi pipeline davomida allaqachon hisoblangan natijalarni (Market Regime, Session, HTF Bias, Liquidity, Signal Quality, Explainability) yagona standart Feature obyektiga aylantirishdir.
Features yangi indikator hisoblamaydi.
Features ML model ishlatmaydi.
Features Signal yoki Decision yaratmaydi.
Director Decision (Architecture Gap Review v1.0 #2): Features 04_Indicator_Layer yoki 07_AI_Layer ichiga qo'shilmaydi — u biznes modul emas, balki bir nechta Layer (AI, Strategy, Backtesting, ML Export) foydalanadigan umumiy kutubxona, shuning uchun Canonical joyi 02_Core_Layer hisoblanadi.
---
# Objective
Features quyidagi vazifalarni bajaradi.
• Feature Extraction (mavjud natijalardan)
• Feature Standardization
• Feature Normalization
• Feature Snapshot Generation
• AI / Strategy / Backtesting / ML Export uchun umumiy format
---
# Layer Position
```text
Analysis Results (Context, Signal Quality, Explainability)
↓
Features
↓
AI Layer / Backtesting Layer / ML Export
```
---
# Responsibilities
Features
✓ Mavjud tahlil natijalarini yagona Feature obyektiga yig'adi
✓ Feature'larni standart formatga keltiradi
✓ Feature'larni normalizatsiya qiladi
✓ AI, Strategy, Backtesting va ML Export uchun umumiy kutubxona vazifasini bajaradi
---
# Not Responsible
Features
✗ Indicator Calculation (04_Indicator_Layer vazifasi)
✗ Market Analysis
✗ Signal Generation
✗ AI Analysis
✗ Trading Decision
✗ Risk Calculation
---
# Input
Features qabul qiladi.
• Market Regime Result
• Session Event
• HTF Bias Result
• Liquidity Zones
• Signal Quality Score
• Signal Explanation
---
# Output
Features yaratadi.
• Market Features Snapshot
• Normalized Feature Set
• Feature Metadata
---
# Workflow
```text
Analysis Results (Context, Signal Quality, Explainability)
↓
Features
↓
AI Layer / Backtesting Layer / ML Export
```
---
# Internal Modules (Planned — implementatsiya bosqichida to'ldiriladi)
```text
Features
├── FeatureEngine
├── FeatureModel
└── FeatureNormalizer
```
---
# Golden Rules
1. Features hech qachon yangi qiymat hisoblamaydi — faqat mavjud natijalarni qayta ishlatadi.
2. Har bir Feature manbasi aniq bo'lishi shart (qaysi modul hisoblagan).
3. Mavjud bo'lmagan Feature None sifatida qoladi — hech qachon to'qib chiqarilmaydi.
4. Features analiz zanjirining OXIRIDA ishlaydi (Signal Quality va Explainability'dan keyin).
5. Features Signal, Decision yoki Risk natijasiga ta'sir qilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Features/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
Features GoldBot Core Layer ichidagi Canonical Feature Standardization moduli hisoblanadi. U AI, Strategy, Backtesting va ML Export uchun umumiy Feature obyektlarini tayyorlaydi — hech qachon yangi tahlil bajarmaydi.
