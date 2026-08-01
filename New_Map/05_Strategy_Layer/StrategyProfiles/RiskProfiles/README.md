# Risk Profiles
Status: CANONICAL
---
# Purpose
RiskProfiles GoldBot Strategy Layer ichidagi barcha Risk Profile konfiguratsiyalarini boshqaruvchi Canonical modul hisoblanadi.
Risk Profile strategiyani o'zgartirmaydi.
Risk Profile strategiyaning qanday risk bilan ishlashini belgilaydi.
---
# Objective
RiskProfiles quyidagi vazifalarni bajaradi.
• Risk Profile Selection
• Risk Configuration
• Risk Validation
• Strategy Risk Profile Generation
---
# Available Risk Profiles
• Conservative
• Moderate
• Balanced
• Aggressive
• Custom
---
# Responsibilities
RiskProfiles
✓ Risk Profile tanlaydi
✓ Risk Configuration yaratadi
✓ Strategy Configuration'ni to'ldiradi
✓ Risk Validation bajaradi
✓ Strategy Profile yaratadi
---
# Not Responsible
RiskProfiles
✗ Risk Calculation
✗ Position Sizing
✗ Stop Loss Calculation
✗ Take Profit Calculation
✗ Money Management
✗ Signal Generation
✗ Trade Execution
---
# Input
• User Risk Selection
---
# Output
• Risk Configuration
• Strategy Risk Profile
---
# Workflow
```text
User Settings
↓
Select Risk Profile
↓
Validate Configuration
↓
Build Risk Profile
↓
StrategyEngine
```
---
# Golden Rules
1. Risk Profile strategiyani o'zgartirmaydi.
2. Risk Layer o'rnini bosmaydi.
3. Risk Profile faqat konfiguratsiya hisoblanadi.
4. Configuration immutable hisoblanadi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
RiskProfiles/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
RiskProfiles GoldBot Strategy Layer ichidagi barcha Risk Profile konfiguratsiyalarini boshqaruvchi Canonical modul hisoblanadi.
