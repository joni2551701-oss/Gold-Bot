# Secrets Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Secrets modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Secrets quyidagilar uchun javobgar.
✓ Secret Loading (Environment / Secret Store'dan)
✓ Secret Masking (leak protection)
✓ Required / Optional Secret Distinction
✓ Secret Validation
✓ Secret Rotation
✓ Single Access Point Enforcement
Secrets bajarmaydi.
✗ Business Logic
✗ Trading Logic
✗ AI Analysis
✗ Configuration Management (Configuration vazifasi)
✗ Authentication (13_Platform_Layer/Authentication vazifasi)
✗ Authorization
✗ Audit Logging (12_Database_Layer/AuditLog vazifasi)
---
# Module Boundary
```text
Environment (Environment Variables / Secret Store)
↓
Secrets
↓
Configuration
```
---
# Input Contract
• Environment Variables
• Secret Store Reference
• Secret Request (kalit nomi bo'yicha)
• Rotation Request
---
# Output Contract
• Masked Secret
• Revealed Secret (faqat aniq `reveal()` chaqiruvida)
• Secret Presence Status
• Validation Result
---
# Allowed Dependencies
✓ Configuration
✓ CoreEngine
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
✗ Media Layer
✗ Backtesting Layer
---
# State Contract
• Unloaded
• Loading
• Loaded
• Validated
• Rotating
• Failed
---
# Runtime Contract
1. Barcha maxfiy qiymatlar faqat Secrets moduli orqali olinadi.
2. Hech bir boshqa modul Environment'dan bevosita maxfiy qiymat o'qimaydi.
3. Maxfiy qiymat sukut bo'yicha Masked ko'rinishda qaytariladi.
4. Haqiqiy qiymat faqat aniq `reveal()` chaqiruvi bilan olinadi.
5. Majburiy maxfiy qiymat yetishmasa, Runtime boshlanmaydi (fail fast).
6. Ixtiyoriy maxfiy qiymat yetishmasa, tegishli Provider "disabled" holatiga o'tadi (fail safe).
7. Maxfiy qiymat hech qachon log'ga, repr'ga yoki traceback'ga tushmaydi.
8. Maxfiy qiymatlar Database'ga ochiq ko'rinishda yozilmaydi.
9. Secret Rotation Runtime'ni to'xtatmasdan bajariladi.
10. Circular Dependency qat'iyan taqiqlanadi.
---
# Architecture Rules
Secrets:
✓ Maxfiy qiymatlarni yuklaydi va taqdim etadi.
✓ Masking'ni majburlaydi.
✓ Validation bajaradi.
✓ Rotation boshqaradi.
Secrets:
✗ Business Logic bajarmaydi.
✗ Trading Decision qabul qilmaydi.
✗ Foydalanuvchini autentifikatsiya qilmaydi.
✗ Maxfiy qiymatni oshkor holda saqlamaydi.
---
# Contract Violations
Quyidagilar Architecture Violation hisoblanadi.
• Secrets modulidan tashqarida `os.getenv` orqali maxfiy qiymat o'qish
• Maxfiy qiymatni log'ga yozish
• Maxfiy qiymatni Database'ga ochiq ko'rinishda saqlash
• Masked Secret'ni `reveal()`siz oshkor qilishga urinish
• Majburiy maxfiy qiymat yetishmasa ham Runtime'ni davom ettirish
• Circular Dependency
---
# Acceptance Criteria
✓ Maxfiy qiymatlar Environment'dan yuklanadi.
✓ Har bir qiymat Masked ko'rinishda qaytariladi.
✓ Majburiy qiymatlar Startup'da tekshiriladi.
✓ Yetishmayotgan majburiy qiymat Runtime'ni to'xtatadi.
✓ Yetishmayotgan ixtiyoriy qiymat Provider'ni "disabled" qiladi.
✓ Hech qanday maxfiy qiymat log'ga tushmaydi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Secrets Contract GoldBot'dagi barcha maxfiy ma'lumotlarni yagona kirish nuqtasi orqali boshqarishni, ularni Masked ko'rinishda saqlashni va hech qachon oshkor bo'lishiga yo'l qo'ymaslikni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
