# System State Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat SystemState modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
SystemState quyidagilar uchun javobgar.
✓ Tizim ish rejimlari ro'yxatini belgilaydi
✓ Joriy holatni taqdim etadi
✓ Holat o'tishlarining haqiqiyligini tekshiradi
SystemState bajarmaydi.
✗ Runtime'ni to'xtatish (Emergency vazifasi)
✗ Business Logic
✗ Trading Logic
✗ Signal Generation
---
# Module Boundary
```text
Owner Command / Emergency
↓
SystemState
↓
Runtime Consumers
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
1. SystemState faqat o'z Module Boundary ichida ishlaydi.
2. SystemState biznes mantiq bajarmaydi.
3. SystemState savdo qarori qabul qilmaydi.
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
SystemState Contract GoldBot Core Layer ichidagi System State jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
