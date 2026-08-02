# RAG
Status: CANONICAL
---
# Purpose
RAG (Retrieval-Augmented Generation) GoldBot KnowledgeAI ichidagi Canonical Knowledge Retrieval moduli hisoblanadi.
Uning asosiy vazifasi AI javob berishdan oldin ichki hujjatlar, KnowledgeBase va boshqa Repository'lardan kerakli ma'lumotlarni topish va AI Context'ga qo'shishdir.
RAG yangi Knowledge yaratmaydi.
RAG Learning bajarmaydi.
RAG Validation bajarmaydi.
RAG faqat Retrieval bilan shug'ullanadi.
---
# Objective
RAG quyidagi vazifalarni bajaradi.
• Document Retrieval
• Semantic Search
• Context Retrieval
• Multi-Source Retrieval
• Knowledge Ranking
• Context Generation
---
# Layer Position
```text
User Request
↓
RAG
↓
KnowledgeBase
↓
Knowledge Context
↓
ProviderRouter
```
---
# Responsibilities
RAG
✓ Documentation qidiradi
✓ KnowledgeBase qidiradi
✓ Semantic Search bajaradi
✓ Context yaratadi
✓ Retrieval Ranking bajaradi
✓ Relevant Document topadi
---
# Not Responsible
RAG
✗ Knowledge Storage
✗ Memory Storage
✗ Learning
✗ Validation
✗ AI Generation
✗ Decision Making
---
# Input
RAG qabul qiladi.
• User Query
• AI Context
• Retrieval Filters
• Search Metadata
---
# Output
RAG yaratadi.
• Retrieved Context
• Relevant Documents
• Retrieval Score
• Context Metadata
---
# Workflow
```text
User Query
↓
Semantic Retrieval
↓
Retrieve Documents
↓
Rank Results
↓
Build Context
↓
ProviderRouter
```
---
# Golden Rules
1. Retrieval Semantic Search asosida ishlaydi.
2. Eng relevant hujjatlar qaytariladi.
3. RAG faqat Read-only ishlaydi.
4. Knowledge o'zgartirilmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
RAG/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
RAG GoldBot AI ichidagi Canonical Retrieval Engine bo'lib, AI javob berishdan oldin kerakli hujjat va Knowledge'larni topib AI Context yaratadi.
