# Architecture Audit Plan
Status: CANONICAL
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
Audit quyidagilarni qamrab oladi.
```text
New_Map/
├── 01_Data_Layer
├── 02_Core_Layer
├── 03_Context_Layer
├── 04_Indicator_Layer
├── 05_Strategy_Layer
├── 06_Signal_Layer
├── 07_AI_Layer
├── 08_Decision_Layer
├── 09_Risk_Layer
├── 10_Execution_Layer
├── 11_Trade_Monitoring_Layer
├── 12_Database_Layer
└── 13_Platform_Layer
```
Audit doirasiga kirmaydi:
* `15_Future_Expansion` (hali loyihalashtirilmagan, kelajak uchun ochiq qoldirilgan bo'lim).
* Haqiqiy kod (`data/`, `strategies/`, `risk/`, va h.k.) — bu hujjatlar faqat `New_Map/` arxitektura spetsifikatsiyasini tekshiradi, mavjud ishlab chiqilgan kodni emas.
---
# 3. Audit Rules
1. Audit har doim Layer Audit → Module Audit → Cross-Layer Audit → Naming Audit ketma-ketligida olib boriladi.
2. Har bir bosqich alohida hisobot bilan yakunlanadi; keyingi bosqichga avvalgisi tugamasdan o'tilmaydi.
3. Audit faqat mavjud `New_Map/` hujjatlarini tekshiradi — audit davomida yangi Layer yoki Module fayllari yaratilmaydi, faqat topilgan muammolar hisobotda qayd etiladi.
4. Har qanday tuzatish (Problem yoki Warning bo'yicha) alohida, Director tasdig'idan so'ng amalga oshiriladi — audit o'zi avtomatik tuzatish qilmaydi.
5. Audit natijalari har doim ushbu hujjatdagi Scoring System va Severity Levels asosida baholanadi.
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
Har bir Layer uchun Architecture Score 100% dan boshlanadi va topilgan muammolarga qarab kamayadi.
```text
Problem (Critical)     -10%  har biri uchun
Warning (Moderate)     -3%   har biri uchun
Suggestion (Minor)      0%   (ballga ta'sir qilmaydi, faqat qayd etiladi)
```
Yakuniy Score quyidagicha hisoblanadi:
```text
Architecture Score = 100% - (Problems × 10%) - (Warnings × 3%)
```
Score 0% dan past tushmaydi (minimal chegara 0%).
---
# 6. Severity Levels
| Daraja | Ta'rif | Misol |
|---|---|---|
| Problem | Arxitektura qoidasini bevosita buzadi (Circular Dependency, Layer-Skipping, mas'uliyat aralashuvi) | `Telegram → DecisionEngine` to'g'ridan-to'g'ri chaqiruvi |
| Warning | Qoidani bevosita buzmaydi, lekin izchillikka putur yetkazadi | `README` va `Contracts` orasidagi Input/Output nomuvofiqligi |
| Suggestion | Muammo emas, lekin yaxshilash mumkin bo'lgan joy | Terminologiyani yanada aniqroq qilish tavsiyasi |
---
# 7. Acceptance Criteria
Bir Layer quyidagi shartlarga javob bersagina APPROVED deb hisoblanadi.
✓ Architecture Score 90% yoki undan yuqori.
✓ 0 ta Problem (Critical) mavjud.
✓ Har bir modulda README, ModuleMap, SequenceDiagram va Contracts bir-biriga mos.
✓ Layer boshqa Layer'ning mas'uliyatini bajarmaydi.
✓ Barcha bog'liqliklar (Dependencies) faqat Contracts.md'da ro'yxatga olingan Allowed Dependencies orqali amalga oshadi.
✓ Nomlash standarti (Engine/Manager/Service/Repository/Validator/Gateway/Coordinator) buzilmagan.

90% dan past Score yoki 1 tadan ko'p Problem — "Needs Revision" statusini bildiradi va keyingi bosqichga o'tishdan oldin tuzatilishi shart.
---
# 8. Freeze Procedure
Barcha 13 Layer APPROVED statusini olgandan so'ng, quyidagi tartibda Freeze amalga oshiriladi.
1. Har bir Layer uchun yakuniy Audit Report tayyorlanadi (bo'lim 10 shabloni bo'yicha).
2. Barcha hisobotlar asosida yagona `Final_Audit_Report.md` yaratiladi.
3. Director yakuniy hisobotni ko'rib chiqadi va tasdiqlaydi.
4. Tasdiqlangandan so'ng `Architecture_Freeze_v1.0.md` hujjati yaratiladi — bu hujjat barcha Layer nomlari, Modul nomlari, Data Flow va Contracts'ni "muzlatilgan" (frozen) spetsifikatsiya sifatida belgilaydi.
5. Freeze'dan keyin har qanday o'zgarish faqat bo'lim 9'da (Change Management) belgilangan Architecture Change Request (ACR) jarayoni orqali amalga oshiriladi.
---
# 9. Change Management
Architecture Freeze v1.0'dan keyin quyidagilarning har qandayi oddiy tahrir bilan emas, balki **Architecture Change Request (ACR)** orqali amalga oshiriladi.
* Layer nomini o'zgartirish.
* Yangi modul qo'shish.
* Data Flow'ni o'zgartirish.
* Contract'ni o'zgartirish.

## ACR Jarayoni
```text
ACR Taklifi
        │
        ▼
Sabab va Ta'sir Tahlili
        │
        ▼
Cross-Layer Ta'sirini Tekshirish
        │
        ▼
Director Tasdig'i
        │
        ▼
Freeze Hujjatiga Yangilanish (versiya oshiriladi, masalan v1.1)
```
ACR'siz Freeze'dan keyingi hech qanday Layer nomi, Modul nomi, Data Flow yoki Contract o'zgartirilmaydi.
---
# 10. Audit Report Template
Har bir Layer uchun quyidagi shablon bo'yicha hisobot chiqariladi.
```text
<Layer Nomi>
Architecture Score:
<foiz>
Problems:
<son>
Warnings:
<son>
Suggestions:
<son>
Status:
<APPROVED | Needs Revision>
```
Misol (muammosiz Layer):
```text
01_Data_Layer
Architecture Score:
100%
Problems:
0
Warnings:
0
Suggestions:
0
Status:
APPROVED
```
Misol (muammoli Layer):
```text
08_Decision_Layer
Architecture Score:
96%
Problems:
1
Warnings:
2
Status:
Needs Revision
```
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
Architecture Freeze v1.0
```
---
# Summary
Architecture Audit Plan GoldBot Canonical Architecture'ning barcha Layer, Module va Cross-Layer aloqalarini, shuningdek nomlash standartlarini yagona metodologiya asosida tekshirish, natijalarni standart Scoring System va Severity Levels bo'yicha baholash, va yakunda Architecture Freeze v1.0 orqali loyihani "konstitutsiya" darajasidagi spetsifikatsiya sifatida muzlatishni belgilovchi rasmiy reja hisoblanadi. Freeze'dan keyingi har qanday o'zgarish faqat Architecture Change Request (ACR) jarayoni orqali amalga oshiriladi.
