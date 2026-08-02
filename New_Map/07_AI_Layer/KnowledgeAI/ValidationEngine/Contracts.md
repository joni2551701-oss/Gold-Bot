# Validation Engine Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat ValidationEngine modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
ValidationEngine quyidagilar uchun javobgar.
✓ Knowledge Validation
✓ Source Validation
✓ Fact Verification
✓ Duplicate Detection
✓ Confidence Evaluation
✓ Knowledge Approval
ValidationEngine bajarmaydi.
✗ Learning
✗ Memory Storage
✗ Knowledge Storage
✗ AI Analysis
✗ Decision Making
✗ External AI Generation
---
# Module Boundary
```text
ProviderRouter
↓
ValidationEngine
↓
LearningEngine
```
---
# Input Contract
• New Knowledge
• External AI Response
• RAG Result
• Knowledge Metadata
---
# Output Contract
• Validation Result
• Confidence Score
• Validation Report
• Approved Knowledge
---
# Allowed Dependencies
✓ ProviderRouter
✓ LearningEngine
✓ KnowledgeManager
---
# Forbidden Dependencies
✗ MemoryManager
✗ MemorySearch
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. Har bir yangi Knowledge tekshirilishi shart.
2. Source Validation majburiy.
3. Fact Verification bajarilishi shart.
4. Duplicate Knowledge rad etilishi shart.
5. Confidence Score hisoblanishi shart.
6. Faqat Approved Knowledge LearningEngine'ga uzatiladi.
7. ValidationEngine hech qachon yangi Knowledge yaratmaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Source tekshiriladi.
✓ Faktlar tekshiriladi.
✓ Duplicate aniqlanadi.
✓ Confidence Score yaratiladi.
✓ Validation Report yaratiladi.
✓ Approved Knowledge LearningEngine'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
ValidationEngine Contract GoldBot AI ichidagi barcha yangi bilimlarni tekshirish, tasdiqlash va LearningEngine'ga faqat ishonchli ma'lumotlarni uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
