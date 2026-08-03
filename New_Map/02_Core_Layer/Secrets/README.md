# Secrets
Status: CANONICAL
---
# Purpose
Secrets — GoldBot Core Layer ichidagi Canonical maxfiy ma'lumot boshqaruv komponentidir.
Uning asosiy vazifasi GoldBot'dagi barcha maxfiy qiymatlarni (API Keys, Broker Credentials, Telegram Token, AI API Keys, Database Credentials, Encryption Keys) yagona kirish nuqtasi orqali taqdim etishdir.
Secrets maxfiy qiymatni hech qachon log'ga, repr'ga yoki traceback'ga chiqarmaydi.
Secrets Business Logic bajarmaydi.
Secrets Runtime Decision qabul qilmaydi.
---
# Objective
Secrets quyidagi vazifalarni bajaradi:
• API Key Management
• Broker Credential Management
• Telegram Token Management
• AI API Key Management
• Database Credential Management
• Encryption Key Management
• Secret Validation
• Secret Rotation
• Secret Masking (leak protection)
---
# Layer Position
```text
Environment (Environment Variables / Secret Store)
↓
Secrets
↓
Configuration
↓
All GoldBot Layers
```
---
# Responsibilities
Secrets:
✓ Maxfiy qiymatlarni Environment'dan o'qiydi
✓ Majburiy va ixtiyoriy maxfiy qiymatlarni farqlaydi
✓ Har bir maxfiy qiymatni Masked ko'rinishda saqlaydi
✓ Startup vaqtida majburiy maxfiy qiymatlarni tekshiradi
✓ Secret Rotation'ni boshqaradi
✓ Barcha Layer'lar uchun yagona kirish nuqtasi bo'lib xizmat qiladi
---
# Not Responsible
Secrets:
✗ Business Logic
✗ Trading Logic
✗ AI Analysis
✗ Configuration Management (Configuration vazifasi)
✗ Authentication (13_Platform_Layer/Authentication vazifasi)
✗ Authorization
✗ Audit Logging (12_Database_Layer/AuditLog vazifasi)
---
# Input
Secrets qabul qiladi:
• Environment Variables
• Secret Store Reference
• Secret Request (kalit nomi bo'yicha)
• Rotation Request
---
# Output
Secrets yaratadi:
• Masked Secret
• Revealed Secret (faqat aniq so'ralganda)
• Secret Presence Status
• Validation Result
---
# Managed Secrets
Secrets quyidagi maxfiy qiymatlarni boshqaradi:
• API Keys (Market Data Provider'lar)
• Broker Credentials (Bitget, Binance va boshqalar)
• Telegram Token va Owner/Chat identifikatorlari
• AI API Keys (Gemini, OpenAI, Claude, Grok, ElevenLabs)
• Database Credentials
• Encryption Keys va Salt/Pepper qiymatlari
---
# Workflow
```text
Read Environment
↓
Wrap as Masked Secret
↓
Validate Required Secrets
↓
Provide on Request
↓
Rotate When Needed
```
---
# Internal Modules (Planned — implementatsiya bosqichida to'ldiriladi)
```text
Secrets
├── SecretProvider
├── MaskedSecret
├── SecretRegistry
├── SecretValidator
└── SecretRotation
```
---
# Golden Rules
1. Barcha maxfiy qiymatlar faqat Secrets moduli orqali olinadi — boshqa hech bir modul Environment'dan bevosita maxfiy qiymat o'qimaydi.
2. Maxfiy qiymat hech qachon log'ga, repr'ga yoki traceback'ga tushmaydi (Masked Secret majburiy).
3. Haqiqiy qiymat faqat aniq `reveal()` chaqiruvi bilan olinadi.
4. Majburiy maxfiy qiymat mavjud bo'lmasa, Runtime boshlanmaydi.
5. Ixtiyoriy maxfiy qiymat mavjud bo'lmasa, tegishli Provider "disabled" holatiga o'tadi — Runtime yiqilmaydi.
6. Maxfiy qiymatlar Database'ga ochiq ko'rinishda yozilmaydi.
7. Secret Rotation Runtime'ni to'xtatmasdan bajarilishi kerak.
8. Secrets Business Logic bajarmaydi.
9. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Secrets/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
Secrets GoldBot'dagi barcha maxfiy ma'lumotlar uchun yagona Canonical kirish nuqtasi hisoblanadi. U maxfiy qiymatlarni Environment'dan o'qiydi, Masked ko'rinishda saqlaydi, majburiy qiymatlarni Startup'da tekshiradi va hech qachon ularning oshkor bo'lishiga yo'l qo'ymaydi.
