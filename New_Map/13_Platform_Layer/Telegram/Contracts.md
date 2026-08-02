# Telegram Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Telegram modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Telegram quyidagilar uchun javobgar.
✓ Telegram Update Reception
✓ Command Processing
✓ Callback Processing
✓ Navigation Management
✓ Message Delivery
✓ Media Delivery
✓ Telegram Session Management
Telegram bajarmaydi.
✗ Trading Decision
✗ AI Analysis
✗ Authentication Logic
✗ Database Management
✗ Risk Calculation
✗ Order Execution
---
# Module Boundary
```text
Telegram User
↓
Telegram
↓
Authentication
↓
PlatformService
```
---
# Input Contract
• Telegram Update
• Command
• Callback Query
• User Message
• Platform Response
---
# Output Contract
• Telegram Message
• Telegram Media
• Reply Keyboard
• Inline Keyboard
• Telegram Metadata
---
# Allowed Dependencies
✓ Authentication
✓ PlatformService
✓ NotificationCenter
---
# Forbidden Dependencies
✗ DatabaseService
✗ AIService
✗ DecisionService
✗ RiskService
✗ ExecutionService
✗ MonitoringService
---
# Runtime Contract
1. Har bir Telegram Update qabul qilinishi shart.
2. Command va Callback to'g'ri ajratilishi shart.
3. Protected Command Authentication'dan o'tishi shart.
4. Reply Keyboard va Inline Keyboard Telegram standartlariga mos bo'lishi shart.
5. PlatformService'dan kelgan Response o'zgartirilmasdan foydalanuvchiga yetkazilishi shart.
6. Telegram Business Logic bajarmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Update qabul qilinadi.
✓ Command qayta ishlanadi.
✓ Callback qayta ishlanadi.
✓ Navigation yaratiladi.
✓ Message yuboriladi.
✓ Media yuboriladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Telegram Contract GoldBot Platform Layer ichidagi Telegram platformasi bilan integratsiyani, Command, Callback, Navigation va Message boshqaruvini hamda PlatformService bilan xavfsiz muloqotni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
