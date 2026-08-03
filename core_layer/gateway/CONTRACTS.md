# Gateway Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Gateway modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Gateway quyidagilar uchun javobgar.
✓ Tashqi so'rovlarni yagona nuqtada qabul qiladi
✓ Service Registry orqali maqsadli xizmatni topadi
✓ Autentifikatsiya va avtorizatsiyani qo'llaydi
✓ Rate Limit va Circuit Breaker'ni boshqaradi
✓ Health va Metrics ma'lumotlarini taqdim etadi
Gateway bajarmaydi.
✗ Business Logic
✗ Trading Logic
✗ Signal Generation
✗ AI Analysis
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
Platform Layer
↓
Gateway
↓
GoldBot Core Services
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
1. Gateway faqat o'z Module Boundary ichida ishlaydi.
2. Gateway biznes mantiq bajarmaydi.
3. Gateway savdo qarori qabul qilmaydi.
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
Gateway Contract GoldBot Core Layer ichidagi Gateway jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
