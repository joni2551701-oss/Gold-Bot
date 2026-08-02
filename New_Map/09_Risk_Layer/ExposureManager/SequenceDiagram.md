# Exposure Manager Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ExposureManager Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
DrawdownManager
↓
ExposureManager
↓
Analyze Open Positions
↓
Analyze Pending Orders
↓
Calculate Exposure
↓
Validate Exposure Policy
↓
Generate Exposure Report
↓
PortfolioManager
```
---
# Runtime Rules
1. Open Positionlar yuklanishi shart.
2. Pending Orderlar tekshirilishi shart.
3. Exposure hisoblanishi shart.
4. Exposure Report yaratilishi shart.
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
Validating
↓
Completed
```
---
# Summary
DrawdownManager
↓
ExposureManager
↓
Exposure Report
↓
PortfolioManager
