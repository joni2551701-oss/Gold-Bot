# Architecture Audit Plan
Status: CANONICAL
---
# Purpose
Ushbu hujjat GoldBot Canonical Architecture uchun rasmiy Audit Metodologiyasini belgilaydi.
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
Audit boshlanganidan (Layer Audit) to Final Report yakunlanguncha, Canonical Architecture'ga o'zgartirish kiritish taqiqlanadi.
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
## Canonical Event Bus Rule
```text
Event_System
(01_Data_Layer)
is the single
Canonical Event Bus
for all 16 Layers.

Layers communicate
asynchronously only
through Event_System —
no Layer creates
its own separate
Event Bus.
```
Sabab: Architecture Gap Review v1.0 §6 topdiki, to'liq Event Bus infratuzilmasi (EventBus, EventDispatcher, EventLifecycle, EventPublisher, EventService, EventSubscriber) mavjud, lekin u faqat `01_Data_Layer/Event_System` ichida hujjatlashtirilgan va boshqa Layerlar (Chart_API'ning "Event API"si, Trade Monitoring, Platform) unga rasman bog'lanmagan — Event Bus'ning butun tizim uchun yagona ekanligi hech qayerda aniq yozilmagan edi. Director Decision: yangi modul kerak emas — mavjud Event_System butun GoldBot uchun Canonical Event Bus deb rasman e'lon qilindi (`01_Data_Layer/README.md` Golden Rule 11, `Layer_Contracts.md` Layer Rule 11, `Layer_DataFlow.md` Event Flow bo'limida hujjatlashtirildi).
---
## Backtesting Isolation Rule
```text
Backtesting Layer
must be fully
isolated from the
real trading
infrastructure.

It only simulates
the behaviour of
existing Layers and
never works directly
with a real Broker,
Platform, or
Trade Execution.
```
Sabab: Architecture Gap Review v1.0 §1/§14 topdiki, `backtesting/` paketi katta hajmdagi real implementatsiyaga ega (BacktestEngine, ReplayEngine, ReplayController, DataFeed, BacktestResult) bo'lsa-da, Canonical Architecture'da unga mos hech qanday Layer yoki modul mavjud emas edi. Director Decision: yangi `17_Backtesting_Layer` qo'shildi (16-raqam `16_Chart_Layer` tomonidan band). Rule quyidagilarni majburlaydi: (1) Backtesting hech qachon Live Trading qilmaydi va Broker bilan ulanmaydi; (2) Backtesting Risk Manager'ni hech qachon chetlab o'tmaydi — har bir tasdiqlangan Decision majburiy ravishda Risk Layer'dan o'tadi (CLAUDE.md "Never bypass Risk Manager" qoidasiga mos); (3) Backtesting Decision Layer'ni almashtirmaydi va hech qanday trading mantiqini qayta yozmaydi — faqat mavjud Layer'larni o'zgartirmasdan chaqiradi; (4) `Execution (Simulated)` va `Trade Monitoring (Simulated)` bosqichlari `11_Trade_Monitoring_Layer/PaperTrading` orqali bajariladi — Module Reuse Principle bo'yicha Backtesting Layer o'zining alohida simulyatsiya moduli yaratmaydi.
Tasdiq: haqiqiy `backtesting/backtest_engine.py` importlari ushbu qoidaga allaqachon mos — u `risk.risk_manager.RiskManager`ni chaqiradi va `execution/` yoki biror Broker mijozini umuman import qilmaydi.
---
## Module Reuse Rule
```text
If an existing module
can perform a new
responsibility without
breaking the
architecture, creating
a new module for that
same function is
forbidden.

Duplicate ownership
and duplicate runtime
are strictly
prohibited.
```
Sabab: `17_Backtesting_Layer` qurilishida Director'ning Canonical Pipeline'i `Execution (Simulated)` va `Trade Monitoring (Simulated)` bosqichlarini nomlagan edi, bu esa `SimulatedExecution` va `SimulatedMonitoring` degan ikkita yangi modul yaratishga olib kelishi mumkin edi. Tekshiruv shuni ko'rsatdiki, `11_Trade_Monitoring_Layer/PaperTrading` allaqachon virtual order, virtual position, virtual lifecycle va virtual monitoring vazifalarini bajaradi — va haqiqiy `backtesting/backtest_engine.py` aynan `lifecycle/paper_trade.py` bilan `lifecycle/paper_trade_monitor.py`ni import qiladi. Director Ruling: yangi modullar yaratilmaydi, Backtesting Layer PaperTrading'ni qayta ishlatadi. Bu qoida CLAUDE.md'dagi Module Reuse Principle'ni ACR darajasiga ko'taradi va keyingi barcha Layer'larda qo'llaniladi: yangi modul yaratishdan oldin (1) bu vazifa allaqachon mavjudmi, (2) mavjud modulni contract'ini buzmasdan kengaytirish mumkinmi — degan savollarga javob berilishi shart; faqat ikkalasi ham "yo'q" bo'lgandagina yangi modul yaratiladi.
---
## Worker Decision Rule (WDR-001)
```text
If a question is
unambiguously resolved
by existing Director
decisions, ACRs, and
the Canonical
Architecture, the
Worker does not ask
the Director again.

The Worker decides
independently,
implements it, and
records it briefly in
the final report.
```
Director Review faqat quyidagilar uchun talab qilinadi:
* Yangi Layer
* Yangi Public API
* Ownership almashishi
* Runtime Pipeline o'zgarishi
* Security Architecture
* Trading Safety
* Database Architecture
* Chart Engine Architecture
* Foundation Freeze
* Version Freeze

