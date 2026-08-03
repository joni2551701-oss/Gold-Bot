# Provider Interface
Status: CANONICAL
---
# Purpose
ProviderInterface GoldBot Data Layer ichidagi Canonical Provider Contract moduli hisoblanadi.
Uning asosiy vazifasi barcha Market Data Provider'lar bajarishi shart bo'lgan yagona interfeys va standart xatti-harakatlarni belgilashdir.
ProviderInterface Provider yaratmaydi.
ProviderInterface API bilan bog'lanmaydi.
ProviderInterface faqat Contract va Standard Behavior'ni belgilaydi.
---
# Objective
ProviderInterface quyidagi vazifalarni bajaradi.
• Provider Contract
• Standard API Definition
• Common Data Model
• Standard Response Format
• Error Contract
• Lifecycle Contract
---
# Layer Position
```text
ProviderFactory
↓
ProviderInterface
↓
TwelveData
Bitget
Future Providers
```
---
# Responsibilities
ProviderInterface
✓ Common Interface belgilaydi
✓ Standard Method'larni belgilaydi
✓ Standard Response Format belgilaydi
✓ Error Contract belgilaydi
✓ Provider Lifecycle Contract belgilaydi
---
# Not Responsible
ProviderInterface
✗ Provider Creation
✗ API Communication
✗ Market Data Retrieval
✗ Data Validation
✗ Trading Logic
---
# Input
ProviderInterface qabul qiladi.
• Provider Implementation
• Interface Contract
---
# Output
ProviderInterface yaratadi.
• Standard Provider Contract
• Standard Response Structure
• Provider Metadata Contract
---
# Workflow
```text
Define Interface
↓
Implement Provider
↓
Validate Contract
↓
Ready for Factory
```
---
# Golden Rules
1. Har bir Provider ProviderInterface'ni implement qilishi shart.
2. Interface barcha Provider'lar uchun yagona bo'lishi shart.
3. Interface Provider turiga bog'liq bo'lmasligi shart.
4. Interface faqat Contract belgilaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
ProviderInterface/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
ProviderInterface GoldBot Data Layer ichidagi barcha Market Data Provider'lar uchun yagona Contract va standart xatti-harakatlarni belgilovchi Canonical modul hisoblanadi.
