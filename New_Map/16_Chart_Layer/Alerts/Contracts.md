# Alerts Contracts
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Alerts modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Alerts quyidagilar uchun javobgar.
✓ Price Alert Management
✓ Indicator Alert Management
✓ Drawing Alert Management
✓ Time Alert Management
✓ Alert Notification
Alerts bajarmaydi.
✗ Signal Generation
✗ Decision Making
✗ Trade Execution
✗ Notification Delivery (Platform Layer vazifasi)
---
# Module Boundary
```text
Shared Render State / Chart State
↓
Alerts
↓
Chart_API (Exit)
```
Alerts Analysis_Overlay/Screenshot'ning ketma-ket Output'ini olmaydi — Render State/Chart State'ni kuzatadi (Chart Shared State Rule).
---
# Input Contract
• Render State (Overlay Object, Price Data)
• Alert Configuration
---
# Output Contract
• Alert Trigger
• Alert Status
• Alert Metadata
---
# Allowed Dependencies
✓ Analysis_Overlay
✓ Drawing_Tools
✓ Chart_Data
✓ Chart_API
---
# Forbidden Dependencies
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
✗ Platform Layer
---
# Public API (Blueprint — imzolar implementatsiya bosqichida aniqlanadi)
```text
getAlertsState()
subscribeAlertsEvent(callback)
configureAlerts(options)
disposeAlerts()
```
---
# Architecture Rules
Alerts:
✓ Price Alert Management bajaradi.
✓ Module Boundary'ni saqlaydi.
Alerts:
✗ Signal yoki Decision yaratmaydi.
✗ BOS/CHoCH/FVG/Liquidity hisoblamaydi.
✗ AI ishlatmaydi.
---
# Runtime Rules
1. Alerts faqat o'z Module Boundary ichida ishlaydi.
2. Har bir Input tekshirilishi shart.
3. Output standart formatda yaratilishi shart.
4. Alerts Signal yoki Decision yaratmaydi.
5. Alerts BOS/CHoCH/FVG/Liquidity hisoblamaydi.
6. Alerts Render State/Chart State'ni kuzatadi — ketma-ket modul Output'ini iste'mol qilmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Input qabul qilinadi.
✓ Price Alert Management bajariladi.
✓ Output yaratiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Alerts Contract GoldBot Chart Layer ichidagi Alerts jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi (Blueprint bosqichi).
