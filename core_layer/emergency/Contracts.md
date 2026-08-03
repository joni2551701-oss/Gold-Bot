# Emergency Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Emergency modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Emergency quyidagilar uchun javobgar.
✓ Emergency holatini saqlaydi va o'zgartiradi
✓ Circuit Breaker'ni boshqaradi
✓ Maintenance rejimini yoqadi va o'chiradi
✓ Har bir holat o'tishini yozib boradi
Emergency bajarmaydi.
✗ Signal Generation
✗ Trading Decision
✗ Risk Calculation
✗ Trade Execution
✗ Business Logic
---
# Module Boundary
```text
Owner Command
↓
Emergency
↓
Pipeline / Runtime
```
---
# Allowed Dependencies
✓ Configuration
✓ Logger
✓ Errors
---
# Forbidden Dependencies
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
✗ Platform Layer
---
# Runtime Contract
1. Emergency faqat o'z Module Boundary ichida ishlaydi.
2. Emergency biznes mantiq bajarmaydi.
3. Emergency savdo qarori qabul qilmaydi.
4. Maxfiy qiymatlar hech qachon log'ga yozilmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Mas'uliyat bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Emergency Contract GoldBot Core Layer ichidagi Emergency jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
