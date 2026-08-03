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

## Canonical Naming Rule
```text
Every module has exactly one
canonical identifier.

README, Contracts, ModuleMap,
SequenceDiagram must all use
the same name.

Different spellings, spacing,
or formatting:
→ Minor
```
Sabab: bitta modulning turli hujjatlarda turlicha yozilishi (masalan "HistoricalDatabase" va "Historical Database") implementatsiyaga bevosita ta'sir qilmaydi, lekin hujjatlar va arxitekturaning izchilligini buzadi hamda kelajakda Dependency ro'yxatlarini solishtirishni chalkashtiradi. Bu qoida `01_Data_Layer/Live_Data/CandleBuilder` modulida ModuleMap.md'ning "Historical Database" (bo'sh joy bilan) deb yozgani, Contracts.md va boshqa barcha modullarning dependency ro'yxatlari esa "HistoricalDatabase" (bo'sh joysiz, papka/modul nomiga mos) deb yozgani aniqlanganidan keyin qo'shildi (Minor, Canonical Naming Consistency).

## Layer Naming Rule
```text
Architecture documents must
reference architectural layers
using their canonical Layer names.

"Layer" is canonical.
"Engine" must not be used when
referring to architectural layers.

Violation:
→ Minor
```
Sabab: Phase 1 Architecture Freeze v1.0'ga ko'ra GoldBot arxitekturasi Layer Architecture hisoblanadi; shuning uchun Context/Analysis/Strategy/Decision/Risk/Signal kabi arxitektura qatlamlariga murojaat qilinganda faqat "Layer" suffiksi ishlatiladi, "Engine" emas. Bu qoida `01_Data_Layer/Market_Memory/MemoryStorage` modulida Contracts.md "Context Layer, Analysis Layer, Strategy Layer, Decision Layer, Risk Layer, Signal Layer" deb yozgan bo'lsa, ModuleMap.md xuddi shu olti obyektni "Context Engine, Analysis Engine, Strategy Engine, Decision Engine, Risk Engine, Signal Engine" deb yozgani aniqlanganidan keyin qo'shildi (Minor, Canonical Naming Rule / Layer va Engine tushunchalarining aralashib ketishi).

## Cross-Cutting Layer Rule
```text
Infrastructure Layers
(Event System, Logging,
Notification, Monitoring
Infrastructure, etc.)
must not be documented as
fixed pipeline stages.

They are shared services
used by multiple layers.

Their canonical position is:
Source Modules
↓
Infrastructure Layer
↓
Target Modules

Violation:
→ Major
```
Sabab: Event System kabi infratuzilma qatlamlari GoldBot'ning barcha biznes Layer'lari (Data, Context, Indicator, Strategy, Signal, AI, Decision, Risk, Execution, Monitoring, Database, Platform) tomonidan foydalaniladigan umumiy xizmatlardir; ularni bitta qat'iy biznes pipeline bosqichi sifatida (masalan, faqat Market Memory bilan GoldBot Core orasida) hujjatlashtirish noto'g'ri Layer Position tasvirlaydi va real foydalanish doirasini soxtalashtiradi. Bu qoida `01_Data_Layer/Event_System` guruhida README.md'ning Layer Position'ni "Historical Data + Live Data -> Market Memory -> Event System -> GoldBot Core -> Application Services" qat'iy bosqich sifatida ko'rsatgani, Layer_Contracts.md va Layer_DataFlow.md esa "Source/GoldBot Modules -> Event System Layer -> Target Modules" umumiy modelini belgilagani aniqlanganidan keyin qo'shildi (Major, Runtime Documentation Consistency).

