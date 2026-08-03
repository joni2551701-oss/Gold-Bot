# Performance
Status: CANONICAL
---
# Purpose
Performance — GoldBot Core Layer ichidagi Canonical Performance Monitoring komponentidir.
Uning asosiy vazifasi Runtime davomida bajarilish vaqti, resurs sarfi va navbat uzunligi kabi ko'rsatkichlarni o'lchash va to'plashdir.
Performance hech qanday qaror qabul qilmaydi.
Performance hech nimani optimallashtirmaydi — u faqat o'lchaydi.
Performance Business Logic bajarmaydi.
---
# Objective
Performance quyidagi vazifalarni bajaradi.
• Metrics Collection
• Latency Measurement
• Memory Usage Tracking
• CPU Usage Tracking
• FPS Tracking (Chart Layer)
• Queue Length Tracking
• Performance Reporting
---
# Layer Position
```text
All GoldBot Layers
↓
Performance
↓
HealthMonitor
```
---
# Responsibilities
Performance
✓ Nomlangan operatsiyalarning bajarilish vaqtini o'lchaydi
✓ O'lchangan ko'rsatkichlarni to'playdi va saqlaydi
✓ Latency, Memory, CPU, FPS va Queue Length ko'rsatkichlarini kuzatadi
✓ To'plangan ko'rsatkichlarni HealthMonitor'ga taqdim etadi
---
# Not Responsible
Performance
✗ Decision Making
✗ Optimization
✗ Signal Generation
✗ AI Analysis
✗ Business Logic
✗ Database Writing (Database Layer vazifasi)
✗ Health Evaluation (HealthMonitor vazifasi)
---
# Input
Performance qabul qiladi.
• Operation Start / Stop Event
• Metric Record
• Resource Sample
---
# Output
Performance yaratadi.
• Performance Metric
• Latency Report
• Resource Usage Report
• Performance Metadata
---
# Workflow
```text
All GoldBot Layers
↓
Performance
↓
HealthMonitor
```
---
# Internal Modules (Planned — implementatsiya bosqichida to'ldiriladi)
```text
Performance
├── PerformanceTimer
├── PerformanceMetric
├── PerformanceCollector
└── ResourceSampler
```
---
# Golden Rules
1. Performance faqat o'lchaydi — hech qachon qaror qabul qilmaydi yoki optimallashtirmaydi.
2. O'lchash o'lchanayotgan kodning xatti-harakatini o'zgartirmaydi.
3. Performance o'zi Database'ga yozmaydi.
4. O'lchov ko'rsatkichlari Runtime'ni sekinlashtirmasligi shart.
5. Sog'liq holatini baholash HealthMonitor zimmasida — Performance faqat xom ko'rsatkich beradi.
6. Performance Business Logic bajarmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Performance/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
Performance GoldBot Runtime'ining bajarilish vaqti va resurs sarfini o'lchovchi Canonical Performance Monitoring moduli hisoblanadi. U faqat o'lchaydi — baholash HealthMonitor zimmasida.
