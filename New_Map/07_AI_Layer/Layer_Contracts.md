# AI Layer Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat AI Layer uchun rasmiy Architecture Contract hisoblanadi.
---
# Layer Responsibility
AI Layer quyidagilar uchun javobgar.
✓ Personal AI
✓ Knowledge Retrieval
✓ Memory
✓ External AI
✓ Vision
✓ Voice
✓ Fundamental Analysis
✓ Explanation
✓ Confidence
✓ AI Package Generation
---
# Layer Does NOT
✗ Decision Making
✗ Signal Generation
✗ Risk Calculation
✗ Trade Execution
✗ Database Management
---
# Input Contract
AI Layer qabul qiladi.
• Context Layer Output
• Signal Layer Output
• User Request
• Voice Input
• Image Input
---
# Output Contract
AI Layer yaratadi.
• Unified AI Context
• Explanation
• Confidence Score
• AI Package
---
# Layer Pipeline
```text
AIService
↓
AIEngine
↓
AICoordinator
↓
AI Modules
↓
ExplanationAI
↓
ConfidenceAI
↓
AI Package
```
---
# Layer Rules
1. AI Layer hech qachon yakuniy qaror qabul qilmaydi.
2. AI Layer Signal yaratmaydi.
3. AI Layer Trade ochmaydi.
4. AI Package faqat Decision Layer uchun yaratiladi.
5. Internal Knowledge har doim External AI'dan ustun turadi.
6. External AI faqat kerak bo'lganda ProviderRouter orqali ishlatiladi.
7. ConfidenceAI har doim AI Package yakunida ishlaydi.
8. AI Layer modullari AICoordinator orqali boshqariladi.
9. AI Layer tashqi tizimlar bilan faqat AIService orqali aloqa qiladi.
10. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ AIService barcha so'rovlarni qabul qiladi.
✓ AIEngine Pipeline'ni ishga tushiradi.
✓ AICoordinator modullarni boshqaradi.
✓ Kerakli AI modullar ishlaydi.
✓ AI Package yaratiladi.
✓ Confidence Report yaratiladi.
✓ Decision Layer'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
AI Layer Contract GoldBot arxitekturasidagi barcha sun'iy intellekt modullarining ishlash chegaralari, mas'uliyatlari, ma'lumot oqimi va tashqi qatlamlar bilan integratsiya qoidalarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
