# RiskProfiles Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat RiskProfiles modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
RiskProfiles quyidagilar uchun javobgar.
✓ Risk Profile Selection
✓ Risk Configuration
✓ Strategy Risk Profile Generation
✓ Configuration Validation
RiskProfiles bajarmaydi.
✗ Risk Calculation
✗ Position Sizing
✗ Drawdown Management
✗ Money Management
✗ Stop Loss Calculation
✗ Take Profit Calculation
✗ Trade Execution
---
# Available Profiles
• Conservative
• Moderate
• Balanced
• Aggressive
• Custom
---
# Input Contract
• User Risk Profile Selection
---
# Output Contract
• Risk Configuration
• Strategy Risk Profile
---
# Allowed Dependencies
✓ StrategyProfiles
✓ StrategyManager
---
# Forbidden Dependencies
✗ Risk Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Execution Layer
✗ Platform Layer Logic
---
# Runtime Contract
1. Risk Profile strategiyani o'zgartirmaydi.
2. Risk Profile faqat konfiguratsiya yaratadi.
3. Risk hisob-kitobi faqat 09_Risk_Layer ichida bajariladi.
4. Configuration immutable bo'lishi kerak.
5. Validation majburiy.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Risk Profile tanlanadi.
✓ Configuration yaratiladi.
✓ Validation muvaffaqiyatli bajariladi.
✓ StrategyManager konfiguratsiyani qabul qiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
RiskProfiles Contract GoldBot Strategy Layer ichidagi barcha Risk Profile konfiguratsiyalarini boshqaruvchi rasmiy arxitektura shartnomasi hisoblanadi.
