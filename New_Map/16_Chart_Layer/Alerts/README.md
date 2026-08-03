# Alerts
Status: BLUEPRINT
---
# Purpose
Alerts GoldBot Chart Layer ichidagi Canonical Alerts moduli hisoblanadi.
Price, Indicator, Drawing va Time Alert'larni boshqaruvchi Canonical Alert moduli.
Alerts Signal yaratmaydi.
Alerts BOS/CHoCH hisoblamaydi.
Alerts AI ishlatmaydi.
Alerts Risk hisoblamaydi.
---
# Objective
Alerts quyidagi vazifalarni bajaradi.
• Price Alert Management
• Indicator Alert Management
• Drawing Alert Management
• Time Alert Management
• Alert Notification
---
# Layer Position
```text
Analysis_Overlay
↓
Alerts
↓
Screenshot
```
---
# Responsibilities
Alerts
✓ Alert shartlarini tekshiradi
✓ Alert Trigger yaratadi
✓ Alert Notification'ni tayyorlaydi
---
# Not Responsible
Alerts
✗ Signal Generation
✗ Decision Making
✗ Trade Execution
✗ Notification Delivery (Platform Layer vazifasi)
---
# Input
Alerts qabul qiladi.
• Overlay Object
• Price Data
• Alert Configuration
---
# Output
Alerts yaratadi.
• Alert Trigger
• Alert Status
• Alert Metadata
---
# Workflow
```text
Analysis_Overlay
↓
Alerts
↓
Screenshot
```
---
# Internal Modules (Planned — Foundation Freeze'dan keyin implementatsiya qilinadi)
```text
Alerts
├── PriceAlerts/
├── IndicatorAlerts/
├── DrawingAlerts/
├── TimeAlerts/
└── AlertManager/
```
---
# Golden Rules
1. Alerts faqat o'z mas'uliyat doirasida ishlaydi.
2. Chart hech qachon Signal yaratmaydi.
3. Chart hech qachon BOS/CHoCH/FVG/Liquidity hisoblamaydi — bu GoldBot Core vazifasi.
4. Chart hech qachon AI ishlatmaydi.
5. Chart hech qachon Risk hisoblamaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Modules
```text
Alerts/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
Predecessor: Analysis_Overlay · Successor: Screenshot
---
# Summary
Alerts GoldBot Chart Layer ichidagi Alerts vazifalarini bajaruvchi Canonical modul hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, yuqoridagi Internal Modules ro'yxati Foundation Freeze'dan keyin haqiqiy implementatsiya bilan to'ldiriladi.
