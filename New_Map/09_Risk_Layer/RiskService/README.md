# Risk Service
Status: CANONICAL
---
# Purpose
RiskService GoldBot Risk Layer uchun Canonical Boundary Gateway hisoblanadi.
Uning asosiy vazifasi Risk Layer'ning yagona Public Entry Point va Public Exit Point bo'lishidir — Decision Layer'dan kelgan so'rovlarni RiskEngine'ga kiritish va RiskValidator'dan qaytgan yakuniy Risk Approval'ni Execution Layer'ga chiqarish.
RiskService Risk hisoblamaydi.
RiskService Risk Validation bajarmaydi.
RiskService faqat Entry/Exit Boundary, Validation va Serialization vazifalarini bajaradi.
---
# Objective
RiskService quyidagi vazifalarni bajaradi.
• Public Entry Point
• Public Exit Point
• Request Validation
• Response Serialization
• Session Management
• API Boundary Enforcement
---
# Layer Position
```text
Decision Layer
↓
RiskService (Entry)
↓
RiskEngine
↓
PositionSizing
↓
MoneyManagement
↓
DrawdownManager
↓
ExposureManager
↓
PortfolioManager
↓
RiskValidator
↓
RiskService (Exit)
↓
Execution Layer
```
---
# Responsibilities
RiskService
✓ Decision Layer'dan Risk Request qabul qiladi (Entry)
✓ Request formatini tekshiradi
✓ RiskEngine'ga uzatadi
✓ RiskValidator'dan Risk Approval qabul qiladi
✓ Standard Risk Response yaratadi
✓ Execution Layer'ga uzatadi (Exit)
---
# Not Responsible
RiskService
✗ Risk Calculation
✗ Position Size Calculation
✗ Money Management
✗ Drawdown Monitoring
✗ Exposure Control
✗ Portfolio Analysis
✗ Risk Validation
✗ Trade Execution
---
# Input
RiskService qabul qiladi.
• Decision Package (Decision Layer'dan)
• Risk Approval (RiskValidator'dan)
• Session Metadata
---
# Output
RiskService yaratadi.
• Validated Risk Request (RiskEngine'ga)
• Risk Response (Execution Layer'ga)
• Standard Response
• Service Metadata
---
# Workflow
```text
Receive Request (Decision Layer)
↓
Validate Request
↓
Forward To RiskEngine
↓
Receive Risk Approval (RiskValidator)
↓
Standardize Response
↓
Return Response (Execution Layer)
```
---
# Golden Rules
1. RiskService Risk Layer'ning yagona Entry Point va yagona Exit Point hisoblanadi.
2. Risk Logic RiskService ichida bajarilmaydi.
3. Risk javoblari standart formatga o'tkaziladi.
4. Risk Layer tashqarisiga faqat RiskService orqali kiriladi va chiqiladi.
5. RiskValidator Layer tashqarisiga chiqmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
RiskService/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
RiskService GoldBot Risk Layer uchun ikki tomonlama (bidirectional) Boundary Gateway hisoblanadi — Decision Layer'dan Risk Layer'ga kirish va Risk Layer'dan Execution Layer'ga chiqish uchun yagona nuqta.
