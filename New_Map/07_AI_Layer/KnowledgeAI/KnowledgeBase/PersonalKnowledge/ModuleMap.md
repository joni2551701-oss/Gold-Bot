# Personal Knowledge Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat PersonalKnowledge ichki arxitekturasini tavsiflaydi.
---
# Module Position
KnowledgeManager
↓
PersonalKnowledge
↓
MemorySearch
---
# Module Architecture
PersonalKnowledge
│
├── User Repository
├── Preference Repository
├── Trading Repository
├── Learning Repository
├── Conversation Repository
├── Version Repository
├── Metadata Repository
└── Index Repository
---
# Internal Components
## User Repository
Foydalanuvchining asosiy bilimlari.
---
## Preference Repository
Foydalanuvchi tanlovlari va odatlari.
---
## Trading Repository
Trading uslubi va sozlamalari.
---
## Learning Repository
O'rganilgan bilimlar va progress.
---
## Conversation Repository
Muhim suhbat faktlari.
---
## Version Repository
Knowledge versiyalari.
---
## Metadata Repository
Knowledge Metadata.
---
## Index Repository
Knowledge indekslari.
---
# Allowed Dependencies
✓ KnowledgeManager
✓ MemorySearch
---
# Forbidden Dependencies
✗ SystemKnowledge
✗ ProviderRouter
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
PersonalKnowledge har bir foydalanuvchi uchun alohida Canonical Knowledge Repository hisoblanadi.
