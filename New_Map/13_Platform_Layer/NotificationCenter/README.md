# Notification Center
Status: CANONICAL
---
# Purpose
NotificationCenter GoldBot Platform Layer ichidagi Canonical Notification Delivery moduli hisoblanadi.
Uning asosiy vazifasi GoldBot tizimida yuz beradigan Signal, Trade, Risk, AI, System va Security hodisalari haqida foydalanuvchiga xabarlarni kerakli platforma orqali yetkazishdir.
NotificationCenter Trading Decision qabul qilmaydi.
NotificationCenter Business Logic bajarmaydi.
NotificationCenter faqat Notification Delivery bilan shug'ullanadi.
---
# Objective
NotificationCenter quyidagi vazifalarni bajaradi.
• Signal Notification
• Trade Notification
• Risk Notification
• AI Notification
• System Notification
• Security Notification
• Notification Routing
---
# Layer Position
```text
Internal Services
↓
NotificationCenter
↓
Telegram
MobileAPI
WebAPI
DesktopAPI
```
---
# Responsibilities
NotificationCenter
✓ Notification qabul qiladi
✓ Notification Priority aniqlaydi
✓ Delivery Platform tanlaydi
✓ Notification yuboradi
✓ Delivery Status kuzatadi
✓ Notification History yaratadi
---
# Not Responsible
NotificationCenter
✗ Trading Decision
✗ Authentication
✗ Database Management
✗ Order Execution
✗ AI Analysis
✗ User Management
---
# Input
NotificationCenter qabul qiladi.
• Signal Event
• Trade Event
• Risk Event
• AI Event
• System Event
• Security Event
---
# Output
NotificationCenter yaratadi.
• Delivered Notification
• Delivery Status
• Notification Metadata
• Delivery Report
---
# Notification Types
• Signal
• Trade
• Risk
• AI
• System
• Security
---
# Workflow
```text
Receive Notification Event
↓
Validate Notification
↓
Determine Priority
↓
Select Platform
↓
Deliver Notification
↓
Receive Delivery Status
↓
Generate Delivery Report
```
---
# Golden Rules
1. Har bir Notification User ID bilan bog'langan bo'lishi shart.
2. Notification faqat ruxsat etilgan platformaga yuboriladi.
3. Delivery natijasi log qilinishi shart.
4. Failed Delivery qayta urinish siyosatiga ega bo'lishi shart.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
NotificationCenter/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
NotificationCenter GoldBot Platform Layer ichidagi Canonical Notification Delivery moduli bo'lib, tizimdagi barcha hodisalarni foydalanuvchiga xavfsiz va standart usulda yetkazadi.
