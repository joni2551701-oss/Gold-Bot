# Risk Layer Data Flow
Status: CANONICAL
---
# Purpose
Ushbu hujjat GoldBot Risk Layer ichidagi ma'lumotlar oqimini (Data Flow) tavsiflaydi.
Risk Layer Decision Layer tomonidan APPROVED qilingan Trade'ni kapital xavfsizligi nuqtai nazaridan baholaydi va faqat Risk Validation'dan o'tgan Trade'larni Execution Layer'ga uzatadi.
---
# Layer Data Flow
```text
Decision Layer
        │
        ▼
RiskService (Entry)
        │
        ▼
RiskEngine
        │
        ▼
PositionSizing
        │
        ▼
MoneyManagement
        │
        ▼
DrawdownManager
        │
        ▼
ExposureManager
        │
        ▼
PortfolioManager
        │
        ▼
RiskValidator
        │
        ▼
Risk Approval
        │
        ▼
RiskService (Exit)
        │
        ▼
Execution Layer
```
---
# Input Sources
• Decision Package
• Account Information
• Symbol Information
• Open Positions
• Portfolio Information
• Risk Policy
---
# Output
• Risk Approval
• Position Size
• Lot Size
• Risk Report
• Portfolio Report
• Risk Metadata
---
# Data Flow Rules
1. Risk Layer faqat APPROVED Decision qabul qiladi.
2. Har bir modul oldingi modul natijasidan foydalanadi.
3. Risk Report barcha modullar yakunlangandan keyin yaratiladi.
4. Risk Approval faqat RiskValidator tomonidan yaratiladi.
5. Risk Approval RiskService orqali Execution Layer'ga uzatiladi — RiskValidator Layer tashqarisiga chiqmaydi.
6. Execution Layer faqat APPROVED Risk natijasini qabul qiladi.
---
# Summary
Risk Layer GoldBot kapitalini himoya qiluvchi Canonical Data Processing Pipeline hisoblanadi.
