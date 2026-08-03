# System State
Status: CANONICAL
---
# Purpose
SystemState GoldBot Core Layer ichidagi Canonical System State moduli hisoblanadi.
Uning asosiy vazifasi tizimning yuqori darajadagi ish rejimi lug'atini (operating mode) belgilashdir.
SystemState hech qanday holatni o'zi majburlamaydi — u faqat lug'at va joriy holatni taqdim etadi.
---
# Objective
SystemState quyidagi vazifalarni bajaradi.
• Operating Mode Vocabulary
• Current State Exposure
• State Transition Validation
---
# Layer Position
```text
Owner Command / Emergency
↓
SystemState
↓
Runtime Consumers
```
---
# Responsibilities
SystemState
✓ Tizim ish rejimlari ro'yxatini belgilaydi
✓ Joriy holatni taqdim etadi
✓ Holat o'tishlarining haqiqiyligini tekshiradi
---
# Not Responsible
SystemState
✗ Runtime'ni to'xtatish (Emergency vazifasi)
✗ Business Logic
✗ Trading Logic
✗ Signal Generation
---
# Implementation
Ushbu modulning Python fayllari shu papkada joylashgan (Single Source of Truth — Director Order No. 005/006):
```text
system_state.py
```
Kod Phase C davomida pre-freeze `core/` paketidan ko'chirilgan. SMR-001 bo'yicha fayllarning ichki tuzilishi o'zgartirilmagan.
---
# Golden Rules
1. SystemState biznes mantiq bajarmaydi.
2. SystemState savdo qarori qabul qilmaydi.
3. SystemState Signal, AI, Decision yoki Risk logikasi bilan shug'ullanmaydi.
4. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
system_state/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
SystemState GoldBot Core Layer ichidagi System State vazifalarini bajaruvchi Canonical modul hisoblanadi.
