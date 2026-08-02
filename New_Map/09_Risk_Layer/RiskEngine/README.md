# Risk Engine
Status: CANONICAL
---
# Purpose
RiskEngine GoldBot Risk Layer ichidagi Canonical Core Risk Assessment moduli hisoblanadi.
Uning asosiy vazifasi Trade uchun barcha Risk komponentlarini yig'ish, tahlil qilish va Risk Evaluation Pipeline'ni boshqarishdir.
RiskEngine Trade Decision qabul qilmaydi.
RiskEngine Order ochmaydi.
RiskEngine faqat Risk Assessment bilan shug'ullanadi.
---
# Objective
RiskEngine quyidagi vazifalarni bajaradi.
• Risk Assessment
• Risk Context Aggregation
• Risk Evaluation
• Risk Pipeline Management
• Risk Context Generation
• Risk Report Generation
---
# Layer Position
```text
Decision Layer
↓
RiskEngine
↓
PositionSizing
↓
MoneyManagement
```
---
# Responsibilities
RiskEngine
✓ Decision ma'lumotlarini qabul qiladi
✓ Account holatini tekshiradi
✓ Risk Context yaratadi
✓ Risk Pipeline'ni boshlaydi
✓ Risk Report yaratadi
✓ Risk modullarini boshqaradi
---
# Not Responsible
RiskEngine
✗ Final Decision
✗ Lot Size Calculation
✗ Drawdown Control
✗ Exposure Control
✗ Trade Execution
✗ Position Monitoring
---
# Input
RiskEngine qabul qiladi.
• Final Decision
• Account Information
• Symbol Information
• Market Context
• Risk Preferences
---
# Output
RiskEngine yaratadi.
• Risk Context
• Risk Report
• Risk Metadata
• Risk Package
---
# Workflow
```text
Receive Decision
↓
Validate Inputs
↓
Collect Risk Context
↓
Generate Risk Package
↓
PositionSizing
```
---
# Golden Rules
1. RiskEngine faqat APPROVED Decision bilan ishlaydi.
2. RiskEngine Decision'ni o'zgartirmaydi.
3. Risk Pipeline yagona Risk Context bilan ishlaydi.
4. Risk Assessment standart formatda yaratiladi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
RiskEngine/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
RiskEngine GoldBot Risk Layer ichidagi barcha Risk Assessment jarayonlarini boshlovchi va boshqaruvchi Canonical modul hisoblanadi.
