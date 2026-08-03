# Gateway
Status: CANONICAL
---
# Purpose
Gateway GoldBot Core Layer ichidagi Canonical Service Gateway moduli hisoblanadi.
Uning asosiy vazifasi Service Registry, Router, Authentication, Authorization, Rate Limiting, Health, Metrics va Versioning'ni yagona kirish nuqtasi ortida birlashtirishdir.
Gateway biznes mantiq bajarmaydi va savdo qarori qabul qilmaydi.
---
# Objective
Gateway quyidagi vazifalarni bajaradi.
• Service Registration va Discovery
• Request Routing
• Authentication va Authorization
• Rate Limiting
• Circuit Breaking
• Health va Metrics Exposure
• API Versioning
---
# Layer Position
```text
Platform Layer
↓
Gateway
↓
GoldBot Core Services
```
---
# Responsibilities
Gateway
✓ Tashqi so'rovlarni yagona nuqtada qabul qiladi
✓ Service Registry orqali maqsadli xizmatni topadi
✓ Autentifikatsiya va avtorizatsiyani qo'llaydi
✓ Rate Limit va Circuit Breaker'ni boshqaradi
✓ Health va Metrics ma'lumotlarini taqdim etadi
---
# Not Responsible
Gateway
✗ Business Logic
✗ Trading Logic
✗ Signal Generation
✗ AI Analysis
✗ Risk Calculation
✗ Trade Execution
---
# Implementation
Ushbu modulning Python fayllari shu papkada joylashgan (Single Source of Truth — Director Order No. 005/006):
```text
authentication.py · authorization.py · dependency_graph.py · gateway.py · gateway_context.py · gateway_events.py · gateway_request.py · health_service.py · metrics_service.py · rate_limiter.py · router.py · service.py · service_breaker.py · service_manifest.py · service_registry.py · service_state.py · version_service.py
```
Kod Phase C davomida pre-freeze `core/` paketidan ko'chirilgan. SMR-001 bo'yicha fayllarning ichki tuzilishi o'zgartirilmagan.
---
# Golden Rules
1. Gateway biznes mantiq bajarmaydi.
2. Gateway savdo qarori qabul qilmaydi.
3. Gateway Signal, AI, Decision yoki Risk logikasi bilan shug'ullanmaydi.
4. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
gateway/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
Gateway GoldBot Core Layer ichidagi Gateway vazifalarini bajaruvchi Canonical modul hisoblanadi.
