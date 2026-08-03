# Features Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Features modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Features quyidagilar uchun javobgar.
✓ Mavjud tahlil natijalarini yagona Feature obyektiga yig'adi
✓ Feature'larni standart formatga keltiradi
✓ Feature'larni normalizatsiya qiladi
✓ AI, Strategy, Backtesting va ML Export uchun umumiy kutubxona vazifasini bajaradi
Features bajarmaydi.
✗ Indicator Calculation (04_Indicator_Layer vazifasi)
✗ Market Analysis
✗ Signal Generation
✗ AI Analysis
✗ Trading Decision
✗ Risk Calculation
---
# Module Boundary
```text
Analysis Results (Context, Signal Quality, Explainability)
↓
Features
↓
AI Layer / Backtesting Layer / ML Export
```
---
# Input Contract
• Market Regime Result
• Session Event
• HTF Bias Result
• Liquidity Zones
• Signal Quality Score
• Signal Explanation
---
# Output Contract
• Market Features Snapshot
• Normalized Feature Set
• Feature Metadata
---
# Allowed Dependencies
✓ CoreEngine
✓ Configuration
---
# Forbidden Dependencies
✗ Strategy Layer
✗ Signal Layer
✗ AI Layer (to'g'ridan-to'g'ri)
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Runtime Contract
1. Features hech qachon yangi qiymat hisoblamaydi — faqat mavjud natijalarni qayta ishlatadi.
2. Har bir Feature manbasi aniq bo'lishi shart (qaysi modul hisoblagan).
3. Mavjud bo'lmagan Feature None sifatida qoladi — hech qachon to'qib chiqarilmaydi.
4. Features analiz zanjirining OXIRIDA ishlaydi (Signal Quality va Explainability'dan keyin).
5. Features Signal, Decision yoki Risk natijasiga ta'sir qilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Mavjud natijalar qabul qilinadi.
✓ Feature Snapshot yaratiladi.
✓ Feature'lar standartlashtiriladi.
✓ Hech qanday qiymat to'qib chiqarilmaydi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Features Contract Features GoldBot Core Layer ichidagi Canonical Feature Standardization moduli hisoblanadi. U AI, Strategy, Backtesting va ML Export uchun umumiy Feature obyektlarini tayyorlaydi — hech qachon yangi tahlil bajarmaydi.