## Runtime Pipeline Rule
```text
Group-level runtime architecture
is the canonical execution order.

Individual module documentation
must not redefine or contradict
the group-level pipeline.

If a conflict exists:
Group-level documentation wins.
Module documentation must be
aligned to the group-level
canonical runtime.

Violation:
→ Critical
```
Sabab: guruh darajasidagi hujjatlar (Group README, Layer_ModuleMap, Layer_Contracts, Layer_SequenceDiagram, Layer_DataFlow) butun guruh bo'yicha kelishilgan yagona Canonical Runtime Pipeline'ni belgilaydi; alohida modul o'z hujjatlarida shu tartibni qayta belgilab, undan farq qiladigan boshqa bir tartib taqdim etsa, bu Runtime Architecture darajasidagi ziddiyat hisoblanadi va Critical toifasiga kiradi (oddiy hujjat nomuvofiqligidan farqli, chunki bu haqiqiy bajarilish tartibiga aloqador). Bu qoida `01_Data_Layer/Providers/ProviderLifecycle` modulida uning o'z README/Contracts/ModuleMap/SequenceDiagram hujjatlari "ProviderFactory -> ProviderLifecycle -> ProviderInterface" tartibini ko'rsatgani, guruh darajasidagi barcha besh Canonical hujjat esa "ProviderFactory -> ProviderInterface -> Concrete Provider -> ProviderLifecycle -> ProviderFlow" tartibini belgilagani aniqlanganidan keyin qo'shildi (Critical, Runtime Architecture). ProviderLifecycle'ning o'z Input Contract'i ("Provider Instance") ham guruh darajasidagi tartibni tasdiqlaydi, chunki Provider Instance faqat Factory+Interface+Concrete implementatsiyadan keyin mavjud bo'ladi.
---
## Context Analysis Order Rule
```text
Analysis modules must not depend on
later analysis modules unless
explicitly approved by Director.

Canonical group pipeline is the
source of truth for execution order.

Violation:
→ Critical
```
Sabab: `03_Context_Layer/AMD` va `03_Context_Layer/Wyckoff` modullarining o'z 4 ta hujjati mos ravishda "Session AMD'dan oldin ishlaydi" va "VolumeProfile Wyckoff'dan oldin ishlaydi" deb ko'rsatgani aniqlangan, holbuki guruh darajasidagi Canonical Pipeline (`MarketStructure -> Liquidity -> OrderBlock -> FairValueGap -> Wyckoff -> AMD -> Session -> Trend -> VolumeProfile -> ContextService`) buning aksini belgilaydi. Director Ruling: AMD Accumulation/Manipulation/Distribution modelini aniqlaydi va Session (vaqt konteksti) buning uchun prerequisite emas; xuddi shunday, VolumeProfile barcha oldingi kontekst natijalaridan foydalanishi mumkin bo'lgan oxirgi analiz moduli bo'lib, Wyckoff VolumeProfile natijasiga bog'liq bo'lmasligi kerak. Har ikkala holatda ham guruh darajasidagi pipeline o'zgarmadi — modul hujjatlari canonical tartibga moslashtirildi (AMD'dan Session dependency, Wyckoff'dan VolumeProfile dependency olib tashlandi). Bu qoida Runtime Pipeline Rule'ni to'ldiradi: u guruh-darajasidagi ziddiyatni umumiy tarzda qamrab oladi, bu qoida esa xususiy holatni — keyingi analiz moduliga bog'liqlik — aniq taqiqlaydi.
---
## Context Ownership Rule
```text
ContextEngine:
Orchestrates only.

ContextService:
Creates the only Canonical
Market Context.

No other module may claim
Market Context ownership.

Violation:
→ Critical
```
Sabab: `03_Context_Layer/ContextEngine/Contracts.md` o'zining README.md hujjati va ContextService'ning egaligi bilan ziddiyatda "✓ Market Context Generation" / Output Contract "Market Context" / "✓ Market Context yaratadi" kabi da'volarni o'z ichiga olgani aniqlangan (ContextEngine/README.md esa aniq: "Yakuniy Market Context obyektini faqat ContextService yaratadi"). Director Ruling: ContextEngine faqat orchestrates, coordinates, executes order, collects outputs, forwards outputs qiladi; Market Context yaratish huquqi faqat ContextService'ga tegishli. ContextEngine/Contracts.md tuzatildi — Market Context yaratish da'volari olib tashlandi va "Context Analysis Results" bilan almashtirildi.
---
## Parallel Execution Rule
```text
Independent analysis modules
that have no data dependency
between each other
must be documented
as parallel runtime branches.

Sequential execution
is used only where
a downstream module
requires upstream output.

Conflict between group-level
Data Flow and Sequence Diagram
on execution topology:
→ Critical
```
Sabab: `04_Indicator_Layer/Layer_DataFlow.md` TrendIndicators, MomentumIndicators, VolatilityIndicators, VolumeIndicators'ni IndicatorEngine'dan parallel fan-out qiladigan, so'ng MarketStructureIndicators'dan oldin fan-in bo'ladigan tarzda ko'rsatgan, holbuki `Layer_SequenceDiagram.md` va `IndicatorEngine/SequenceDiagram.md` bu to'rtta modulni qat'iy ketma-ket (Trend → Momentum → Volatility → Volume) ishga tushiriladigan qilib ko'rsatgan — bu ikki guruh hujjat o'rtasidagi Runtime Architecture darajasidagi ziddiyat (Critical). Director Ruling: Trend/Momentum/Volatility/Volume Indicators bir-birining natijasiga bog'liq emas, shuning uchun parallel execution canonical hisoblanadi (kechikishni kamaytiradi va arxitekturaga mos keladi); MarketStructureIndicators/SmartMoneyIndicators/CustomIndicators esa avvalgi natijalarni birlashtirgani uchun ketma-ket qoladi. `Layer_DataFlow.md` Canonical Source sifatida qabul qilindi; `Layer_SequenceDiagram.md` va `IndicatorEngine/SequenceDiagram.md` parallel-fan-out/Synchronization-Point modeliga moslashtirildi. Bu qoida keyingi Layerlardagi (masalan AI, Risk, Media) o'zaro bog'liq bo'lmagan parallel modullar uchun ham qo'llaniladi.
---
## Strategy Execution Rule
```text
StrategyLibrary modules
implement strategy algorithms.

StrategyEngine
is the only runtime executor
and owner of
Strategy Result.

StrategyLibrary modules
must never claim ownership
of the final Strategy Result.

Violation:
→ Critical
```
Sabab: `05_Strategy_Layer`ning barcha 7 ta StrategyLibrary modulida (AMD, Breakout, ICT, LiquiditySweep, MeanReversion, SMC, TrendFollowing, Wyckoff) o'z 4 ta hujjati "Strategy Result yaratadi" va natijani to'g'ridan-to'g'ri StrategyManager'ga uzatadi deb ko'rsatgani aniqlangan, holbuki StrategyEngine'ning o'z hujjatlari xuddi shu "Strategy Execution"/"Strategy Result Aggregation" huquqini yagona egasi sifatida da'vo qilgan va guruh darajasidagi `Layer_DataFlow.md`/`Layer_SequenceDiagram.md` StrategyEngine'ni (StrategyManager emas) context'ni iste'mol qiluvchi ijro modul sifatida ko'rsatgan — bu Runtime Ownership Overlap va Runtime Pipeline ziddiyati (Critical). Director Ruling: Option A tasdiqlandi — StrategyEngine yagona Strategy Execution va Strategy Result egasi hisoblanadi; StrategyLibrary modullari esa strategiya implementatsiyasi (algorithm definitions) bo'lib, faqat Execution Output/Candidate Output yaratadi va uni StrategyEngine'ga uzatadi (StrategyManager'ga emas). Barcha 7 StrategyLibrary modulining 4 tadan hujjati va StrategyEngine'ning o'z hujjatlari shu modelga moslashtirildi (StrategyEngine endi StrategyLibrary algoritmini bevosita chaqiradi).
---
## Algorithm vs Runtime Rule
```text
Algorithm Modules
define how a computation
is performed.

Runtime Engines
own execution,
coordination,
aggregation,
and final outputs.
```
Sabab: Strategy Execution Rule bilan bir vaqtda qo'shildi — u xususiy holatni (Strategy Layer) taqiqlaydi, bu qoida esa umumiy tamoyilni belgilaydi: algoritm/qoida ta'riflovchi modullar (masalan, StrategyLibrary strategiyalari) hech qachon runtime execution, coordination, aggregation yoki final output egaligini da'vo qilmasligi kerak — bu huquq har doim shu turdagi modullarni boshqaruvchi Runtime Engine'ga (masalan, StrategyEngine) tegishli. Bu tamoyil keyinchalik AI, Signal va Media Layerlarida ham xuddi shunday arxitektura standarti sifatida qo'llaniladi.
---
## AI Sequential Processing Rule
```text
AI context enriches
stage by stage.

AI Layer's Internal Modules
(PersonalAI, KnowledgeAI,
FundamentalAI, VisionAI, VoiceAI,
ExplanationAI, ConfidenceAI)
execute in strict sequential
order, not in parallel.

Group-level Data Flow and
Sequence Diagram must agree
on this sequential order.

Violation:
→ Critical
```
Sabab: `07_AI_Layer/Layer_DataFlow.md` PersonalAI/KnowledgeAI/VoiceAI'ni AICoordinator'dan parallel fan-out qiladigan qilib ko'rsatgan, holbuki `Layer_SequenceDiagram.md` va `AICoordinator/SequenceDiagram.md` bu modullarni qat'iy ketma-ket ishga tushiradigan qilib ko'rsatgan (Critical, Runtime Architecture). Director Ruling: sequential pipeline canonical hisoblanadi, chunki AI context bosqichma-bosqich boyib boradi (`PersonalAI → KnowledgeAI → FundamentalAI → VisionAI → VoiceAI → ExplanationAI → ConfidenceAI → AICoordinator`) — har bir keyingi modul avvalgi modullar to'plagan kontekstdan foydalanadi. `Layer_DataFlow.md` parallel ko'rinishidan voz kechildi va `Layer_SequenceDiagram.md`ning qat'iy ketma-ket modeliga moslashtirildi.
---
## Layer Direction Rule
```text
Lower layer modules
must never depend on
their own orchestrator.

AIEngine
↓
PersonalAI

never

PersonalAI
↓
AIEngine
```
Sabab: `07_AI_Layer/PersonalAI/InteractionManager`, `Senior`, va `Seniorita` o'z Allowed Dependencies ro'yxatida `AIEngine`'ni ko'rsatgan, holbuki guruh darajasidagi Contracts.md'ga ko'ra AIEngine PersonalAI'ning ustidagi orchestrator hisoblanadi (`AIEngine → PersonalAI`) — bu Circular Dependency naqshi (Critical, Runtime Ownership), chunki hech bir modul o'z chaqiruvchisiga (orchestrator) qarab dependency qila olmaydi. Director Ruling: uchala modulning ham Allowed Dependencies ro'yxatidan AIEngine olib tashlandi — bu qoida umumiy tamoyil sifatida qayd etildi: pastki (child) layer/modul hech qachon o'zini boshqaruvchi yuqori orchestrator'ga dependency qilmaydi, aloqa faqat yuqoridan pastga (orchestrator → child) yo'nalishida bo'ladi.
---
## Knowledge Lifecycle Rule
```text
KnowledgeManager
↓
KnowledgeBase
↓
MemorySearch
↓
MemoryManager
↓
PersonalKnowledge
↓
SystemKnowledge
↓
RAG
↓
ProviderRouter
↓
ValidationEngine
↓
LearningEngine
↓
Knowledge Context

KnowledgeManager and KnowledgeBase
must be ready before any other
KnowledgeAI sub-module can function.
```
Sabab: `07_AI_Layer/KnowledgeAI`'ning guruh darajasidagi Canonical Sequence hujjati KnowledgeManager va KnowledgeBase'ni butunlay tashlab qo'ygan (Internal Modules ro'yxatida bo'lsa-da), individual sub-modullar esa bir-biriga zid ikkinchi bir lifecycle zanjirini tasvirlagan (Critical, Runtime Pipeline). Director Ruling: yuqoridagi 11 bosqichli chiziqli pipeline canonical deb belgilandi — KnowledgeManager va KnowledgeBase avval tayyor bo'lmasa, qolgan modullar ishlay olmaydi; MemorySearch bazadan qidiradi; MemoryManager natijani boshqaradi; RAG valid knowledge yig'adi; Validation tekshiradi; Learning oxirida feedback qiladi. Guruh va barcha 9 sub-modul (KnowledgeManager, KnowledgeBase, MemorySearch, MemoryManager, PersonalKnowledge, SystemKnowledge, RAG, ProviderRouter, ValidationEngine, LearningEngine) shu pipeline'ga moslashtirildi.
---
## Command Interpretation Rule
```text
SpeechToText
only produces text.

Command interpretation
is exclusively
VoiceCommands' responsibility.

WakeWord
↓
SpeechToText
↓
VoiceCommands
↓
InteractionManager
```
Sabab: `07_AI_Layer/VoiceAI`ning guruh darajasidagi hujjatlari VoiceCommands'ni Internal Module sifatida ro'yxatga olgan, ammo o'z Workflow/SequenceDiagram'ida hech qachon chaqirmagan; `SpeechToText`ning o'z hujjatlari ham to'g'ridan-to'g'ri InteractionManager'ga o'tib ketgan, holbuki `VoiceCommands`ning o'z hujjatlari o'zini SpeechToText bilan InteractionManager orasida majburiy bosqich sifatida ko'rsatgan (Critical, Runtime Pipeline). Director Ruling: VoiceCommands haqiqiy pipeline stage hisoblanadi va hech qachon tashlab yuborilmaydi — canonical tartib `WakeWord → SpeechToText → VoiceCommands → InteractionManager`. SpeechToText faqat matn yaratadi; ovozli buyruqni talqin qilish (Command Interpretation) faqat VoiceCommands vazifasi. VoiceAI guruh hujjatlari va SpeechToText'ning barcha hujjatlari shu tartibga moslashtirildi.
---
## Execution Ownership Rule
```text
BrokerGateway owns
Broker Execution Response.

ExecutionMonitor owns
Execution Result.

ExecutionEngine
owns execution orchestration only.

Violation:
→ Critical
```
Sabab: `10_Execution_Layer`da uchta modul — ExecutionEngine, BrokerGateway va ExecutionMonitor — mustaqil ravishda "Execution Result" nomli obyektni o'zining Output sifatida da'vo qilgani aniqlangan (ExecutionEngine va BrokerGateway'ning Output Contract'lari, ExecutionService'ning Input Contract'i esa buni ExecutionMonitor'dan qabul qilinadi deb ko'rsatgan, holbuki ExecutionMonitor'ning o'z Output Contract'ida bu umuman yo'q edi) — uchta manba, uchta ziddiyatli da'vo (Critical, Runtime Ownership). Director Ruling: ExecutionMonitor Execution Result'ning yagona Canonical egasi hisoblanadi; BrokerGateway faqat "Broker Execution Response" yaratadi (hech qachon "Execution Result" emas); ExecutionEngine faqat execution orchestration bilan shug'ullanadi va o'z Output'ini "Execution Plan"/"Execution Context" deb ataydi. Barcha uch modulning README/Contracts hujjatlari shu modelga moslashtirildi.
---
## Risk Policy Rule
```text
Risk Layer
produces Risk Policy.

Trade Monitoring
may execute only
actions allowed
by Risk Policy.

Trade Monitoring
must never
recalculate risk.

Violation:
→ Critical
```
Sabab: `11_Trade_Monitoring_Layer`da BreakevenManager, TrailingStop va PartialClose ochiq Position'ning Stop Loss/hajmini bevosita o'zgartiradi, ammo barchasi Risk Layer'ni Forbidden Dependency sifatida ko'rsatgan va hech qanday Risk Manager tekshiruvi hujjatlashtirilmagan edi — bu CLAUDE.md'ning "Never bypass Risk Manager" qoidasiga zid ko'rinardi (Critical, Trading Safety). Director Ruling: Risk Layer bypass qilinmaydi, lekin Trade ochilgandan keyingi Breakeven/Trailing Stop/Partial Close harakatlari yangi risk hisoblash emas, balki Trade Management hisoblanadi — shuning uchun ular Risk Layer'ga to'g'ridan-to'g'ri dependency olmaydi. Buning o'rniga: Trade ochilish vaqtida Risk Layer "Risk Policy" (masalan, Allow BE / Allow Trailing / Allow Partial Close / Max Partial % / Trailing Rules / BreakEven Rules) ishlab chiqaradi va bu Risk Policy Execution natijasi bilan birga Trade Monitoring Layer'ga uzatiladi; Trade Monitoring shu Policy doirasida ishlaydi va hech qachon risk'ni qayta hisoblamaydi yoki yangi Risk Manager chaqirmaydi. Shu tarzda Risk Manager trade ochilishida bir marta qaror qiladi, Monitoring esa faqat o'sha qarorni bajaradi — CLAUDE.md qoidasi buzilmaydi.
---
## Platform Gateway Rule
```text
PlatformService is the
sole entry point
to GoldBot Core services.

PlatformService is NOT
the Platform Layer's
external entry point.

Client channels
(Telegram/Mobile/Web/Desktop)
+ Authentication
are the actual
external entry points.
```
Sabab: `13_Platform_Layer/PlatformService`ning o'z hujjatlari (README Golden Rule 1, Contracts Runtime Contract 1) "Platform Layer'ga barcha tashqi kirishlar PlatformService orqali amalga oshiriladi" deb da'vo qilgan, holbuki guruh darajasidagi Canonical Pipeline'da haqiqiy tashqi kirish nuqtasi mijoz kanallari (Telegram/MobileAPI/WebAPI/DesktopAPI) va Authentication bo'lib, ular PlatformService'dan oldin keladi (Critical, Ownership Scope). Director Ruling: Worker to'g'ri topgan — PlatformService Platform Layer'ning emas, balki GoldBot Core xizmatlarining yagona gateway'i hisoblanadi. PlatformService'ning matni "PlatformService is the sole entry point to GoldBot Core services" deb aniqlashtirildi.
---
## Chart Shared State Rule
```text
Chart modules
communicate through
Chart State
and
Render State.

Modules do not
pass ownership
objects through
a strict pipeline.
```
Sabab: Chart Layer audit'ida Objects (Critical) Drawing_Tools/Indicators/Analysis_Overlay'ning Output'ini — bu modullar Objects'dan keyin ishlaydigan bo'lsa ham — o'zining Input'i sifatida hujjatlashtirgan; xuddi shunday Chart_Renderer "Object List"ni Input deb ko'rsatgan, holbuki Renderer Objects'dan oldin joylashgan edi. Sabab — 20-modulli Chart Layer strict linear token-passing Pipeline sifatida hujjatlashtirilgan, lekin haqiqiy vizual modullar (Objects, Drawing_Tools, Indicators, Analysis_Overlay, Chart_Renderer) markazlashgan holat orqali ishlaydi, ketma-ket Input→Output zanjiri orqali emas. Director Ruling (Option 1): Chart modullari bir-birining Output'ini to'g'ridan-to'g'ri iste'mol qilmaydi — Chart State/Render State orqali muloqot qiladi. Bu qoida faqat Chart Layer'ga tegishli; boshqa 15 Layer'ning Input→Output Contract modeli o'zgarmaydi.
---
## Render Loop Rule
```text
Chart Renderer
renders every frame
from the current
Render State.

Renderer does not
consume sequential
module outputs.
```
Sabab: Chart_Renderer'ning Module Boundary'si avval "Chart_Data → Chart_Renderer → Chart_Interaction" edi va Input'i "Object List"ni o'z ichiga olgan — bu Objects modulining Output'i bo'lib, Objects Renderer'dan keyin joylashgan (Critical, Runtime Pipeline Rule). Director Ruling (Option 1): Chart_Renderer pipeline'ning "bir bosqichi" emas — u har frame joriy Shared Render State'ni o'qib chizadigan Render Loop. Screenshot va Alerts ham xuddi shunday — ular ketma-ket oldingi modul Output'ini emas, Chart_Renderer/Render State/Chart State'ning joriy holatini kuzatadi (watch). Batafsil qoidalar: `16_Chart_Layer/Rendering_Guide.md` (Canonical Rendering Source).
---
## Chart Runtime Rule
```text
Layer_DataFlow
represents
execution order.

It is not a
token-passing
ownership chain.
```
Sabab: Chart Layer'ning guruh darajasidagi hujjatlari (`README.md` Chart Runtime, `Layer_DataFlow.md`, `Layer_SequenceDiagram.md`, `Layer_Contracts.md`) 20 modulni bitta chiziqli zanjir sifatida tasvirlagan, bu esa Objects/Chart_Renderer/Screenshot kabi modullarning haqiqiy Input/Output Contract'lari bilan mos kelmagan (Chart Shared State Rule va Render Loop Rule'ga qarang). Director Ruling (Option 1 — Orchestrated Shared-State Architecture): bu 4 ta hujjatdagi ketma-ketlik endi faqat **Execution/Processing Order** sifatida talqin qilinadi, Input→Output ownership zanjiri sifatida emas. "Pipeline" so'zi shu ma'noda ishlatilmaydi — "Chart Execution Flow" yoki "Chart Processing Order" ishlatiladi. Chart_API Chart Layer'ning yagona Entry HAM Exit nuqtasi bo'lib qoladi (o'zgarmagan).
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
