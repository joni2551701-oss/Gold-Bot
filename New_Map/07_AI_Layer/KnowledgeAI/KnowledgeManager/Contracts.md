# Knowledge Manager Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat KnowledgeManager modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
KnowledgeManager quyidagilar uchun javobgar.
✓ Knowledge Registration
✓ Knowledge Classification
✓ Knowledge Versioning
✓ Knowledge Metadata
✓ Knowledge Lifecycle
KnowledgeManager bajarmaydi.
✗ Memory Storage
✗ Memory Search
✗ Learning
✗ Validation
✗ RAG
✗ External AI
✗ AI Analysis
---
# Module Boundary
```text
KnowledgeAI
↓
KnowledgeManager
↓
KnowledgeBase
```
---
# Input Contract
• Validated Knowledge
• Knowledge Metadata
• Knowledge Update
---
# Output Contract
• Registered Knowledge
• Knowledge Version
• Knowledge Metadata
• Knowledge Reference
---
# Allowed Dependencies
✓ KnowledgeBase
---
# Forbidden Dependencies
✗ MemoryManager
✗ MemorySearch
✗ ProviderRouter
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. Faqat Validation'dan o'tgan Knowledge qabul qilinadi.
2. Har bir Knowledge noyob ID'ga ega bo'lishi shart.
3. Har bir Knowledge Version saqlanishi shart.
4. Metadata majburiy.
5. Duplicate Knowledge yaratilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Knowledge ro'yxatdan o'tadi.
✓ Classification bajariladi.
✓ Version yaratiladi.
✓ Metadata yaratiladi.
✓ KnowledgeBase'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
KnowledgeManager Contract GoldBot AI Knowledge Lifecycle'ni boshqaruvchi rasmiy Canonical Architecture Contract hisoblanadi.
