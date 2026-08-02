# AI Coordinator Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat AICoordinator modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
AICoordinator quyidagilar uchun javobgar.
✓ AI Workflow Management
✓ Module Orchestration
✓ Context Aggregation
✓ Result Collection
✓ AI Package Generation
✓ Pipeline Monitoring
AICoordinator bajarmaydi.
✗ Market Analysis
✗ Learning
✗ Knowledge Storage
✗ Decision Making
✗ Trade Execution
✗ Risk Calculation
---
# Module Boundary
```text
AIEngine
↓
AICoordinator
↓
Decision Layer
```
---
# Input Contract
• Personal Context
• Knowledge Context
• Fundamental Context
• Vision Context
• User Request
---
# Output Contract
• Unified AI Context
• AI Package
• AI Metadata
• Confidence Report
---
# Allowed Dependencies
✓ PersonalAI
✓ FundamentalAI
✓ KnowledgeAI
✓ VisionAI
✓ ExplanationAI
✓ ConfidenceAI
---
# Forbidden Dependencies
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
---
# Runtime Contract
1. Har bir AI Request uchun faqat kerakli modullar ishga tushirilishi shart.
2. AI modullar natijalari standart formatga o'tkazilishi shart.
3. Context Aggregation bajarilishi shart.
4. ConfidenceAI AI Package yaratilishidan oldin ishlashi shart.
5. AI Package yagona formatda Decision Layer'ga uzatilishi shart.
6. AICoordinator yangi Signal yoki Decision yaratmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ AI Workflow ishga tushadi.
✓ Kerakli modullar ishlaydi.
✓ Natijalar yig'iladi.
✓ Unified AI Context yaratiladi.
✓ Confidence Report qo'shiladi.
✓ AI Package Decision Layer'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
AICoordinator Contract GoldBot AI Layer ichidagi barcha AI modullarini orkestratsiya qilish, ularning natijalarini birlashtirish va Decision Layer uchun yagona AI Package yaratishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
