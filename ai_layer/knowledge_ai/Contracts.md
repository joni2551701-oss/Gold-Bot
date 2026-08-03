# Knowledge AI Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat KnowledgeAI modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
KnowledgeAI quyidagilar uchun javobgar.
✓ Knowledge Management
✓ Shared Memory
✓ Memory Search
✓ Knowledge Retrieval
✓ AI Learning
✓ Knowledge Validation
✓ RAG Retrieval
✓ External AI Routing
KnowledgeAI bajarmaydi.
✗ Technical Analysis
✗ Strategy
✗ Signal Generation
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
PersonalAI
↓
KnowledgeAI
↓
AICoordinator
```
---
# Input Contract
• User Request
• AI Context
• Memory Context
• Knowledge Query
• RAG Query
---
# Output Contract
• Knowledge Context
• Memory Result
• Validated Knowledge
• Learning Result
• Provider Response
---
# Allowed Dependencies
✓ AIEngine
✓ PersonalAI
✓ AICoordinator
---
# Forbidden Dependencies
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Runtime Contract
1. KnowledgeManager va KnowledgeBase birinchi tayyor bo'lishi shart — bo'lmasa qolgan modullar ishlay olmaydi.
2. Memory KnowledgeBase'dan keyin tekshirilishi shart.
3. Personal Knowledge System Knowledge'dan ustun.
4. RAG ichki hujjatlar uchun ishlatiladi.
5. External Provider faqat zarurat bo'lsa chaqiriladi.
6. Validation majburiy.
7. Learning oxirida feedback sifatida ishlaydi (Validation muvaffaqiyatli o'tgandan keyin).
8. Shared Memory barcha Persona uchun umumiy.
9. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Memory Search ishlaydi.
✓ Knowledge Retrieval ishlaydi.
✓ RAG ishlaydi.
✓ Provider Routing ishlaydi.
✓ Validation ishlaydi.
✓ Learning ishlaydi.
✓ Knowledge Context yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
KnowledgeAI Contract GoldBot AI Layer ichidagi barcha Knowledge, Memory, Learning, RAG va External AI Provider jarayonlarini boshqaruvchi rasmiy Canonical Architecture Contract hisoblanadi.
