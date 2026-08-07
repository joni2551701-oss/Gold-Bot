# Director Decisions — Append-Only Log

This file is the single append-only record of every Director-approved
decision that governs GoldBot's engineering process: Worker Authority
Registry entries (WAR), Worker Decision Rule entries (WDR), Migration
Isolation Rule entries (MIR), Repository Aggregation Rule entries
(RAR), GoldBot Engineering Law entries (GEL), and any other Director
Decision (DD) or numbered Director Order.

Entries are never edited or removed once appended — a superseded
decision gets a new entry that says so explicitly; the old entry stays
for history. Full text/history of most entries pre-dating this file
lives in `Architecture_Audit_Plan.md`; this file is the canonical
home for everything from Director Order No. 016 onward.

## Log

### Director Order No. 016 — Worker Authority Expansion

The Worker becomes System Owner of every module it works on —
responsible for that module's quality, consistency, extensibility and
stability, not only the task at hand. Grants the Worker autonomous
authority (no per-change Director approval needed) over: Autonomous
Bug Fix, Performance Optimization (behavior-preserving), Internal
Refactoring, Documentation Evolution, Test Evolution, Code Quality,
Dependency Cleanup, Module Expansion (Canonical Architecture
preserved), Backlog Management, Continuous Self Review (per-Sprint,
Director gets only the final Consolidated Review), Development
Planning (per-Sprint Task/Risk/Dependency/Estimate), and Autonomous
Root Cause Analysis (ARCA — Problem → Root Cause → Permanent Solution
→ Validation → Lessons Learned; temporary fixes forbidden).

Director Review remains mandatory whenever a change touches: Layer
Architecture, Pipeline, Trading Logic, AI Logic, Decision Logic, Risk
Logic, a public-API breaking change, Ownership, a Canonical Contract,
or a Foundation Rule.

