# Platform Layer Data Flow
Status: CANONICAL
---
# Purpose
Ushbu hujjat GoldBot Platform Layer ichidagi ma'lumotlar oqimini (Data Flow) tavsiflaydi.
Platform Layer foydalanuvchi va GoldBot Core o'rtasidagi yagona kirish va chiqish (Entry/Exit) nuqtasi hisoblanadi.
---
# Layer Data Flow
```text
User
        │
        ▼
        ├──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
   Telegram      MobileAPI         WebAPI         DesktopAPI
        │              │              │              │
        └──────────────┴──────────────┴──────────────┘
                       │
                       ▼
                Authentication
        │
        ▼
PlatformService
        │
        ├──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼              ▼
 AIService     DecisionService   RiskService   ExecutionService   DatabaseService
        │
        ▼
NotificationCenter
        │
        ▼
Telegram / Mobile / Web / Desktop
        │
        ▼
User
```
---
# Input Sources
• User Request
• API Request
• Authentication Request
• Internal Event
• Notification Event
---
# Output
• Platform Response
• Authentication Result
• API Response
• Notification
• Session Metadata
---
# Data Flow Rules
1. Barcha User Request Platform Layer orqali kiradi.
2. Telegram, MobileAPI, WebAPI, DesktopAPI bir-birining natijasiga bog'liq emas va parallel mustaqil kanallar sifatida ishlaydi; har biri Authentication'ni alohida chaqiradi.
3. Authentication Protected Request uchun majburiy.
3. PlatformService Request'ni kerakli Service'ga marshrutlaydi.
4. Notification faqat NotificationCenter orqali yuboriladi.
5. Platform Layer Business Logic bajarmaydi.
---
# Summary
Platform Layer GoldBot arxitekturasidagi Canonical User Communication Pipeline hisoblanadi.
