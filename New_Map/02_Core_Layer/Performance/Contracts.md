# Performance Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Performance modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Performance quyidagilar uchun javobgar.
✓ Nomlangan operatsiyalarning bajarilish vaqtini o'lchaydi
✓ O'lchangan ko'rsatkichlarni to'playdi va saqlaydi
✓ Latency, Memory, CPU, FPS va Queue Length ko'rsatkichlarini kuzatadi
✓ To'plangan ko'rsatkichlarni HealthMonitor'ga taqdim etadi
Performance bajarmaydi.
✗ Decision Making
✗ Optimization
✗ Signal Generation
✗ AI Analysis
✗ Business Logic
✗ Database Writing (Database Layer vazifasi)
✗ Health Evaluation (HealthMonitor vazifasi)
---
# Module Boundary
```text
All GoldBot Layers
↓
Performance
↓
HealthMonitor
```
---
# Input Contract
• Operation Start / Stop Event
• Metric Record
• Resource Sample
---
# Output Contract
• Performance Metric
• Latency Report
• Resource Usage Report
• Performance Metadata
---
# Allowed Dependencies
✓ CoreEngine
✓ HealthMonitor
✓ Configuration
---
# Forbidden Dependencies
✗ Strategy Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
✗ Platform Layer
---
# Runtime Contract
1. Performance faqat o'lchaydi — hech qachon qaror qabul qilmaydi yoki optimallashtirmaydi.
2. O'lchash o'lchanayotgan kodning xatti-harakatini o'zgartirmaydi.
3. Performance o'zi Database'ga yozmaydi.
4. O'lchov ko'rsatkichlari Runtime'ni sekinlashtirmasligi shart.
5. Sog'liq holatini baholash HealthMonitor zimmasida — Performance faqat xom ko'rsatkich beradi.
6. Performance Business Logic bajarmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Operatsiya vaqti o'lchanadi.
✓ Ko'rsatkichlar to'planadi.
✓ Resurs sarfi kuzatiladi.
✓ HealthMonitor'ga taqdim etiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Performance Contract Performance GoldBot Runtime'ining bajarilish vaqti va resurs sarfini o'lchovchi Canonical Performance Monitoring moduli hisoblanadi. U faqat o'lchaydi — baholash HealthMonitor zimmasida.
