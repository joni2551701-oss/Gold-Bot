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
# 2. Audit Principles
1. Architecture first.
2. Evidence first.
3. No assumptions.
4. No implementation review.
5. Consistency over preference.
6. Every finding must include evidence.
7. Every recommendation must include rationale.
---
# 3. Audit Scope
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
# 4. Audit Rules
* Auditor taxmin qilmaydi.
* Faqat hujjat asosida baho beradi.
* Har bir xulosa dalil bilan yoziladi.
* Tavsiya va xato alohida yoziladi.
* Hech bir Layer boshqa Layer vazifasini bajarmasligi kerak.
---
# 5. Audit Stages
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
# 6. Scoring System
Status: CANONICAL
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
---
# 7. Severity Levels
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
# 8. Acceptance Criteria
Status: CANONICAL
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
---
# 9. Freeze Procedure
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
# 9a. Architecture Lock (Audit davomida)
Audit boshlanganidan (Layer Audit) to Final Report yakunlanguncha, `New_Map/` arxitekturasiga o'zgartirish kiritish taqiqlanadi.
```text
Architecture Freeze v1.0
↓
Architecture Audit
↓
Final Report
↓
Agar kerak bo'lsa ACR
↓
Version 1.1
```
Audit davomida (Architecture Lock kuchda bo'lgan paytda):
* yangi modul qo'shilmaydi;
* modul nomi o'zgarmaydi;
* Data Flow o'zgarmaydi;
* Contracts o'zgarmaydi.

Sabab: aks holda audit mezoni va audit obyekti bir vaqtning o'zida o'zgarib, natijalar taqqoslanmaydigan bo'lib qoladi. Zarurat tug'ilsa, o'zgartirish faqat audit yakunlanib Final Report chiqqandan so'ng, ACR orqali (masalan Version 1.1 sifatida) amalga oshiriladi.
---
# 9b. Module Audit Rule (Phase 2, ACR amendment)
Har bir modul faqat o'zi uchun javobgar.

```text
Agar modul ichida boshqa modulning
responsibility aniqlansa:
→ Critical

Agar ownership overlap aniqlansa:
→ Critical

Agar stale documentation topilsa:
→ Major

Agar diagram va Contracts mos kelmasa:
→ Major

Agar naming farq qilsa:
→ Minor
```

Bu qoida Phase 1 — Layer Audit davomida eng ko'p uchragan xato turlarini (Boundary Gateway ziddiyati, Ownership overlap, Artifact ≠ Module, stale README) Module Audit darajasida ham izchil baholash uchun qo'llaniladi.

## Module Audit Tekshiruv Ro'yxati
1. **Module Identity** — Purpose, Objective, Responsibility, Not Responsible bir martalik va aniqmi?
2. **Internal Structure** — ModuleMap ↔ README ↔ Contracts bir xil narsani aytyaptimi?
3. **Workflow** — SequenceDiagram ↔ README Workflow ↔ Contracts Runtime Flow bir xilmi?
4. **Contracts** — Allowed/Forbidden Dependencies, Input, Output, Boundary to'g'rimi?
5. **Ownership** — Har bir vazifaning bitta egasi bormi (masalan ContextEngine ↔ ContextService, StrategyManager ↔ StrategyEngine)?
6. **Dependency** — Circular yoki Hidden Dependency bormi?
7. **Data Flow** — Input → Processing → Output hamma hujjatda bir xilmi?
8. **Naming** — README, ModuleMap, Contracts, SequenceDiagram bir xil nom ishlatganmi?
9. **Documentation** — Eski matn, Stale Diagram yoki Broken Link qolmaganmi?

## Module Runtime Ownership Rule
```text
A module may reference another module,
but may never document that module's
runtime algorithm, workflow, or sequence.

A module may produce an output that is
consumed by another module. However, it
must never document the next module's
runtime actions. Module boundary ends
at its own output.

Violation:
→ Critical
```
Sabab: har bir modul faqat o'zining runtime'ini hujjatlashtiradi va faqat o'z output'i bilan tugaydi. Boshqa modulning lifecycle/sequence'ini yoki keyingi modulning runtime harakatlarini o'z hujjatiga yozish Ownership Overlap (Forbidden Dependency in Runtime Workflow) hisoblanadi — har bir modul mustaqil ravishda audit qilinishi va mustaqil ravishda o'zgarishi kerak bo'lgan alohida Canonical hujjat hisoblanadi. Bu qoida ikki marta aniqlandi: `01_Data_Layer/Historical_Data/Bootstrap` modulida Recovery'ning runtime ketma-ketligi Bootstrap'ning o'z SequenceDiagram'i ichida hujjatlashtirilgani (Critical, Ownership Overlap), va `01_Data_Layer/Historical_Data/Recovery` modulida "Resume Live Stream" (Live_Data modulining lifecycle harakati) Recovery'ning o'z SequenceDiagram'i ichida hujjatlashtirilgani (Critical, Ownership Overlap / Forbidden Dependency in Runtime Workflow) aniqlanganidan keyin qo'shildi.

## Dependency Source of Truth Rule
```text
Contracts.md is the canonical source
for module dependencies.
ModuleMap.md must always mirror
Contracts.md exactly.

Any mismatch:
→ Major
```
Sabab: Contracts.md modulning rasmiy interfeysi va arxitektura shartnomasini belgilaydi; ModuleMap.md esa shu shartnomani vizual/strukturaviy aks ettirishi kerak. Agar Allowed/Forbidden Dependencies ro'yxati ikkala hujjatda turlicha bo'lsa, Contracts.md ustun hisoblanadi va ModuleMap.md unga moslashtiriladi. Bu qoida `01_Data_Layer/Historical_Data/HistoricalProviders` modulida ModuleMap.md'ning Allowed Dependencies'da Network Layer'ni va Forbidden Dependencies'da Event System/Future Expansion Layer'ni Contracts.md'ga nisbatan tushirib qoldirgani aniqlanganidan keyin qo'shildi (Major, Documentation Consistency).

## Module Runtime Boundary Rule
```text
A module's SequenceDiagram must terminate
at its own output or at the caller.
It must never continue into the runtime
of downstream modules.

Violation:
→ Critical
```
Sabab: har bir modulning SequenceDiagram'i faqat o'z javobgarlik chegarasini ko'rsatadi; keyingi modulning ichki jarayoni boshqa modul hujjatlarida tasvirlanmaydi. Bu qoida `01_Data_Layer/Historical_Data/HistoricalDatabase` modulida "Validation Sequence" va yopilish Summary'sining Historical Database'ning o'z Forbidden Dependencies'iga (Data Validation, Market Memory) qaramay ushbu modullarning runtime'iga davom etgani aniqlanganidan keyin qo'shildi (Critical, Ownership Overlap / Runtime Boundary Violation) — Bootstrap va Recovery auditlarida tasdiqlangan Module Runtime Ownership Rule'ning yana bir ko'rinishi sifatida.

## Group README Rule
```text
Every canonical module declared in
Layer_ModuleMap must also appear in:
• Internal Structure
• Module Overview
• Repository Structure
of the Group README.

Missing module:
→ Major
```
Sabab: Group README bo'lim ichidagi barcha modullarning to'liq va aniq ro'yxatini taqdim etishi shart; agar Layer_ModuleMap.md'da rasmiy Orchestrator yoki boshqa har qanday modul sifatida e'lon qilingan modul Group README'ning Internal Structure/Module Overview/Repository Structure bo'limlarida ko'rsatilmasa, bu Canonical Module Identity buzilishi hisoblanadi. Bu qoida `01_Data_Layer/Live_Data` guruhida README.md'ning LiveDataService'ni (Layer_ModuleMap.md'da e'lon qilingan markaziy Orchestrator) uchala bo'limdan ham tushirib qoldirgani aniqlanganidan keyin qo'shildi (Major, Canonical Module Identity).
---
# 10. Change Management
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
# 11. Audit Report Template
Har bir Layer uchun quyidagi shablon bo'yicha hisobot chiqariladi.
```text
Layer:
<Layer Nomi>

Architecture Score:
Layer Responsibility:   <ball> / 20
Module Consistency:     <ball> / 20
Data Flow:              <ball> / 20
Dependency:             <ball> / 20
Documentation:          <ball> / 20
Total Score:            <ball> / 100

Strengths:
<topilgan kuchli tomonlar ro'yxati>

Problems:
<Critical va Major toifasidagi topilmalar, dalil bilan>

Warnings:
<Minor toifasidagi topilmalar, dalil bilan>

Suggestions:
<Suggestion toifasidagi tavsiyalar, asos bilan>

Dependencies:
<tekshirilgan Allowed/Forbidden Dependencies natijasi>

Boundary Check:
<Layer boshqa Layer mas'uliyatini bajarmaganligi bo'yicha xulosa>

Status:
<APPROVED | APPROVED WITH NOTES | REVISION REQUIRED | REJECTED>
```
---
# 11a. Module Audit Report Template (Phase 2, ACR amendment)
Har bir modul uchun quyidagi shablon bo'yicha hisobot chiqariladi.
```text
Module:
<Modul Nomi>

Architecture Score:
Responsibility:   <ball> / 20
Consistency:      <ball> / 20
Data Flow:        <ball> / 20
Dependency:       <ball> / 20
Documentation:    <ball> / 20
Total Score:      <ball> / 100

Strengths:
<topilgan kuchli tomonlar ro'yxati>

Problems:
<Critical va Major toifasidagi topilmalar, dalil bilan>

Warnings:
<Minor toifasidagi topilmalar, dalil bilan>

Suggestions:
<Suggestion toifasidagi tavsiyalar, asos bilan>

Dependencies:
<tekshirilgan Allowed/Forbidden Dependencies natijasi>

Boundary Check:
<modul boshqa modul mas'uliyatini bajarmaganligi bo'yicha xulosa>

Status:
<APPROVED | APPROVED WITH NOTES | REVISION REQUIRED | REJECTED>
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
Architecture Freeze
```
---
# Note on Status
Ushbu hujjat Director tomonidan to'liq ko'rib chiqilgan va tasdiqlangan — barcha 11 bo'lim (Audit Objective, Audit Principles, Audit Scope, Audit Rules, Audit Stages, Scoring System, Severity Levels, Acceptance Criteria, Freeze Procedure, Change Management/ACR, Audit Report Template) `Status: CANONICAL` hisoblanadi.

Scoring System va Acceptance Criteria ataylab shu bosqichda muzlatildi (audit boshlanishidan oldin), toki barcha 13 Layer bir xil mezon bilan baholansin va natijalar taqqoslanadigan bo'lsin.

Ushbu hujjat Architecture Freeze v1.0 tarkibiga kiradi. Shu sababli, bundan buyon Layer nomi, Modul nomi, Data Flow, Contract yoki ushbu Audit metodologiyasining o'zi faqat Architecture Change Request (ACR) jarayoni orqali o'zgartiriladi (masalan, Version 1.1 sifatida).

Metodologiya tasdiqlangani sababli, Layer Audit (1-bosqich) boshlanishi mumkin. Audit boshlangan lahzadan Final Report yakunlanguncha 9a-bo'limdagi Architecture Lock kuchda bo'ladi.

Phase 1 — Layer Audit tartibi (`New_Map/` dagi haqiqiy papka nomlari bo'yicha):
```text
01_Data_Layer
↓
02_Core_Layer
↓
03_Context_Layer
↓
04_Indicator_Layer
↓
05_Strategy_Layer
↓
06_Signal_Layer
↓
07_AI_Layer
↓
08_Decision_Layer
↓
09_Risk_Layer
↓
10_Execution_Layer
↓
11_Trade_Monitoring_Layer
↓
12_Database_Layer
↓
13_Platform_Layer
```
---
# Summary
Architecture Audit Plan GoldBot Canonical Architecture'ning barcha Layer, Module va Cross-Layer aloqalarini, shuningdek nomlash standartlarini yagona metodologiya asosida tekshirish, natijalarni standart Scoring System va Severity Levels bo'yicha baholash, va yakunda Architecture Freeze orqali loyihani "konstitutsiya" darajasidagi spetsifikatsiya sifatida muzlatishni belgilovchi rasmiy reja hisoblanadi. Freeze'dan keyingi har qanday o'zgarish faqat Architecture Change Request (ACR) jarayoni orqali amalga oshiriladi.
