# Errors Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Errors modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Errors quyidagilar uchun javobgar.
✓ Yagona `GoldBotError` bazasini taqdim etadi
✓ Xato kodlarini belgilaydi
✓ Modulga xos exception'larni e'lon qiladi
Errors bajarmaydi.
✗ Business Logic
✗ Error Handling Policy (chaqiruvchi zimmasida)
✗ Logging (Logger vazifasi)
✗ Trading Logic
---
# Module Boundary
```text
Barcha Layer'lar
↓
Errors
↓
Logger / Caller
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
1. Errors faqat o'z Module Boundary ichida ishlaydi.
2. Errors biznes mantiq bajarmaydi.
3. Errors savdo qarori qabul qilmaydi.
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
Errors Contract GoldBot Core Layer ichidagi Errors jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
