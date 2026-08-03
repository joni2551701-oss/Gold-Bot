# Secrets Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Secrets ichki arxitekturasini tavsiflaydi (ichki submodullar implementatsiya bosqichida to'ldiriladi).
---
# Module Position
```text
Environment (Environment Variables / Secret Store)
↓
Secrets
↓
Configuration
```
---
# Module Architecture
```text
Secrets
        ├── SecretProvider
        ├── MaskedSecret
        ├── SecretRegistry
        ├── SecretValidator
        └── SecretRotation
```
---
# Internal Components
## SecretProvider
Maxfiy qiymatlarni Environment yoki Secret Store'dan o'qiydi. Yagona o'qish nuqtasi.
---
## MaskedSecret
Maxfiy qiymatni o'rab turuvchi qiymat tipi. Uning `repr`/`str` ko'rinishi har doim `***` qaytaradi, shuning uchun qiymat log'ga, `repr`ga yoki traceback'ga hech qachon tushmaydi. Haqiqiy qiymat faqat `reveal()` orqali olinadi.
---
## SecretRegistry
Ma'lum maxfiy kalitlar katalogi — har bir kalitning nomi, majburiy/ixtiyoriy ekanligi va qaysi Provider'ga tegishli ekanligi.
---
## SecretValidator
Startup vaqtida majburiy maxfiy qiymatlarning mavjudligini tekshiradi. Yetishmovchilik aniqlansa Runtime boshlanmaydi.
---
## SecretRotation
Maxfiy qiymatlarni Runtime'ni to'xtatmasdan almashtirish jarayonini boshqaradi.
---
# Dependency Map
```text
Environment
↓
Secrets
↓
Configuration
```
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
# Ownership
Secrets GoldBot'dagi barcha maxfiy qiymatlarning yagona egasi hisoblanadi.
Hech bir boshqa modul maxfiy qiymatni Environment'dan bevosita o'qimaydi va o'z nusxasini saqlamaydi.
---
# Module Rules
1. Maxfiy qiymat faqat Secrets orqali olinadi.
2. Har bir qiymat MaskedSecret sifatida qaytariladi.
3. Majburiy qiymat yetishmasa Runtime boshlanmaydi.
4. Rotation Runtime'ni to'xtatmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Summary
Secrets GoldBot Core Layer ichidagi barcha maxfiy ma'lumotlarni boshqaruvchi yagona Canonical modul hisoblanadi.
