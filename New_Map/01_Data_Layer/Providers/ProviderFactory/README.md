# Provider Factory
Status: CANONICAL
---
# Purpose
ProviderFactory GoldBot Data Layer ichidagi Canonical Provider Creation va Provider Selection moduli hisoblanadi.
Uning asosiy vazifasi konfiguratsiya va so'rov talablariga mos ravishda kerakli Market Data Provider'ni yaratish va taqdim etishdir.
ProviderFactory Market Data yuklamaydi.
ProviderFactory API bilan bevosita ishlamaydi.
ProviderFactory faqat Provider Instance yaratadi va boshqaradi.
---
# Objective
ProviderFactory quyidagi vazifalarni bajaradi.
• Provider Selection
• Provider Creation
• Provider Initialization
• Provider Registration
• Provider Configuration
• Provider Lifecycle Integration
---
# Layer Position
```text
Data Request
↓
ProviderFactory
↓
ProviderInterface
↓
TwelveData
Bitget
```
---
# Responsibilities
ProviderFactory
✓ Provider tanlaydi
✓ Provider yaratadi
✓ Provider konfiguratsiyasini yuklaydi
✓ Provider Instance qaytaradi
✓ Provider Lifecycle bilan integratsiyalashadi
---
# Not Responsible
ProviderFactory
✗ API Request
✗ Market Data Retrieval
✗ Data Validation
✗ Market Analysis
✗ Signal Generation
✗ Trading Decision
---
# Input
ProviderFactory qabul qiladi.
• Provider Request
• Provider Name
• Configuration
---
# Output
ProviderFactory yaratadi.
• Provider Instance
• Provider Metadata
• Initialization Status
---
# Workflow
```text
Receive Provider Request
↓
Read Configuration
↓
Select Provider
↓
Create Provider
↓
Initialize Provider
↓
Return Provider Instance
```
---
# Golden Rules
1. Har bir Provider ProviderInterface'ni implement qilishi shart.
2. Provider faqat ProviderFactory orqali yaratiladi.
3. ProviderFactory Provider Logic bajarmaydi.
4. ProviderFactory Provider turiga bog'liq kod yozmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
ProviderFactory/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
ProviderFactory GoldBot Data Layer ichidagi Canonical Factory moduli bo'lib, barcha Market Data Provider'larni yaratish, tanlash va ishga tushirish uchun yagona kirish nuqtasi hisoblanadi.