Filing scheme (Director's own recommendation, mapped onto existing
files per the Module Reuse Principle): `ARCHITECTURE.md` for the
unchanging architecture, `CLAUDE.md` for Worker operating rules
(Order No. 016's full text lives there), this file
(`DIRECTOR_DECISIONS.md`) for the append-only decision log, and each
module's own `WORK_LOG.md` for that module's completed work.

Full order text recorded in `CLAUDE.md`'s "Worker Authority — Director
Order No. 016" section.

### Director Order No. 017 — GoldBot Development Standard (GDS)

Establishes the single Development Standard governing how code is
written, tested, refactored, and evolved: GDS-001 Coding Standard
through GDS-011 Code Review Standard, plus Definition of Done (DoD),
Development Workflow (Read → Understand → Design → Implement → Unit
Test → Integration Test → Refactor → Documentation → Validation →
Commit → Push → Review), Risk Assessment (Low/Medium/High/Critical,
High/Critical requiring Director Review), Rollback Strategy (Failure →
Rollback → Restore → Revalidate → Retest → Continue), Module Health
Score (Architecture/Contracts/Documentation/Testing/Performance/
Maintainability/Dependency/Security), Technical Debt Standard (housed
in each module's ROADMAP.md), Dependency Graph Standard (housed in
each module's CONTRACTS.md/MODULE_MAP.md), Module Status Lifecycle
(Blueprint → In Development → Implemented → Testing → Stable →
Deprecated), and an AI Knowledge Base / Lessons Learned standard
(housed in each module's WORK_LOG.md, reusing ARCA's Problem → Root
Cause → Permanent Solution → Lessons Learned structure). GDS
operationalizes existing rules (CLAUDE.md's Commit Protocol and
Trading Safety, GEL-001's doc set, ARCHITECTURE.md's Layer Direction)
into a day-to-day workflow — it does not override any of them.

Full order text and every GDS-NNN section live in
`GOLDBOT_DEVELOPMENT_STANDARD.md`.

### Director Order No. 018 — RFC Standard

Establishes the RFC (Request For Change) process: large changes are
proposed, analyzed, risk-assessed, and Director-approved before any
code is written — never coded directly first. Mandates an RFC before
any change touching a new/removed Layer, the Pipeline, Ownership, a
Canonical Contract, Trading Logic, AI Logic, Risk Logic, Database
Architecture, a Public API Breaking Change, Security Architecture, the
Engineering Standard, or the Development Standard — the same boundary
already set by Order No. 016's Director Review list, now formalized
into a document process. The Worker may draft an RFC freely; the
Worker must not begin implementation until the RFC's Director Decision
reads Approved — a hard gate.

Full order text, the RFC template, and the process definition live in
`RFC_STANDARD.md`; individual RFC records live under `rfcs/`
(`rfcs/README.md` index, `rfcs/TEMPLATE.md` template).

### Director Order No. 019 — ADR Standard

Establishes the ADR (Architecture Decision Record) process: the
detailed technical record of *why* a significant architecture
decision was made, kept as permanent history — distinct from the
short WAR/WDR entries already in this file. Mandates an ADR for a new
Layer, a Layer merge, an Event Bus change, a Pipeline change, Database
Architecture, AI Architecture, Execution Flow, Security Architecture,
Performance Architecture, a Canonical Rule, an Engineering Rule, or a
Development Rule. An RFC is the proposal-and-approval gate; an ADR is
the permanent record of the resulting decision — a major change often
has both. The Worker may draft an ADR; it only becomes Approved after
Director sign-off — draft ADRs are not binding.

Full order text and the ADR template live in `ADR_STANDARD.md`;
individual ADR records live under `adrs/` (`adrs/README.md` index,
`adrs/TEMPLATE.md` template).

### Director Order No. 020 — Release Management Standard

Establishes the Release Lifecycle (Planning → Development → Internal
Testing → QA → Alpha → Beta → Release Candidate → Production →
Maintenance → Hotfix → End of Life) and the mandatory per-release
fields (Version Number, Scope, Features, Breaking Changes, Migration
Guide, Test Summary, Performance Summary, Security Review, Known
Issues, Rollback Strategy, Release Notes), plus a Release Checklist
(Architecture Validation, Engineering Validation, Development
Validation, Regression Test, Performance Test, Security Review,
Documentation Review, CHANGELOG, Director Approval) required before
any Production release. The Worker prepares Release Candidates, runs
tests, and writes Release Notes and Known Issues; Worker Authority
stops at Release Candidate — Production Release requires explicit
Director approval, full stop, no exception.

Full order text, lifecycle stage criteria, and the Version Numbering
convention (semantic versioning, MAJOR.MINOR.PATCH) live in
`RELEASE_MANAGEMENT_STANDARD.md`.

Orders No. 018, 019, and 020 together with Order No. 017 (GDS) and the
existing Architecture/Engineering standards form the full Governance
Chain, recorded in `CLAUDE.md`'s Worker Authority section.

### Director Order No. 021 — Deployment Authority — Worker as Deployment/DevOps Engineer

Establishes the Worker's deployment authority in two phases. Phase 1
(recommended, in effect now) is semi-autonomous: the Worker may
connect to the VPS, clone/pull the repo, create a virtualenv, install
dependencies, verify (never change) `.env`, run migrations, run tests
and a smoke test, create/update the systemd service, configure Nginx
if needed, check logs, start monitoring, fix errors, and prepare a
deployment report — but must not change production API keys, change
DNS, change firewall rules, or enable production trading. Phase 2
(fully autonomous, production-level — not yet in effect, Development
must complete first) adds CI/CD-driven deploy, Blue/Green deployment,
rollback, health check, auto-restart, monitoring, hotfix deploy, and
release deploy. Regardless of phase, replacing a Production API Key,
replacing the server, changing the VPS provider, a database reset,
changing firewall policy, replacing an SSL certificate,
enabling/disabling Live Trading, and deleting production data always
require Director Approval. The Director's own framing: the Worker is
not a VPS Administrator — the Worker performs the role of Deployment
Engineer / DevOps Engineer. The future-state target pipeline is Git
Push → Worker → CI/CD → VPS → Deploy → Health Check → Monitoring →
Report.

### Director Decision — DD-003 (Append-Only Journal Discipline)

Approved. `DIRECTOR_DECISIONS.md` is an append-only log — a missing
entry (Order No. 017's, caught and backfilled above) must never be
deferred to "next time"; it is corrected immediately as its own
append, never by editing or reordering existing entries.

**Governance Rule — Append-Only Discipline.** No entry is ever skipped
in any of the repository's append-only journals: `DIRECTOR_DECISIONS.md`,
a module's `WORK_LOG.md`, a module's `CHANGELOG.md`, an RFC record
under `rfcs/`, or an ADR record under `adrs/`. Every completed Director
Order, RFC, ADR, or significant Sprint must update its corresponding
journal immediately, in the same work pass — not deferred. This closes
the "when was this decision actually made?" question permanently by
keeping Governance History continuous.

Full order text recorded in `CLAUDE.md`'s "Deployment Authority —
Director Order No. 021" section; `docs/DEPLOYMENT.md` and
`docs/deployment/PRODUCTION_DEPLOYMENT.md` cross-reference it rather
than duplicating it.

### Director Decision — DD-004 (superseded by DD-005 below)

Recorded here for the first time, per DD-003's Append-Only Discipline
(a ratified decision must never remain only in chat history): DD-004
proposed a "flat `.py` facade" pattern for select GEL-001 modules —
keeping a canonical module as a top-level `.py` file re-exporting from
elsewhere, to preserve compatibility with code that resolves it by a
literal file path. **Status: superseded.** Empirical verification (see
DD-005) showed CPython's import system does not support this pattern
the way DD-004 assumed — see DD-005 for the corrected mechanism.

### Director Decision — DD-005 (GEL-001 Compatibility Exception)

**Approved.** The Worker's empirical finding is ratified: in CPython,
if both `system_monitor.py` and `system_monitor/` exist as siblings,
`import system_monitor` always resolves to the **package**, never the
flat file — there is no way to make a flat `.py` act as a stable
facade next to a same-named package. DD-004's flat-facade diagram is
therefore **revoked**; DD-005 replaces it.

**Canonical Decision.** GEL-001's goal remains *One Canonical Module =
One Package*, with one exception class:

**Compatibility Exception.** A module is exempted from automatic
packaging — and classified `Compatibility Exception`, not
`Violation` — if it is physically path-bound to any of: an
architecture/isolation test, an AST parser, a monkeypatch target, or
an external Public API. Converting such a module to a package would
break the very thing depending on its literal file path.

**Metrics (superseding any prior GEL-001 count):**

| Category | Count |
|---|---|
| Canonical Packages | 274 |
| Compatibility Exceptions | 11 |
| Violations | 0 |

`Exception ≠ Violation` — an exception is a deliberate, documented,
Worker-classified state; a violation is unaddressed non-compliance.

**Worker Authority.** The Worker may self-classify any module as
`Compatible → Package` or `AST Coupled → Compatibility Exception`
without Director Review — report only, per Director Order No. 016.

**Future path.** In v2, once the coupled AST tests are themselves
refactored to stop depending on the literal file path, the exception
is removed and the module is packaged normally.

**New standing rule — Empirical Verification for Foundation Rules.**
For any Foundation Rule, the Worker decides from empirical
verification, not theoretical assumption. If the real platform
(Python, the OS, Git, etc.) constrains what a rule can require, the
Worker documents the constraint and raises a Director Review to adapt
the rule — as happened here (GEL-001's flat-facade assumption in DD-004
did not hold empirically, so GEL-001 itself was adapted via DD-005
rather than forcing an unworkable rule on real code).

### DD-005 Compliance Audit — Result (commit `d9e0a84`)

A full DD-005 compliance audit (`DD005_COMPLIANCE_REPORT.md`, Uzbek,
per GLS-001 below) checked all 146 top-level canonical modules across
all 17 Layers against the seven DD-005 audit questions. Result: 146/146
`Compatible`, 0 `Potential Violations`. **One item raised for Director
Review** (documentation-completeness gap, not a Foundation Rule
breach): DD-005 states 274 Canonical Packages / 11 Compatibility
Exceptions, but no document itemizes those 11 exceptions by module
name — the audit's own top-level scope found 0 exceptions, meaning the
11 exist at a narrower/nested-file granularity that isn't registered
anywhere. Open question for Director: should a dedicated itemized
registry (e.g. `GEL001_EXCEPTIONS.md`) be created to name all 11, so
this count is independently verifiable rather than only asserted.

### Director Order — GLS-001 (GoldBot Engineering Language Standard)

**Approved.** All documents, audits, reports, and engineering records
in the GoldBot repository are written in Uzbek. Exceptions, kept in
their original form: programming languages, code elements (class/
function/file names, import statements, code blocks), API names,
library/framework names, standard protocols, and international
technical terms (the Director's own list: API, REST API, WebSocket,
Event Bus, Cache, Queue, Pipeline, Layer, Module, Package, Interface,
Dependency, Import, Export, Commit, Branch, Merge, Pull Request,
CI/CD, Docker, Kubernetes, PostgreSQL, Redis, Logger, Metrics, Health
Check, Benchmark, Performance, Rollback, Refactor, Compatibility,
Regression, Unit Test, Integration Test, Mock, Fixture — extensible,
not exhaustive). Report section headers use Uzbek terms, not copied
English templates (`Muammo`/`Sabab`/`Tavsiya`, not `Problem`/`Cause`/
`Recommendation`). Standard technical values (YES/NO, PASS/FAIL) are
exempt.

**Scope decision (Director-selected option): phased via RFC, not
immediate retroactive translation.** GLS-001 applies from this
decision onward to every newly created document, audit, and report —
already demonstrated by `DD005_COMPLIANCE_REPORT.md`, written fully
in Uzbek per this rule. The repository's existing English-language
documents (`CLAUDE.md`, `README.md`, `ARCHITECTURE.md`,
`GOLDBOT_DEVELOPMENT_STANDARD.md`, `RFC_STANDARD.md`, `ADR_STANDARD.md`,
`RELEASE_MANAGEMENT_STANDARD.md`, `DIRECTOR_DECISIONS.md` itself, and
others) are **not** retroactively translated by this decision. Full
retroactive translation — a large, risk-bearing effort, especially for
Trading Safety/Risk Logic text where a translation slip could shift
meaning — is deferred to its own dedicated RFC (per `RFC_STANDARD.md`,
since it is a Development/Engineering Standard-affecting change),
carrying its own Impact Analysis and Rollback Plan, to be scheduled as
a future Sprint rather than executed under this order.

Full order text recorded here (`DIRECTOR_DECISIONS.md`); no new
top-level file created for GLS-001 itself, per the Module Reuse
Principle — this entry is its canonical record.

### GLS-001 Amendment 1 — Report/Record Types in Scope

**Approved.** GLS-001's Uzbek-language requirement is not limited to
newly created *documents* — it explicitly covers every one of these
report/record types, generated at any time from this decision onward:
Audit Report, Director Review, Worker Report, `WORK_LOG.md` entries,
`CHANGELOG.md` entries, Pull Request description, RFC Summary, ADR
Summary, Release Notes, Sprint Report, Bug Report, Investigation
Report, Root Cause Analysis, Performance Report, Compliance Report.

**Exception list for this amendment** (stays in English, unchanged by
GLS-001): code, class, function, and variable names; package and
module names; file names; commit messages; API and protocol names;
RFC IDs, ADR IDs, and GEL/DD/GLS identifiers; other technical terms
already covered by GLS-001's base exception list.

This does not change GLS-001's retroactive-scope decision above —
existing English-language documents are still not translated by this
amendment; it only confirms which *kinds* of future output must be
Uzbek, closing the "does this apply beyond brand-new files" ambiguity.

### GLS-001 Amendment 1, mavjud hujjatlarga ta'siri

`GOLDBOT_DEVELOPMENT_STANDARD.md`'s Development Workflow (GDS-010) va
Rollback Strategy bo'limlaridagi "commit message"/"PR description"
namunalari — bu amendment ular endi Uzbek tilida yozilishini talab
qiladi; mavjud GDS matni o'zi ingliz tilida qolaveradi (yuqoridagi
scope decision'ga ko'ra), faqat undan keyin yozilgan haqiqiy commit
message va PR description'lar shu qoidaga bo'ysunadi.

### Director Order — Options-Before-Review (Worker Decision-Support Rule)

**Approved, Foundation-level.** Before opening any Director Review,
the Worker must first, on its own: (1) aniqlashi — identify the
problem precisely; (2) tahlil qilishi — analyze its root cause; (3)
kamida 2–3 ta yechim variantini tayyorlashi — prepare at least 2-3
solution options; (4) har birining afzallik va kamchiligini yozishi —
document each option's pros and cons; (5) tavsiya etilgan variantni
ko'rsatishi — state its own recommended option. Only after all five
steps does the Worker open a Director Review — and it opens with the
analysis already attached, not a bare question.

**Purpose, in the Director's own words:** this reduces how many
Director Reviews are needed and raises their quality — the Director
decides between concretely evaluated options, not from a blank
problem statement.

**Applies to:** every Director Review trigger already defined in
Director Order No. 016 (Layer Architecture, Pipeline, Trading Logic,
AI Logic, Decision Logic, Risk Logic, a public-API breaking change,
Ownership, a Canonical Contract, a Foundation Rule) and RFC/ADR
triggers (`RFC_STANDARD.md`, `ADR_STANDARD.md`) alike — this rule
governs *how* a review is opened, not *when* one is required; it does
not loosen or expand any existing Director Review trigger list.

**Exception:** a genuine emergency (Trading Safety incident requiring
immediate Director attention) may open a review without the full
options analysis if delay itself would be the greater risk — the
Worker states this explicitly when it happens, then backfills the
options analysis once the immediate risk is addressed.

### Director Order — DRQ-001 (Director Review Quality Rule)

**Approved, Foundation-level.** Every Director Review the Worker opens
must contain, in full, all of: Muammo tavsifi (problem description),
Root Cause Analysis, Ta'sir doirasi (which Layers/modules are
affected), Risk darajasi (Low/Medium/High/Critical), at least 2-3
yechim varianti (solution options), Worker tavsiyasi (the Worker's own
recommendation), the impact on Development if no decision is made, and
one precise question the Director's decision must answer.

**Forbidden — a Review is rejected-on-arrival if it is only:** "Nima
qilamiz?" ("What do we do?"), "Qanday bo'lsin?" ("How should it be?"),
or "Qaysi variantni tanlaymiz?" ("Which option do we pick?") without
the full analysis above attached. A Director Review exists to
**confirm an already-analyzed decision**, not to ask a bare question.

DRQ-001 is the enforcement form of the Options-Before-Review rule
recorded just above — that rule states *what* the Worker must do
before opening a review; DRQ-001 states the exact *shape* a compliant
review must have, and what disqualifies one.

### GEL001_EXCEPTIONS.md — Exception Lifecycle Rule

**Approved, Foundation-level.** Every entry in `GEL001_EXCEPTIONS.md`
must carry a `Status` field set to exactly one of: `Active`, `Under
Review`, `Resolved`, `Deprecated`. No exception is permitted to exist
without a lifecycle state, and no exception is permitted to live
forever unexamined — every Active exception is a candidate for future
re-evaluation (e.g. once the AST/monkeypatch/Public API coupling that
justified it is itself refactored away, per DD-005's own "Future path"
clause) or for closure. This rule binds `GEL001_EXCEPTIONS.md` itself,
whenever that registry is created/updated.

### DD-005 Correction — Exception Registry Verification (Empirical Re-Verification, kengaytirilgan metodologiya)

**Kelib chiqishi:** Director Order "DD-005 Exception Registry
Verification" — avvalgi tor-metodologiyali audit (`GEL001_EXCEPTIONS.md`,
commit `72135eb`) faqat `Path(...).read_text()` + `ast.parse()`
kombinatsiyasini "bitta test = bitta literal Path" naqshi bo'yicha
qidirgan va 9 ta Compatibility Exception topgan edi, DD-005'ning asl
"11" raqamiga zid holda.

