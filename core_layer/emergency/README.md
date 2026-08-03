# Emergency
Status: CANONICAL
---
# Purpose
Emergency GoldBot Core Layer ichidagi Canonical Emergency Safety moduli hisoblanadi.
Uning asosiy vazifasi tizimni favqulodda holatlarda to'xtatish, pauza qilish yoki texnik xizmat rejimiga o'tkazishdir.
Emergency savdo qarori qabul qilmaydi — u faqat Runtime'ni to'xtatish/davom ettirish huquqiga ega.
---
# Objective
Emergency quyidagi vazifalarni bajaradi.
• Emergency State Management (Pause / Kill / Maintenance / Resume)
• Circuit Breaking
• Maintenance Mode
• Emergency Transition History
---
# Layer Position
```text
Owner Command
↓
Emergency
↓
Pipeline / Runtime
```
---
# Responsibilities
Emergency
✓ Emergency holatini saqlaydi va o'zgartiradi
✓ Circuit Breaker'ni boshqaradi
✓ Maintenance rejimini yoqadi va o'chiradi
✓ Har bir holat o'tishini yozib boradi
---
# Not Responsible
Emergency
✗ Signal Generation
✗ Trading Decision
✗ Risk Calculation
✗ Trade Execution
✗ Business Logic
---
# Implementation
Ushbu modulning Python fayllari shu papkada joylashgan (Single Source of Truth — Director Order No. 005/006):
```text
circuit_breaker.py · emergency_manager.py · emergency_state.py · maintenance.py
```
Kod Phase C davomida pre-freeze `core/` paketidan ko'chirilgan. SMR-001 bo'yicha fayllarning ichki tuzilishi o'zgartirilmagan.
---
# Golden Rules
1. Emergency biznes mantiq bajarmaydi.
2. Emergency savdo qarori qabul qilmaydi.
3. Emergency Signal, AI, Decision yoki Risk logikasi bilan shug'ullanmaydi.
4. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
emergency/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
Emergency GoldBot Core Layer ichidagi Emergency vazifalarini bajaruvchi Canonical modul hisoblanadi.
