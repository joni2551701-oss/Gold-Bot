# Architecture Audit Plan
Status: DRAFT (metodologiya loyihasi — Director tomonidan hali tasdiqlanmagan)
---
# Purpose
Ushbu hujjat GoldBot Canonical Architecture (`New_Map/`) uchun rasmiy Audit Metodologiyasini belgilaydi.
Kod implementatsiyasi boshlanishidan oldin arxitektura to'liq tekshiruvdan o'tishi va so'ngra Architecture Freeze v1.0 orqali rasmiy spetsifikatsiya sifatida muzlatilishi shart.
Ushbu metodologiya nafaqat v1 audit uchun, balki kelajakdagi barcha auditlar (v2, v3, yangi modul qo'shilishi) uchun ham yagona standart hisoblanadi.
---
# 1. Audit Objective
Audit'ning maqsadi:
* Har bir Layer va Module'ning mas'uliyati aniq va bir martalik (single-responsibility) ekanligini tasdiqlash.
* Layer'lar orasidagi Data Flow to'g'ri va izchil ekanligini tekshirish.
* Circular Dependency va Layer-Skipping kabi arxitektura buzilishlarini aniqlash.
* Nomlash standarti (Engine/Manager/Service/Repository/Validator/Gateway/Coordinator) barcha modullarda bir xil qo'llanganini tasdiqlash.
* Auditdan o'tgan arxitekturani Architecture Freeze v1.0 sifatida rasmiylashtirish va kod implementatsiyasi uchun yagona asos qilib belgilash.
---
# 2. Audit Scope
Audit qilinadi
* Layer Architecture
* Module Architecture
* Data Flow
* Sequence
* Contracts
* Naming
* Dependency
* Consistency

Audit qilinmaydi
* Python Code
* Performance
* Security Testing
* Unit Test
* UI Design
* Trading Strategy sifati
* AI Prompt sifati
---
# 3. Audit Rules
* Auditor taxmin qilmaydi.
* Faqat hujjat asosida baho beradi.
* Har bir xulosa dalil bilan yoziladi.
* Tavsiya va xato alohida yoziladi.
* Hech bir Layer boshqa Layer vazifasini bajarmasligi kerak.
---
# 4. Audit Stages
## Layer Audit
Har bir Layer alohida tekshiriladi.

Masalan:
```text
01_Data_Layer          ✅
02_Market_Data         ✅
03_Context             ✅
...
13_Platform            ✅
```

Tekshiriladi:
* Layer vazifasi aniqmi?
* Ortiqcha modul yo'qmi?
* Yetishmayotgan modul yo'qmi?
* Layer boshqa Layer ishini qilmayaptimi?
---
## Module Audit
Har bir modul tekshiriladi.

Masalan:
```text
DecisionEngine
README
ModuleMap
SequenceDiagram
Contracts
```

Tekshiriladi:
* README ↔ Contracts mosmi?
* ModuleMap ↔ SequenceDiagram mosmi?
* Input/Output bir xilmi?
* Responsibility hamma faylda bir xilmi?
---
## Cross-Layer Audit
Bu eng muhim qism.

Masalan:
```text
Signal Layer
      │
      ▼
AI Layer
      │
      ▼
Decision Layer
```

Tekshiriladi:
* Data Flow to'g'rimi?
* Circular Dependency yo'qmi?
* Noto'g'ri chaqiriqlar yo'qmi?
* Public Service orqali chaqiryaptimi?

Masalan:
```text
❌ AI → DatabaseRepository
To'g'ri emas
AI → DatabaseService → Repository
```

yoki

```text
❌ Telegram → DecisionEngine
To'g'ri emas
Telegram
    │
PlatformService
    │
DecisionService
```
---
## Naming Audit
Bu keyinchalik juda katta muammolarni oldini oladi.

Masalan:
```text
DecisionEngine
RiskEngine
ExecutionEngine
MonitoringService
DatabaseService
```

hammasi bir xil standartga mos bo'lishi kerak.

Misollar:
* Engine — hisoblaydi yoki qaror chiqaradi.
* Manager — boshqaradi.
* Service — tashqi interfeys (Public API).
* Repository — ma'lumot saqlaydi.
* Validator — tekshiradi.
* Gateway — tashqi tizim bilan ishlaydi.
* Coordinator — bir nechta modulni muvofiqlashtiradi.
---
# 5. Scoring System
100 ballik tizim o'rniga kategoriya bo'yicha baholash qo'llanadi.
```text
Layer Responsibility      20
Module Consistency        20
Data Flow                 20
Dependency                20
Documentation             20
```
Jami:
```text
100 points
```
Chegaralar keyinchalik birgalikda aniqlanadi.
---
# 6. Severity Levels
```text
Critical
Architecture ishlamaydi
Major
Katta arxitektura muammosi
Minor
Yaxshilash mumkin
Suggestion
Faqat tavsiya
```
---
# 7. Acceptance Criteria
```text
95–100
APPROVED
85–94
APPROVED WITH NOTES
70–84
REVISION REQUIRED
0–69
REJECTED
```
Bu faqat misol. Chegaralarni keyin birgalikda aniqlash mumkin.
---
# 8. Freeze Procedure
Freeze quyidagi ketma-ketlik yakunlangandan so'ng beriladi.
```text
Layer Audit tugaydi
↓
Module Audit tugaydi
↓
Cross Layer Audit tugaydi
↓
Naming Audit tugaydi
↓
Final Report
↓
Architecture Freeze
```
---
# 9. Change Management
Architecture Freeze'dan keyin quyidagilarning har qandayi oddiy tahrir bilan emas, balki **Architecture Change Request (ACR)** orqali amalga oshiriladi.
* Layer nomini o'zgartirish.
* Yangi modul qo'shish.
* Data Flow'ni o'zgartirish.
* Contract'ni o'zgartirish.

## ACR Jarayoni
```text
Problem
↓
Reason
↓
Impact
↓
Proposal
↓
Director Approval
↓
Implementation
↓
New Version
```
ACR'siz Freeze'dan keyingi hech qanday Layer nomi, Modul nomi, Data Flow yoki Contract o'zgartirilmaydi.
---
# 10. Audit Report Template
Har bir Layer uchun quyidagi shablon bo'yicha hisobot chiqariladi.
```text
<Layer Nomi>
Layer Responsibility:   <ball> / 20
Module Consistency:     <ball> / 20
Data Flow:              <ball> / 20
Dependency:             <ball> / 20
Documentation:          <ball> / 20
Total Score:            <ball> / 100
Critical:
<son>
Major:
<son>
Minor:
<son>
Suggestion:
<son>
Status:
<APPROVED | APPROVED WITH NOTES | REVISION REQUIRED | REJECTED>
```
Bu shablon ham misol tariqasida keltirilgan bo'lib, 5–7-bo'limlar bilan birga yakuniy tahrirga ochiq.
---
# Audit Sequence
```text
Architecture_Audit_Plan
        │
        ▼
Layer Audit
        │
        ▼
Module Audit
        │
        ▼
Cross-Layer Audit
        │
        ▼
Naming Audit
        │
        ▼
Final Report
        │
        ▼
Architecture Freeze
```
---
# Note on Status
Ushbu hujjat hozircha DRAFT holatida. Barcha bo'limlar (ayniqsa 5–7: Scoring, Severity, Acceptance) Director tomonidan ko'rib chiqilib, kerakli chegaralar aniqlangandan so'nggina bu hujjat CANONICAL deb tasdiqlanadi. Faqat shundan keyin Layer Audit boshlanadi. Hujjat CANONICAL deb tasdiqlangach, unga ham Freeze qo'llaniladi — shundan keyin ushbu metodologiyaning o'zi ham ACR'siz o'zgartirilmaydi.
---
# Summary
Architecture Audit Plan GoldBot Canonical Architecture'ning barcha Layer, Module va Cross-Layer aloqalarini, shuningdek nomlash standartlarini yagona metodologiya asosida tekshirish, natijalarni standart Scoring System va Severity Levels bo'yicha baholash, va yakunda Architecture Freeze orqali loyihani "konstitutsiya" darajasidagi spetsifikatsiya sifatida muzlatishni belgilovchi rasmiy reja hisoblanadi. Freeze'dan keyingi har qanday o'zgarish faqat Architecture Change Request (ACR) jarayoni orqali amalga oshiriladi.
