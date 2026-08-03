# Logger
Status: CANONICAL
---
# Purpose
Logger GoldBot Core Layer ichidagi Canonical Logging moduli hisoblanadi.
Uning asosiy vazifasi butun tizim uchun yagona, izchil logger konfiguratsiyasini taqdim etishdir.
Logger biznes mantiq bajarmaydi va maxfiy qiymatlarni yozmaydi.
---
# Objective
Logger quyidagi vazifalarni bajaradi.
• Logger Setup
• Uniform Log Format
• Log Level Management
---
# Layer Position
```text
Barcha Layer'lar
↓
Logger
↓
Log Output
```
---
# Responsibilities
Logger
✓ Nomlangan logger yaratadi va sozlaydi
✓ Yagona format va darajani ta'minlaydi
---
# Not Responsible
Logger
✗ Business Logic
✗ Error Taxonomy (Errors vazifasi)
✗ Audit Trail (Database Layer/AuditLog vazifasi)
✗ Maxfiy qiymatlarni yozish
---
# Implementation
Ushbu modulning Python fayllari shu papkada joylashgan (Single Source of Truth — Director Order No. 005/006):
```text
logger.py
```
Kod Phase C davomida pre-freeze `core/` paketidan ko'chirilgan. SMR-001 bo'yicha fayllarning ichki tuzilishi o'zgartirilmagan.
---
# Golden Rules
1. Logger biznes mantiq bajarmaydi.
2. Logger savdo qarori qabul qilmaydi.
3. Logger Signal, AI, Decision yoki Risk logikasi bilan shug'ullanmaydi.
4. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
logger/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
Logger GoldBot Core Layer ichidagi Logger vazifalarini bajaruvchi Canonical modul hisoblanadi.
