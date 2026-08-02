# Provider Router Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat ProviderRouter modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
ProviderRouter quyidagilar uchun javobgar.
✓ Provider Selection
✓ AI Request Routing
✓ Provider Failover
✓ Health Monitoring
✓ Response Normalization
✓ Provider Registry
ProviderRouter bajarmaydi.
✗ Knowledge Storage
✗ Memory Storage
✗ Learning
✗ Validation
✗ AI Decision
✗ Signal Generation
---
# Module Boundary
```text
KnowledgeAI
↓
ProviderRouter
↓
External AI
↓
ValidationEngine
```
---
# Input Contract
• AI Request
• AI Context
• Provider Policy
• Routing Metadata
---
# Output Contract
• Provider Response
• Normalized Response
• Routing Report
• Provider Metadata
---
# Allowed Dependencies
✓ ValidationEngine
---
# Forbidden Dependencies
✗ MemoryManager
✗ LearningEngine
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. Internal Knowledge har doim birinchi ishlatilishi shart.
2. External AI faqat kerak bo'lganda chaqiriladi.
3. Provider Selection avtomatik bajariladi.
4. Provider Failure bo'lsa Failover ishlashi shart.
5. Response yagona standart formatga o'tkazilishi shart.
6. Har bir so'rov va javob log qilinishi kerak.
7. ProviderRouter yangi Knowledge yaratmaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ To'g'ri Provider tanlanadi.
✓ Request muvaffaqiyatli yuboriladi.
✓ Response olinadi.
✓ Response Normalize qilinadi.
✓ ValidationEngine'ga uzatiladi.
✓ Failover ishlaydi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
ProviderRouter Contract GoldBot AI ichidagi barcha tashqi AI Provider'larni boshqarish, ularni marshrutlash, xatoliklarda avtomatik almashtirish va javoblarni yagona formatga keltirishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
