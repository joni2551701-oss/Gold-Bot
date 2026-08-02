# Risk Validator
Status: CANONICAL
---
# Purpose
RiskValidator GoldBot Risk Layer ichidagi Canonical Final Risk Validation moduli hisoblanadi.
Uning asosiy vazifasi Risk Layer ichidagi barcha modullar natijalarini tekshirib, Trade Execution uchun yakuniy Risk Approval yaratishdir.
RiskValidator Risk hisoblamaydi.
RiskValidator Position Size hisoblamaydi.
RiskValidator faqat yakuniy Risk Validation bilan shug'ullanadi.
---
# Objective
RiskValidator quyidagi vazifalarni bajaradi.
• Final Risk Validation
• Risk Policy Validation
• Capital Protection Validation
• Risk Approval
• Reject Reason Generation
• Risk Report Generation
---
# Layer Position
```text
PortfolioManager
↓
RiskValidator
↓
RiskService
↓
Execution Layer
```
---
# Responsibilities
RiskValidator
✓ Risk Reportlarni tekshiradi
✓ Money Management natijalarini tekshiradi
✓ Drawdown natijalarini tekshiradi
✓ Exposure natijalarini tekshiradi
✓ Portfolio natijalarini tekshiradi
✓ Yakuniy Risk Approval yaratadi
---
# Not Responsible
RiskValidator
✗ Position Size Calculation
✗ Money Management
✗ Drawdown Monitoring
✗ Exposure Monitoring
✗ Portfolio Calculation
✗ Trade Execution
---
# Input
RiskValidator qabul qiladi.
• Risk Context
• Position Package
• Money Report
• Drawdown Report
• Exposure Report
• Portfolio Report
---
# Output
RiskValidator yaratadi.
• Risk Approval
• Risk Status
• Reject Reason
• Risk Validation Report
• Risk Metadata
---
# Risk States
• APPROVED
• REJECTED
• REDUCE
• BLOCKED
---
# Workflow
```text
Receive Risk Reports
↓
Validate All Risk Modules
↓
Validate Risk Policy
↓
Generate Risk Approval
↓
Create Validation Report
↓
RiskService
```
---
# Golden Rules
1. Barcha Risk modullar yakunlangan bo'lishi shart.
2. Har bir REJECT uchun sabab yaratilishi shart.
3. APPROVED bo'lmasa Execution Layer ishga tushmaydi.
4. RiskValidator Risk qiymatlarini o'zgartirmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
RiskValidator/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
RiskValidator GoldBot Risk Layer ichidagi barcha Risk Assessment natijalarini tekshiruvchi va Execution Layer uchun yakuniy Risk Approval yaratuvchi Canonical modul hisoblanadi.