**Muammo tavsifi:** Direktor ushbu 9 vs 11 farqni hal qilishdan oldin
kengroq qidiruv metodologiyasi bilan (`ast.parse`, `inspect.getsource`/
`getfile`, `.exists()`/`.is_file()`, `importlib.resources`, `pkgutil`,
`monkeypatch.setattr`/`mock.patch` literal-yo'l nishonlari va boshqa
literal fayl-yo'l satrlari) butun repozitoriyni (barcha 17 Layer) qayta
tekshirishni buyurdi.

**Root Cause Analysis:** Kengaytirilgan qidiruv shuni ko'rsatdi — ikkala
oldingi audit ham (DD-005'ning o'zi va undan keyingi 9-tali tor audit)
faqat "bitta test funksiyasi bitta modulga literal Path quradi" naqshini
qidirgan. Ammo repoda uchtа qo'shimcha test **bir nechta modulni bitta
`for filename in (...)` sikli ichida ketma-ket** literal yo'l bilan
qurib, har birini alohida `.read_text()` + `ast.parse()` bilan o'qiydi:
`tests/media/test_media_adapter.py` (2 fayl: `media_adapter.py`,
`media_pipeline.py`), `tests/monitoring/test_monitoring_isolation.py`
va `tests/monitoring/test_phase_b0_isolation.py`/
`test_phase_b0_compatibility.py` (`core_layer/health_monitor/` ichidagi
9 fayl: `system_monitor.py`, `market_monitor.py`, `signal_monitor.py`,
`error_monitor.py`, `models.py`, `resource_monitor.py`,
`health_monitor.py`, `performance_collector.py`, `access.py`). Bu
naqsh mezonning ikkala shartiga ((a) muayyan bitta modul fayliga
literal yo'l, (b) shu aniq faylni o'qish/tahlil qilish) to'liq mos
keladi, faqat bir nechta modul bitta test funksiyasida qamrab olingani
sababli avvalgi ikkala audit metodologiyasi buni ko'rmagan.

**Ta'sir doirasi:** Media Layer (`media_layer/content_manager/`) va
Core Layer (`core_layer/health_monitor/`) — jami 11 ta qo'shimcha modul
avvalgi 9 taga qo'shildi.

**Natija:** Ushbu kengaytirilgan tekshiruvda haqiqiy dalil bilan
tasdiqlangan Compatibility Exception soni **20** — bu DD-005'ning asl
**"11"** raqamidan ham, avvalgi tor audit topgan **"9"** raqamidan ham
farq qiladi. To'liq ro'yxat, har biri uchun Evidence (fayl:qator,
kod parchasi), Confidence va Status bilan — `GEL001_EXCEPTIONS.md`da
qayd etilgan.

**Risk darajasi:** Low — bu hujjatlashtirish/hisob farqi, Trading
Safety, Signal Logic, Risk Logic yoki Decision Logic'ga hech qanday
ta'siri yo'q; DD-005'ning "Exception ≠ Violation" tamoyili
o'zgarishsiz qolmoqda (0 Violations tasdiqlangan holicha qoladi).

**DD-005'ning asl "11" raqami** ushbu empirik topilma bilan
**superseded** deb belgilanadi — DD-003 Append-Only Discipline
tamoyiliga ko'ra yuqoridagi original DD-005 matni o'zgartirilmadi/
o'chirilmadi, faqat mazkur yozuv orqali tuzatiladi: haqiqiy son 11
emas, **20 (empirik tasdiqlangan, GEL001_EXCEPTIONS.md'da to'liq
ro'yxatlangan)**.

**Director Review uchun ochiq savol:** DD-005'ning "274 Canonical
Packages / 11 Compatibility Exceptions" metrikasi Compatibility
Exceptions ustuniga nisbatan "20" ga yangilanishi kerakmi, yoki
Direktor 274 Canonical Packages sonini ham qayta hisoblashni
buyuradimi (chunki 11 ta qo'shimcha flat modul — `media_adapter.py`,
`media_pipeline.py` va `core_layer/health_monitor/`ning 9 fayli —
hozircha "274 Canonical Packages" ichida paketlashtirilmagan flat
modul sifatida hisoblanayotgan bo'lishi mumkin).

**Worker tavsiyasi:** DD-005 metrikasi jadvalida Compatibility
Exceptions ustunini 11'dan 20'ga yangilash, Canonical Packages sonini
(274) o'zgartirmaslik — chunki bu 20 modul hali paketlanmagan holda
qolmoqda (ular hali "Compatibility Exception" holatida, "Canonical
Package" emas).

**Manba:** Ushbu qayta tekshiruvning to'liq metodologiyasi, ko'rib
chiqilgan va False Positive deb rad etilgan holatlar ro'yxati (110 ta
`mock.patch`/`monkeypatch.setattr` dotted-path chaqiruvi, 6 ta
`inspect.getsource` chaqiruvi, va boshqalar) `GEL001_EXCEPTIONS.md`da
to'liq keltirilgan.

### Director Order — GLS-001 Translation Standard

**Tasdiqlandi.** GoldBot repository hujjatlarini yagona standart
asosida O'zbek tiliga o'tkazish jarayoni belgilanadi. Bu faqat
hujjatlar tarjimasi — kod va arxitekturaga o'zgartirish kiritilmaydi.

**Tarjima qilinmaydi (doim ingliz tilida qoladi):** `.py` fayl
nomlari, Package nomlari, Module nomlari, Class nomlari, Function
nomlari, Variable nomlari, API nomlari, Framework nomlari, Kutubxona
nomlari, Git Commit, Branch nomlari, kod bloklari, texnik terminlar,
RFC/ADR/DD/GEL/GDS/GLS identifikatorlari.

**O'zbek tiliga tarjima qilinadi:** `README.md`, `CONTRACTS.md`,
`ROADMAP.md`, `MODULE_MAP.md`, `IMPLEMENTATION.md`, `WORK_LOG.md`,
`DIRECTOR_DECISIONS.md`, `CHANGELOG.md`, Audit Report, Sprint Report,
Director Review, Bug Report, Root Cause Analysis, Compliance Report,
Performance Report, Investigation Report, Release Notes.

**Tarjima tartibi:** Layer → Module → File. Har bir modul ichida:
001 `README.md` → 002 `CONTRACTS.md` → 003 `ROADMAP.md` → 004
`MODULE_MAP.md` → 005 `IMPLEMENTATION.md` → 006 `WORK_LOG.md` → 007
`DIRECTOR_DECISIONS.md` → 008 `CHANGELOG.md`. Har bir fayl 100%
yakunlangandan keyingina keyingi faylga o'tiladi.

**Workflow (har bir hujjat uchun majburiy):** Hujjatni o'qish →
Mazmunni tahlil qilish → O'zbek tiliga tarjima qilish → Texnik
terminlarni tekshirish → Sifat nazorati → WORK_LOG yangilash →
Keyingi hujjat.

**Tarjima qoidalari:** ma'no o'zgartirilmaydi, kod bloklariga
tegilmaydi, diagrammalarga tegilmaydi, jadval tuzilishi
o'zgartirilmaydi, identifikatorlar tarjima qilinmaydi, texnik
terminlar saqlanadi.

**Commit Policy:** har bir hujjatdan keyin commit qilinmaydi — har
bir modul tugagandan keyin bitta commit. Har bir commit uchun
Validation (CLAUDE.md'ning to'liq Commit Protocol'i) majburiy.

**Taqiqlangan:** batch translation, bir nechta hujjatni bir vaqtda
tarjima qilish, kodni o'zgartirish, `.py` fayl/Package/Module
nomlarini o'zgartirish, xayoliy ma'lumot qo'shish (Empirical
Verification standing rule bilan bir xil — faqat haqiqiy matn
tarjima qilinadi, hech narsa o'ylab topilmaydi).

**Success Criteria (har modul yakunida):** barcha hujjatlar O'zbek
tiliga o'tkazilgan, texnik terminlar saqlangan, kodga o'zgartirish
kiritilmagan, `WORK_LOG.md` yangilangan, Validation muvaffaqiyatli
yakunlangan, modul bitta commit bilan yakunlangan.

**Asosiy qoida:** ustuvor maqsad so'zma-so'z tarjima emas — hujjatning
texnik ma'nosini to'liq va aniq O'zbek tilida saqlab qolish.

Bu buyurtma GLS-001 va uning Amendment 1'ini bekor qilmaydi —
retroaktiv tarjima haqidagi asosiy scope decision ("bosqichma-bosqich
RFC orqali", yuqorida qayd etilgan) shu buyurtma bilan rasman
boshlanadi: bu — o'sha kelajakdagi RFC/Sprint ishining birinchi
bosqichi, mavjud hujjatlarni bir martalik ommaviy tarjima emas,
qat'iy nazorat qilinadigan, modul-ma-modul jarayon sifatida.

### GLS-001 Translation Standard — Amendment 1 (Commit Granularity, Terminology)

**Tasdiqlandi.** Birinchi bosqichlar (`risk_layer` — 8 modul, 8
commit; `trade_monitoring_layer`, `execution_layer`, `decision_layer`
— Layer-level hujjatlar + modullar, har biri alohida commit bilan)
to'g'ri yo'nalishda bajarildi, lekin commit granularity juda mayda
bo'ldi: 215+ modulda bu 200+ commit degani, Git tarixini haddan
tashqari maydalab yuboradi. Shu sababli GLS-001 Translation
Standard'ning Commit Policy bandi quyidagicha tuzatiladi (asl band
tarixiy o'rnida qoladi — bu uni almashtiruvchi tuzatish, DD-003
Append-Only Discipline'ga muvofiq):

**Yangi Commit Policy: 1 Layer = 1 Commit.** Tarjima tartibi
o'zgarmaydi (Layer → Layer Documents → Module 001 → [README →
CONTRACTS → ROADMAP → MODULE_MAP → IMPLEMENTATION → WORK_LOG →
DIRECTOR_DECISIONS → CHANGELOG] → Module 002 → ... → Layer Complete),
lekin butun Layer (barcha modullar + Layer-level hujjatlar) to'liq
tarjima qilib bo'lingandan keyingina **bitta** commit qilinadi
(masalan: `Translate risk_layer documentation to Uzbek (GLS-001)`).
Worker har modul ichida xuddi avvalgidek ishlaydi (bitta hujjat
to'liq tugagandan keyin keyingisiga o'tadi), farq faqat **qachon
commit qilinishida**.

**Layer yakunida Director Review formati (majburiy):**
```
<Layer nomi>
Completed Modules: <son>
Translated Files: <son>
Validation: PASS/FAIL
Terminology: PASS/FAIL
Missing: <son>
Ready: YES/NO
```

**Effective from:** bu tuzatish `risk_layer`, `trade_monitoring_layer`,
`execution_layer`, `decision_layer`'ning allaqachon yakunlangan
commit tarixini o'zgartirmaydi (tarix qayta yozilmaydi). **Keyingi
Layer'dan boshlab** (`signal_layer` va undan keyingilar) yangi 1
Layer = 1 Commit qoidasi qo'llaniladi.

**Terminology qoidasi (soddalashtirilgan — Director'ning ikkinchi
tuzatishi).** Faqat `.md` hujjat matni tarjima qilinadi: gap O'zbek
tilida yoziladi, lekin texnik terminlar har doim asl inglizcha
shaklida qoladi — ularga alohida O'zbek muqobili qidirilmaydi (masalan
`Layer`, `Package`, `Pipeline`, `Compatibility`, `Dependency`,
`Validation`, `Exception`, `Rollback` — bularning hech biriga
tarjima yozilmaydi, gap ichida original holida turadi). Faqat oddiy
prozaik so'zlar (`Problem` → `Muammo`, `Cause` → `Sabab`, `Solution`
→ `Yechim`, `Recommendation` → `Tavsiya` kabi) tarjima qilinadi.
Yagona lug'at `docs/TERMINOLOGY.md`da saqlanadi — Worker yangi
prozaik so'zga duch kelganda avval shu faylni tekshiradi, mavjud
bo'lmasa mos tarjimani tanlab shu faylga qo'shadi (append-only,
mavjud yozuv o'zgartirilmaydi); texnik terminlar bu lug'atga
kiritilmaydi, chunki ular umuman tarjima qilinmaydi.

**Muhim eslatma — bir vaqtlilik xavfi haqida.** Bu tuzatish
birinchi marta yozilganida, aynan shu paytda ishlayotgan tarjima
agenti uni "fabricated Director Order" deb noto'g'ri talqin qilib,
ikki marta bekor qildi (o'z hisobotida to'g'ri qayd etilgan) — bu
in'ektsiya emas, Worker'ning o'zining bir vaqtda ishlayotgan ikki
jarayoni orasidagi to'qnashuv edi. Xulosa: `DIRECTOR_DECISIONS.md`
va shunga o'xshash boshqaruv fayllariga yozish faqat bitta jarayon
tinch holatda bo'lganda amalga oshiriladi, parallel ishlayotgan boshqa
Worker jarayoni yo'qligi tasdiqlangandan keyin.

### Director Review — PHASE-02 Rasmiy Yakun

**Tasdiqlandi.** FLOW-019 (Application Services) yakuniy holati:
Production Wiring ✅, Telegram Consumer ✅, Application Service Layer
✅, Architecture PASS, Tests 5490 PASS, GitHub Actions SUCCESS
(commit `a06926e`, CI Run `31225897192`). PHASE-02 (Flow-by-Flow
Development) shu bilan **rasman COMPLETED** deb e'lon qilinadi —
FLOW-016 (Chart Service Foundation), FLOW-017 (Personal AI Core),
FLOW-018 (Backtesting Engine), FLOW-019 (Application Services)
barchasi Input → Processing → Output → Real Consumer mezoni bo'yicha
tekshirilgan va CI bilan tasdiqlangan. To'liq yozuv:
`docs/PHASE_02_FLOW_BY_FLOW_DEVELOPMENT.md`'ning "PHASE-02 — Rasmiy
Yakun" bo'limi.

**Muhim fakt (audit orqali aniqlangan):** `goldbot-v1` uchun
avtomatik GitHub Actions ishlamaydi (`ci.yml`'ning `push` trigger'i
faqat `main`/`feature/**`/`fix/**`/`hotfix/**`ni qamraydi). PHASE-02
yakuni qo'lda ishga tushirilgan `workflow_dispatch` orqali haqiqiy CI
bilan tasdiqlandi — bu holat PHASE-03 davomida ham (branch strategiyasi
hal qilingunga qadar) davom etadi.

**PHASE-03 — Release Preparation boshlandi.** Reja: Branch Cleanup →
`release/v1.0.0-rc1` → Final Release Audit → Final Validation → `main`
Promotion → VPS Deployment → Production Monitoring. Zamin: GBA-001
(`audits/GBA-001/`), GBA-002 (`audits/GBA-002/`).
