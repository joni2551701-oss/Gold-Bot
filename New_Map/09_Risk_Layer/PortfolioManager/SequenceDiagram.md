# Portfolio Manager Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat PortfolioManager Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
ExposureManager
↓
PortfolioManager
↓
Analyze Portfolio
↓
Calculate Portfolio Risk
↓
Analyze Correlation
↓
Analyze Diversification
↓
Generate Portfolio Report
↓
RiskValidator
```
---
# Runtime Rules
1. Exposure Report mavjud bo'lishi shart.
2. Portfolio Risk hisoblanishi shart.
3. Correlation tekshirilishi shart.
4. Portfolio Report yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Analyzing
↓
Calculating
↓
Reporting
↓
Completed
```
---
# Summary
ExposureManager
↓
PortfolioManager
↓
Portfolio Report
↓
RiskValidator
