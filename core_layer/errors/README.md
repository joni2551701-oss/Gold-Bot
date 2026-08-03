# Errors
Status: CANONICAL
---
# Purpose
Errors GoldBot Core Layer ichidagi Canonical Error Taxonomy moduli hisoblanadi.
Uning asosiy vazifasi butun tizim uchun yagona xato ierarxiyasi va xato kodlarini belgilashdir.
Errors biznes mantiq bajarmaydi.
---
# Objective
Errors quyidagi vazifalarni bajaradi.
• Base Error Hierarchy
• Error Codes
• Module-specific Exceptions
• Structured Error Payload
---
# Layer Position
```text
Barcha Layer'lar
↓
Errors
↓
Logger / Caller
```
---
# Responsibilities
Errors
✓ Yagona `GoldBotError` bazasini taqdim etadi
✓ Xato kodlarini belgilaydi
✓ Modulga xos exception'larni e'lon qiladi
---
# Not Responsible
Errors
✗ Business Logic
✗ Error Handling Policy (chaqiruvchi zimmasida)
✗ Logging (Logger vazifasi)
✗ Trading Logic
---
# Implementation
Ushbu modulning Python fayllari shu papkada joylashgan (Single Source of Truth — Director Order No. 005/006):
```text
base.py · codes.py · exceptions.py
```
Kod Phase C davomida pre-freeze `core/` paketidan ko'chirilgan. SMR-001 bo'yicha fayllarning ichki tuzilishi o'zgartirilmagan.
---
# Golden Rules
1. Errors biznes mantiq bajarmaydi.
2. Errors savdo qarori qabul qilmaydi.
3. Errors Signal, AI, Decision yoki Risk logikasi bilan shug'ullanmaydi.
4. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
errors/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
Errors GoldBot Core Layer ichidagi Errors vazifalarini bajaruvchi Canonical modul hisoblanadi.
