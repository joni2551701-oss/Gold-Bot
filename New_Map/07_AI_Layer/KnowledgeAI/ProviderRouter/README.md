# Provider Router
Status: CANONICAL
---
# Purpose
ProviderRouter GoldBot KnowledgeAI ichidagi Canonical AI Provider Orchestration moduli hisoblanadi.
Uning asosiy vazifasi AI so'rovlarini eng mos AI Provider'ga yuborish, javoblarni qabul qilish va yagona standart formatga keltirishdir.
ProviderRouter AI qaror qabul qilmaydi.
ProviderRouter Knowledge saqlamaydi.
ProviderRouter Learning bajarmaydi.
ProviderRouter faqat AI Provider Routing bilan shug'ullanadi.
---
# Objective
ProviderRouter quyidagi vazifalarni bajaradi.
• Provider Selection
• Provider Routing
• Provider Failover
• Response Normalization
• Cost Optimization
• Latency Optimization
---
# Layer Position
```text
KnowledgeAI
↓
ProviderRouter
↓
AI Providers
↓
ValidationEngine
```
---
# Responsibilities
ProviderRouter
✓ Eng mos Provider tanlaydi
✓ AI Request yuboradi
✓ Provider almashtiradi
✓ Timeout boshqaradi
✓ Response formatini standartlashtiradi
✓ Provider Health tekshiradi
---
# Not Responsible
ProviderRouter
✗ Knowledge Storage
✗ Memory Storage
✗ Learning
✗ Validation
✗ AI Decision
✗ Signal Generation
---
# Input
ProviderRouter qabul qiladi.
• AI Request
• AI Context
• Provider Policy
• Routing Metadata
---
# Output
ProviderRouter yaratadi.
• Provider Response
• Normalized Response
• Provider Metadata
• Routing Report
---
# Workflow
```text
Receive Request
↓
Select Provider
↓
Send Request
↓
Receive Response
↓
Normalize Response
↓
ValidationEngine
```
---
# Golden Rules
1. Internal Knowledge har doim ustuvor.
2. External Provider faqat kerak bo'lganda chaqiriladi.
3. Provider Failure avtomatik boshqariladi.
4. Response standart formatga o'tkaziladi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
ProviderRouter/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
ProviderRouter GoldBot AI ichidagi barcha External AI Provider'larni boshqaruvchi Canonical AI Gateway hisoblanadi.
