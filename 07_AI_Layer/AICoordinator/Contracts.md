# AI Coordinator Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat AICoordinator modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
AICoordinator quyidagilar uchun javobgar.
✓ AI Module Execution (yagona egasi)
✓ AI Workflow Management
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
PersonalAI / FundamentalAI / KnowledgeAI / VisionAI / VoiceAI / ExplanationAI / ConfidenceAI
↓
AICoordinator
↓
AIEngine
```
---
# Input Contract
• AI Request (AIEngine'dan)
• Personal Context
• Knowledge Context
• Fundamental Context
• Vision Context
• Voice Context
• User Request
---
# Output Contract
• Unified AI Context
• AI Package
• AI Metadata
• Confidence Report
---
# Allowed Dependencies
✓ AIEngine
✓ PersonalAI
✓ FundamentalAI
✓ KnowledgeAI
✓ VisionAI
✓ VoiceAI
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
1. AICoordinator AI modullarining yagona to'g'ridan-to'g'ri chaqiruvchisi hisoblanadi.
2. Har bir AI Request uchun faqat kerakli modullar ishga tushirilishi shart.
3. AI modullar natijalari standart formatga o'tkazilishi shart.
4. Context Aggregation bajarilishi shart.
5. ConfidenceAI AI Package yaratilishidan oldin ishlashi shart.
6. AI Package yagona formatda AIEngine'ga qaytarilishi shart (Decision Layer'ga emas — bu AIService orqali amalga oshadi).
7. AICoordinator yangi Signal yoki Decision yaratmaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ AIEngine'dan Request qabul qilinadi.
✓ Kerakli modullar ishlaydi.
✓ Natijalar yig'iladi.
✓ Unified AI Context yaratiladi.
✓ Confidence Report qo'shiladi.
✓ AI Package AIEngine'ga qaytariladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
AICoordinator Contract GoldBot AI Layer ichidagi barcha AI modullarini bevosita ishga tushiruvchi yagona egasi bo'lib, ularning natijalarini birlashtirish va AIEngine uchun yagona AI Package yaratishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
