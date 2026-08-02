# Risk Service
Status: CANONICAL
---
# Purpose
RiskService GoldBot Risk Layer ichidagi Canonical Public Risk Interface moduli hisoblanadi.
Uning asosiy vazifasi Risk Layer uchun yagona Service Gateway bo'lish va barcha tashqi Layer'lar bilan standart Risk API orqali ishlashdir.
RiskService Risk hisoblamaydi.
RiskService Risk Validation bajarmaydi.
RiskService faqat Risk Layer Service Gateway hisoblanadi.
---
# Objective
RiskService quyidagi vazifalarni bajaradi.
• Risk Request Management
• Risk API Gateway
• Request Validation
• Response Standardization
• Risk Session Management
• Risk Layer Integration
---
# Layer Position
```text
Decision Layer
↓
RiskService
↓
RiskEngine
↓
RiskValidator
↓
Execution Layer
```
---
# Responsibilities
RiskService
✓ Risk Request qabul qiladi
✓ Request formatini tekshiradi
✓ RiskEngine'ga uzatadi
✓ RiskValidator natijasini qabul qiladi
✓ Standard Risk Response yaratadi
✓ Execution Layer'ga uzatadi
---
# Not Responsible
RiskService
✗ Risk Calculation
✗ Position Size Calculation
✗ Drawdown Monitoring
✗ Portfolio Analysis
✗ Risk Approval
✗ Trade Execution
---
# Input
RiskService qabul qiladi.
• Decision Package
• Risk Request
• Session Metadata
---
# Output
RiskService yaratadi.
• Risk Response
• Standard Response
• Risk Metadata
• Service Metadata
---
# Workflow
```text
Receive Request
↓
Validate Request
↓
RiskEngine
↓
RiskValidator
↓
Receive Result
↓
Standardize Response
↓
Execution Layer
```
---
# Golden Rules
1. Risk Layer'ga barcha kirishlar RiskService orqali amalga oshiriladi.
2. RiskService Risk hisoblamaydi.
3. Response yagona formatda qaytariladi.
4. Risk Layer tashqarisiga faqat RiskService chiqadi.
5. Circular Dependency qat'iyan taqiqlanadi.
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
RiskService GoldBot Risk Layer uchun yagona Public Interface va Service Gateway hisoblanadi.
