# Sessions Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Sessions modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Sessions quyidagilar uchun javobgar.
✓ Trading Session Selection
✓ Session Configuration
✓ Session Validation
✓ Session Profile Generation
✓ Session Filter Configuration
Sessions bajarmaydi.
✗ Strategy Logic
✗ Indicator Calculation
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Available Sessions
• Asia
• London
• New York
• London + New York Overlap
• Custom Session
---
# Input Contract
• Session Selection
---
# Output Contract
• Session Configuration
• Session Profile
---
# Allowed Dependencies
✓ StrategyProfiles
✓ StrategyEngine
---
# Forbidden Dependencies
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer Logic
---
# Runtime Contract
1. Har qanday Strategy istalgan Session bilan ishlashi mumkin.
2. Session Strategy Logic'ni o'zgartirmaydi.
3. Session faqat vaqt filtri hisoblanadi.
4. Session Configuration immutable bo'lishi kerak.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Session tanlanadi.
✓ Session Configuration yaratiladi.
✓ Session Validation muvaffaqiyatli yakunlanadi.
✓ StrategyEngine Session Configuration'ni qabul qiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Sessions Contract GoldBot ichidagi barcha Trading Session konfiguratsiyalarini boshqaruvchi rasmiy arxitektura shartnomasi hisoblanadi.