Worker Director Review'siz mustaqil bajaradigan ishlar:
1. Gap Review xulosalarini kodga qarab o'zi tuzatish (masalan "Secrets yo'q" xulosasi noto'g'ri ekanligini aniqlab, Gap Review/Tracker/hujjatni yangilash).
2. Mavjud kodni Canonical Architecture bilan bog'lash (mapping), masalan `core/secrets.py` → `02_Core_Layer/Secrets`.
3. Refactoring TODO yaratish (masalan `config.py` → `Secrets`ga ko'chirish).
4. Legacy kodni Blueprint'ga moslashtirish (masalan `MaskedSecret` → `SecretRegistry`, `ProviderAdapter` → `VoiceProvider`).
5. Hujjatni real kod asosida boyitish (kodda bor, README'da yo'q bo'lgan komponentni qo'shish).
6. Yangi modul qo'shilganda Golden Rule'ni tabiiy ravishda kengaytirish.
7. Layer Flow tartibini tuzatish — agar ownership o'zgarmasa (masalan `Startup → Secrets → Configuration`).
8. Submodule yaratish (masalan `SecretRotation`, `SecretRegistry`, `SecretValidator`).
9. Real kodni tahlil qilib duplicate/dead code/unused/inconsistent holatlarni topish va hisobot qilish.
10. Blueprint'ni koddan oldinda yuritish — Blueprint doim oldinda, kod keyin unga moslashtiriladi.
11. Refactoring Note yozish (implementatsiya vaqtida nima ko'chishini qayd etish).
12. Critical bo'lmagan Canonical Gap'ni "Known Gap" deb belgilash.
13. Mavjud kod ACR'ga allaqachon mos ekanligini tekshirib "Verified" deb belgilash.
14. Mavjud ACR asosida "yangi modul kerak emas" degan xulosaga kelish (Module Reuse Rule).
15. Roadmap, Tracker, Progress va Commit summary'ni yangilash.

Sabab: Phase 2 Module Audit va Architecture Gap Review v1.0 davomida Worker'ning har bir aniq-ravshan qaror uchun Director'dan qayta ruxsat so'rashi jarayonni sekinlashtirdi, holbuki qarorlarning katta qismi mavjud ACR'lar va Canonical Architecture asosida bir ma'noli hal qilinardi. Director Ruling: WDR-001 bilan Director review'lar soni taxminan 80–90% ga kamayadi, arxitektura nazorati esa yuqoridagi 10 ta toifada to'liq saqlanib qoladi.
---
## Repository Aggregation Rule (RAR-001)
```text
The number of
repositories in the
Database Layer need
not equal the number
of business objects.

Multiple storage
implementations within
one domain are
documented as the
internal responsibility
of a single Repository
module.
```
Sabab: Architecture Gap Review v1.0'ning KG-002 topilmasi — `12_Database_Layer` 5 ta repository hujjatlashtirgan, real kodda esa 16 ta storage implementatsiyasi mavjud (`admin, audit_log, config_snapshot, emergency, feedback, learning, market_snapshot, monitoring, raw_candle, risk_decision, risk_state, runtime_feature, signal, subscription, sync_state, user`). Director uchta variantni ko'rib chiqdi: (1) har birini alohida modul qilish — ortiqcha fragmentatsiya sababli rad etildi; (3) Freeze'dan keyinga qoldirish — Foundation Freeze'dan keyin Database arxitekturasini o'zgartirish noto'g'ri bo'lgani uchun rad etildi; (2) domen bo'yicha guruhlash — **tasdiqlandi**. Guruhlash real kod mas'uliyatiga qarab Worker tomonidan aniqlandi:
* **UserRepository** (foydalanuvchi va hisob) — `user`, `subscription`, `feedback`, `admin`
* **TradeRepository** (savdo va risk) — `signal`, `risk_decision`, `risk_state`, `emergency`
* **MarketRepository** (market ma'lumot) — `market_snapshot`, `raw_candle`, `sync_state`
* **JournalRepository** (AI Journal va tizim holati) — `learning`, `config_snapshot`, `runtime_feature`
* **AuditLog** (audit va kuzatuv) — `audit_log`, `monitoring`

Guruhlash asoslari: `admin` — `AdminRecord(telegram_id, role)`, ya'ni hisob domeni; `emergency` — `EmergencyStateEntry(state, reason, source)`, ya'ni Trading Safety domeni; `runtime_feature` — `RuntimeFeatureRecord(feature, enabled, updated_by)`, ya'ni tizim holati (upsert), shuning uchun append-only AuditLog'ga emas, JournalRepository'ga kiritildi. Yangi storage qo'shilganda u mos domendagi mavjud Repository ichiga kiritiladi — yangi Repository moduli yaratilmaydi.
---
## Migration Isolation Rule (MIR-001)
```text
Each migration commit
is limited to one
module or one small
subsystem.

No commit migrates
several Layers or a
large bulk move at
once.
```
Sabab: Director Order No. 002 — Migration Strategy. `goldbot-v1` branchi bir vaqtning o'zida ham implementatsiya, ham migratsiya branchi hisoblanadi. Agar 1000+ import, 5400 test va yuzlab fayl birdaniga ko'chirilsa: xato qayerdan chiqqanini aniqlash qiyinlashadi, git history shovqinli bo'ladi va rollback murakkablashadi. Kichik commitlar `git diff`ni kichik saqlaydi, rollback'ni osonlashtiradi va testdagi xatoni tez topishga imkon beradi.
---
## Import Compatibility Rule (ICR-001)
```text
During migration old
imports may keep
working and
compatibility wrappers
may be created.

The Foundation Freeze
architecture itself
does not change.
```
Sabab: Director Order No. 002. Migratsiya bosqichma-bosqich bo'lgani uchun, ko'chirilmagan modullar eski top-level paketlardan ishlashda davom etadi. Wrapper'lar vaqtinchalik ko'prik vazifasini bajaradi — ular Canonical Contract, Ownership yoki Runtime Pipeline'ni o'zgartirmaydi va Phase E (Cleanup) davomida olib tashlanadi.
---
## Migration Validation Rule (MVR-001)
```text
After every module
migration the following
must be performed:

- import check
- unit tests
- old vs new namespace
  parity check (if the
  module is already in
  use)
- commit
```
Sabab: Director Order No. 002 (Phase B). MIR-001 migratsiyani kichik bo'laklarga ajratadi, MVR-001 esa har bir bo'lakning to'g'riligini kafolatlaydi. Worker ushbu qoidani Director'siz mustaqil qo'llaydi. Amalda bu GoldBot'ning mavjud Commit Protocol'i bilan birlashadi: `git add -A` → `pyflakes` → `compileall` → `pytest` → `python main.py` → toza `git status` → commit.
---
## Stable Migration Rule (SMR-001)
```text
If an existing module
works and matches the
architecture, its
internal structure is
not changed during
migration.

Internal refactoring
happens only after the
migration is complete.
```
Sabab: Phase B.2 (Secrets). `core/secrets.py` toza ko'chdi, lekin `config.py` (471 qator, 29 ta importer) Configuration va Secrets domenlarini aralashtiradi — `Settings` bloklari bilan `MaskedSecret` bir faylda. Uni migratsiya davomida ikkiga bo'lish bitta commit ichida migratsiya, refactoring va import o'zgarishini aralashtirardi, bu esa MIR-001'ga zid. Director Decision: hozirgi maqsad **Migration Stability**, Architecture Refactoring emas. `config.py` migratsiya yakunlanguncha o'z holicha qoladi; KG-001 / RT-001 / RT-002 bo'yicha ajratish Phase E'dan keyin yoki Implementation v1.1'da bajariladi.
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

Phase 1 — Layer Audit tartibi (repository root'idagi haqiqiy papka nomlari bo'yicha):
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

---
# 11. Worker Authority Registry (WAR)

Director Order No. 003. Har bir Director qarori bir marta tasdiqlanadi va Worker uni keyingi ishlarida avtomatik qo'llaydi — qayta ruxsat so'ralmaydi (WDR-001'ning kengaytmasi).

## WAR-001 — Auto Fix Authority
Worker Director'siz bajaradi:
* Typo, formatting, markdown fix
* README va broken link tuzatish
* Dependency Source of Truth moslashtirish
* Allowed/Forbidden ro'yxatlarini moslashtirish
* Canonical Naming
* Import update
* Wrapper qo'shish/olib tashlash (ruxsat berilgan holatlarda)
* Test update (arxitekturani o'zgartirmasa)
* ACR raqamlash
* Tracker update

## WAR-002 — Migration Authority
Worker mustaqil bajaradi:
* `git mv`
* Papka yaratish
* Namespace o'zgartirish
* `__init__.py` yozish va package export sozlash
* README havolalari
* Import migration
* Skeleton yaratish

## WAR-003 — Documentation Authority
Worker README, Contracts, ModuleMap va SequenceDiagram orasidagi oddiy nomuvofiqliklarni o'zi tuzatadi.

## WAR-004 — Validation Authority
Har commitdan keyin avtomatik: `pyflakes` · `compileall` · `pytest` · `python main.py` · `git diff` · import check.

## WAR-005 — Refactoring Restriction
Worker quyidagilarni **qilmaydi** — Director Review talab qilinadi:
* Modulni bo'lish
* Ownership o'zgartirish
* Runtime Pipeline o'zgartirish
* Layer qo'shish
* Public API o'zgartirish

## WAR-006 — Decision Memory
Har bir Director qarori eslab qolinadi. Worker qayta "ruxsat berasizmi?" deb so'ramaydi — mavjud qoidaga havola qilib davom etadi, masalan: "SMR-001 bo'yicha modul bo'linmaydi, shuning uchun faqat migratsiya qilindi."

Amaldagi qoidalar: MIR-001 · ICR-001 · MVR-001 · SMR-001 · WDR-001 · RAR-001 va §9b dagi barcha ACR'lar.

## WAR-008 — Repository Infrastructure Rule
Worker quyidagilarni **Repository Infrastructure** deb qabul qiladi va Director ruxsatisiz ularning joylashuvini o'zgartirmaydi:
`.github/` · `tests/` · `docs/` · `scripts/` · `deploy/` · `assets/` · `logs/` · `requirements*.txt` · `Dockerfile` · `docker-compose.yml` · `CLAUDE.md`

Ularni ko'chirish yoki qayta tashkil qilish alohida Director qarorini talab qiladi.

## WAR-009 — Stable Package Rule
Agar mavjud package ishlayotgan bo'lsa, ichki importlari murakkab bo'lsa va testlar yashil bo'lsa — Worker migratsiya vaqtida uni ichidan bo'lmaydi. Faqat `git mv` qiladi. Ichki refactoring faqat **Phase F** da bajariladi.

## WAR-010 — Natural Layer Order
Migratsiya Layer dependency tartibida davom etadi — bu importlar va bog'liqliklarni eng kam buzadi:
```text
data_layer → context_layer → indicator_layer → strategy_layer → signal_layer →
ai_layer → decision_layer → risk_layer → execution_layer → trade_monitoring_layer →
database_layer → platform_layer → media_layer → chart_layer → backtesting_layer
```

## WAR-007 — Escalation Rule
Faqat quyidagilar Director Review'ga chiqadi:
* Yangi Layer
* Yangi Modul
* Ownership o'zgarishi
* Runtime Pipeline
* Security Boundary
* Public API
* Architectural Pattern
* Canonical Rule

Qolgan hamma narsa avtomatik bajariladi.

---
# 12. Repository Structure (Director Order No. 003)

Foundation Freeze v1.0 tasdiqlanganidan boshlab kuchga kiradi.

## 12.1 Canonical Architecture
Foundation Freeze v1.0 = GoldBot v1. `goldbot-v1` branchining asosiy tuzilmasi aynan Freeze'da tasdiqlangan arxitektura hisoblanadi. Worker bundan keyin barcha qarorlarini shu asosda qabul qiladi.

## 12.2 Repository Root — Canonical tarkib
```text
01_Data_Layer/ … 17_Backtesting_Layer/
ARCHITECTURE.md
FOUNDATION_FREEZE_V1.md
Architecture_Audit_Plan.md
Architecture_Audit_Tracker.md
README.md
MIGRATION_TRACKER.md
                     (Canonical implementatsiya namespace'i — Phase A.5'da tasdiqlangan)
```

## 12.3 Foundation Freeze tarkibiga KIRMAYDI
* Vaqtinchalik papkalar
* Eski experiment branch fayllari
* Audit davomida ishlatilgan yordamchi fayllar
* Duplicate hujjatlar
* Keraksiz migration artefaktlari

## 12.4 Eski implementatsiya
`core/`, `data/`, `ai/`, `execution/` va boshqa pre-freeze paketlar Foundation Freeze arxitekturasi **emas**. Ular faqat migratsiya tugaguncha implementatsiya manbai sifatida mavjud bo'ladi va bosqichma-bosqich o'z Layer papkasiga ko'chiriladi (Phase B-E).

## 12.5 Loyiha infratuzilmasi — RESOLVED (Deferred to Phase E)
Quyidagilar arxitektura hujjati ham, pre-freeze implementatsiya ham emas: `main.py`, `config.py`, `tests/`, `docs/`, `contracts/`, `scripts/`, `deploy/`, `assets/`, `logs/`, `requirements*.txt`, `Dockerfile`, `docker-compose.yml`, `.github/`, `.gitignore`, `.env.example`, `.env.production`, `CLAUDE.md`. Ular **Repository Infrastructure** hisoblanadi va hozir ko'chirilmaydi ham, o'chirilmaydi ham (WAR-008).

Director Decision: Phase E — Cleanup davomida ular uchta toifaga ajratiladi:
1. **Repository Infrastructure (saqlanadi)** — `.github/`, `tests/`, `docs/`, `scripts/`, `Dockerfile`, `requirements*.txt` va shu kabilar.
2. **Application Implementation** — tegishli Layer papkasi ichiga ko'chadigan kod.
3. **Legacy** — migratsiya tugagach olib tashlanadigan eski paketlar.

## 12.6 Worker vakolati
Ruxsat: ortiqcha vaqtinchalik hujjatlarni olib tashlash · duplicate fayllarni yo'qotish · README havolalarini yangilash · migratsiya trackerini yangilash.
Taqiqlanadi: Foundation Freeze tarkibini o'zgartirish · yangi Layer qo'shish · yangi Modul qo'shish · Canonical hujjatlarni Director tasdiqisiz o'zgartirish.

---
# 13. Migration Mission (Director Order No. 006)

Foundation Freeze v1.0 yakunlandi. Loyiha Architecture Design bosqichidan **Implementation Migration** bosqichiga o'tdi. Yagona maqsad: Canonical Architecture va Real Implementation bir xil bo'lishi.

## 13.1 Single Source of Truth Rule
Har bir Layer o'zining Architecture, Documentation, Contracts, Python Code va Tests uchun yagona Source of Truth hisoblanadi. Kod va hujjat hech qachon ikki xil joyda parallel yashamaydi.

## 13.2 Migration Phases
| Phase | Qamrov | Holat |
|---|---|---|
| A | Layer nomlarini yakuniy standartga o'tkazish | ✅ |
| B | `goldbot/` temporary namespace'ni yo'q qilish | ✅ |
| C | Eski paketlarni (`core/`, `data/`, `ai/` …) `git mv` orqali Layer ichiga ko'chirish, history saqlanadi | 🔄 |
| D | Importlarni yangilash | 🔄 |
| E | Cleanup — duplicate/dead code, bo'sh papka, buzuq import va hujjat; eski paketlar to'liq olib tashlanadi | ⏳ |
| F | Final Audit — missing docs, broken imports/contracts, dependency/ownership/gateway/runtime/canonical violations, duplicate logic | ⏳ |
| G | Architecture Lock — GoldBot v1 | ⏳ |

## 13.3 Migration Principles (har bir commitda tekshiriladi)
1. Bu migratsiya Canonical Architecture'ga yaqinlashtiryaptimi?
2. Bu keyinchalik ikkinchi marta ko'chirishga majbur qilmaydimi?
3. Bu Layer ichida hujjat va kodni birlashtiryaptimi?
4. Bu Source of Truth'ni yaxshilayaptimi?

Bittasiga javob "yo'q" bo'lsa — Worker to'xtaydi va Director Review so'raydi.

## 13.4 Execution Mode — AUTONOMOUS
Worker mavjud WAR/WDR/MIR/MVR/ICR/SMR/RAR qoidalari va Director Order'lar asosida mustaqil ishlaydi. Director faqat quyidagilarda jalb qilinadi: yangi Layer qo'shish/olib tashlash · Canonical Module qo'shish/olib tashlash · Ownership o'zgarishi · Runtime Pipeline o'zgarishi · Public API o'zgarishi · Decision/Risk Engine logikasi · Trading Logic · Security Boundary · Foundation Freeze qoidalarini o'zgartirish · Canonical Architecture o'zgarishi.

## 13.5 Final Success Criteria
✅ Repository to'liq Layer Architecture asosida ishlaydi · ✅ Har bir Layer ichida hujjat va kod birga · ✅ `goldbot/` yo'q · ✅ Eski paketlar olib tashlangan · ✅ Importlar 100% yangi strukturada · ✅ Testlar yashil · ✅ Duplicate logic yo'q · ✅ Documentation Drift yo'q · ✅ Canonical Architecture = Real Implementation
