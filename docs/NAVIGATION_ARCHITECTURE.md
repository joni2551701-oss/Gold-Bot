# Navigation Architecture (TASK-002B)

**Status: ✅ APPROVED** (Director review, following the 6 Director
Questions below — see "Director Decisions" for the actual resolutions,
which supersede this document's original proposals where they
differ). TASK-002C (Navigation Registry) is 🟢 AUTHORIZED under the
constraints recorded in `communication/task_queue/TASK-002C.md`.

Step 2 of `docs/PLATFORM_WORKFLOW.md`'s "Architecture First" process.
**Architecture only — no implementation, code, or public API exists
after this document.** Every proposal below is a design for Director
review; nothing here is built until TASK-002C (Registry) is
authorized, which does not happen until this document is approved.

Governed by `communication/decisions/ADR-001.md` and Constitution
Article 13 (Future First Principle): every component below states its
compatibility across all five target platforms — Telegram Bot,
Telegram Mini App, Android, iOS, Desktop — using
`platform_layer/platform_service/capability_model.py`'s existing `SupportStatus` contract
(`SUPPORTED` / `NOT_SUPPORTED` / `PLANNED`, the latter two always with
a reason). Built on `docs/NAVIGATION_ANALYSIS.md`'s findings; answers
its six open questions per `communication/decisions/ADR-001.md`.

Every proposal follows the Universal UI Abstraction rule: nothing
below connects a client directly to Business Logic. The shape is
always `Platform UI → Navigation Layer → Application Layer → Business
Logic` — the 13 components below are what the Navigation Layer (and
its immediate neighbors) is made of.

## 1. Universal Navigation (umbrella)

The name for this whole architecture, not a component of its own: a
platform-agnostic description of where a user can go and how they get
there, expressed once and rendered differently per client by each
client's own Platform Adapter (§8). Everything below is a piece of it.

## 2. Screen Model

**Responsibility**: the atomic navigable unit — a destination,
independent of how any client renders it. Extends
`platform_layer/platform_service/navigation_model.py`'s existing `NavigationNode` (id,
label_key, permission, platforms) rather than replacing it (Article 11
reuse): a Screen adds a `category` (which section it groups under —
generalizing today's Settings/Admin/Owner/Profile/Signals concept) and
a `content_type` (what kind of content it shows — a list, a form, a
static message — data-driven, never a rendering instruction).

A Screen is a description. It is never itself a rendered UI element,
a Telegram message, or an Android Fragment instance.

| Platform | Status | Reason |
|---|---|---|
| Telegram Bot | SUPPORTED | Every existing command already maps to one conceptual destination (`docs/PLATFORM_ARCHITECTURE.md` §5's six sections) — a Screen is that same concept, generalized. |
| Telegram Mini App | SUPPORTED | A Mini App screen (web view route) is the same concept rendered as a page. |
| Android | SUPPORTED | Maps to a Fragment/Activity's destination concept. |
| iOS | SUPPORTED | Maps to a UIViewController's destination concept. |
| Desktop | SUPPORTED | Maps to a window/panel destination concept. |

## 3. Navigation Graph

**Responsibility**: the full set of Screens and the valid transitions
between them — replacing the *implicit* structure hardcoded today
across `_SECTION_BY_COMMAND`/`_SECTION_LABEL_KEYS`
(`platform_layer/telegram/reply_keyboard_manager.py`) with an *explicit* directed
graph: Screens are nodes, allowed transitions are edges.

**Why a graph, not a tree**: `NavigationNode.children` (TASK-001)
implies a tree — but GoldBot's real navigation already has a
non-tree edge (Settings and Profile are siblings, yet Profile's
Subscription screen and the Signals section's Premium screen both lead
to `/upgrade` — a shared destination reachable from two places). A
graph expresses this without duplicating the destination; a tree
would force a choice about which parent "owns" it.

| Platform | Status | Reason |
|---|---|---|
| Telegram Bot | SUPPORTED | Today's five sections + Main are expressible as a graph today; the graph would describe the *existing* structure, not change it. |
| Telegram Mini App | SUPPORTED | A page graph is the native shape of a web-app router. |
| Android | SUPPORTED | Matches the "navigation graph" concept Android's own platform tooling already uses natively. |
| iOS | SUPPORTED | Matches a coordinator-pattern navigation graph. |
| Desktop | SUPPORTED | Matches a windowed app's panel/menu graph. |

## 4. Route Registry

**Responsibility**: resolves Analysis open question 1 (destination
type). Extends `platform_layer/platform_service/menu_registry.py`'s existing `MenuRegistry`
(Article 11 reuse) with a **target binding** per platform: for a given
Screen id, what does each platform actually navigate *to* —
Telegram: a `"/command"` string (today's real mechanism); Mini App: a
URL path; Android: a route name; iOS: a view-controller identifier;
Desktop: a window/panel identifier. One Screen id, five possible
concrete targets, only as many populated as that platform has code for.

| Platform | Status | Reason |
|---|---|---|
| Telegram Bot | SUPPORTED | Target binding = the existing `"/command"` string; no new concept, just naming what already exists. |
| Telegram Mini App | PLANNED | Target shape (URL path) is known in principle; no Mini App client exists to bind to yet. |
| Android | PLANNED | Target shape (route name) is known in principle; no Android client exists yet. |
| iOS | PLANNED | Same as Android. |
| Desktop | PLANNED | Same as Android. |

## 5. Back Stack

**Responsibility**: resolves Analysis open question 2 (flat
mode-switch vs. real stack). **Proposed**: a real, arbitrary-depth
stack (push on navigate, pop on Back) as the universal model — because
it is a strict superset of Telegram's current behavior, not a
different model. Telegram's actual UX (every submenu's Back always
returns to Main, never to an intermediate screen — `docs/PHASE6_FREEZE.md`
Stage 3) is expressible as a stack with a platform-specific rule its
own Platform Adapter (§8) enforces: "collapse to depth ≤ 1." Native
platforms use the stack at full depth instead. One model, not two —
**flagged as a Director Question below**, since this is the single
proposal in this document most likely to be wrong if GoldBot's real
future UX needs differ from this assumption.

| Platform | Status | Reason |
|---|---|---|
| Telegram Bot | SUPPORTED | Current behavior is a depth-1-collapsing special case of a real stack — no behavior change, just a reinterpretation. |
| Telegram Mini App | SUPPORTED | A web app's browser-history-style stack is the native shape. |
| Android | SUPPORTED | Matches Android's own back-stack concept directly. |
| iOS | SUPPORTED | Matches `UINavigationController`'s stack directly. |
| Desktop | SUPPORTED | Matches a windowed app's own back/forward concept. |

## 6. Deep Link System

**Responsibility**: resolves an external URI directly to a Screen +
parameters, bypassing manual navigation (e.g. a shared link opening
straight to a specific signal). **Does not exist in any form today** —
GoldBot has no navigation-purposed deep-link handling currently (only
the unrelated `/start <payload>` registration-source concept, not a
navigation deep link). Genuinely new, no existing Foundation/Manager/
Contract/Model/Capability/Registry to reuse (Article 11 audit: all
six "no").

| Platform | Status | Reason |
|---|---|---|
| Telegram Bot | PLANNED | Telegram supports deep links (`t.me/bot?start=...`) technically, but none is wired to Navigation today. |
| Telegram Mini App | PLANNED | Mini Apps support URL-based deep links natively; no Mini App exists yet to receive one. |
| Android | PLANNED | Android Intents support this natively; no Android client exists yet. |
| iOS | PLANNED | iOS Universal Links support this natively; no iOS client exists yet. |
| Desktop | PLANNED | Desktop deep-linking (custom URI scheme) is platform-dependent; no Desktop client exists yet. |

## 7. Permission Layer

**Responsibility**: resolves Analysis open question 4. Decides which
Screens in the Navigation Graph a given user/tier can reach.
**Proposed**: keep tier *resolution* per-client (each platform already
has, or will have, its own identity mechanism — Telegram's
`telegram_id`, a future Android account/session), but standardize the
*output* — a platform-agnostic tier concept mirroring
`platform_layer/telegram/permissions.py`'s `PermissionLevel` (OWNER/ADMIN/USER) values
by convention, the same "by convention, not by import" relationship
`platform_layer/platform_service/navigation_model.py`'s `permission` field already has today
(TASK-001). The Navigation Graph itself, not each client individually,
is what checks a Screen's required tier against the resolved value —
centralizing the *check*, not the *resolution*.

| Platform | Status | Reason |
|---|---|---|
| Telegram Bot | SUPPORTED | `platform_layer/telegram/permissions.py`'s existing `PermissionLevel`/`get_permission_level()` already resolves this; nothing to build, only to reference by convention. |
| Telegram Mini App | PLANNED | Would need its own identity resolution (likely Telegram's own auth data, since Mini Apps run inside Telegram) — not designed here. |
| Android | PLANNED | Needs an account/session system that doesn't exist yet. |
| iOS | PLANNED | Same as Android. |
| Desktop | PLANNED | Same as Android. |

## 8. Platform Adapter

**Responsibility**: the per-client translation layer — takes the
universal Navigation Graph + Route Registry + Back Stack state and
executes it however that platform natively works. This is the
component the Universal UI Abstraction rule's middle arrow
(`Navigation Layer → Application Layer`) passes through on its way
to a real client screen. `platform_layer/telegram/reply_keyboard_manager.py` and
`platform_layer/telegram/keyboards.py` are, conceptually, *today's entire Platform
Adapter for Telegram* — already built, already tested
(`tests/telegram/test_keyboards.py`, 38 tests) — but this Architecture
does **not** propose modifying them; a future, separately-approved
task decides whether/how they come to consume the graph described
here internally, without changing their external behavior (Phase 6
Freeze stands).

| Platform | Status | Reason |
|---|---|---|
| Telegram Bot | SUPPORTED | Already exists today (`platform_layer/telegram/reply_keyboard_manager.py`), just not yet connected to a shared graph — connecting it is explicitly out of scope for this Architecture. |
| Telegram Mini App | NOT_SUPPORTED | No client exists; future adapter would be a JS/web router. |
| Android | NOT_SUPPORTED | No client exists; future adapter would use Android's native navigation component. |
| iOS | NOT_SUPPORTED | No client exists; future adapter would use `UINavigationController`. |
| Desktop | NOT_SUPPORTED | No client exists; future adapter would use whatever desktop UI framework is chosen (undecided). |

## 9. Navigation State

**Responsibility**: resolves Analysis open question 3. **Proposed**:
per-client-session, in-memory (or platform-native equivalent),
**not** centralized in `database/` — extending today's Telegram
precedent (`_LAST_SECTION`, process-local, `docs/PHASE6_FREEZE.md`
Stage 2) to every platform, rather than replacing it. Reasoning:
navigation position is an ephemeral UI fact tied to one live client
connection, not a persistent business record; centralizing it would
add a round-trip to a shared store on every tap for no product
benefit, and none of the five platforms need to know another
platform's navigation position (each device/session navigates
independently, even for the same user).

| Platform | Status | Reason |
|---|---|---|
| Telegram Bot | SUPPORTED | Already implemented this way (`_LAST_SECTION` in `platform_layer/telegram/reply_keyboard_manager.py`). |
| Telegram Mini App | PLANNED | Would use browser/session storage; not built yet. |
| Android | PLANNED | Would use the OS's own saved-instance-state mechanism; not built yet. |
| iOS | PLANNED | Would use `UIViewController`'s own state restoration; not built yet. |
| Desktop | PLANNED | Would use the app's own in-memory window state; not built yet. |

## 10. Session Navigation

**Responsibility**: binds Navigation State (§9) to a concrete identity
per platform — e.g. Telegram's `telegram_id`, a future Android
account/session token. Authentication/session-management itself is
explicitly **not** part of Navigation's scope (it is whatever each
platform's own identity system provides); Session Navigation is only
the thin binding between "this session" and "this session's current
Navigation State."

| Platform | Status | Reason |
|---|---|---|
| Telegram Bot | SUPPORTED | `telegram_id` already serves this role today (`_LAST_SECTION` is keyed by it). |
| Telegram Mini App | PLANNED | Would bind to whatever identity Telegram's Mini App auth data provides. |
| Android | PLANNED | Would bind to a future account/session system, undesigned. |
| iOS | PLANNED | Same as Android. |
| Desktop | PLANNED | Same as Android. |

## 11. Navigation Events

**Responsibility**: the event vocabulary a Platform Adapter (§8) emits
when a user navigates — e.g. `ScreenEntered`, `ScreenExited`,
`BackPressed`, `DeepLinkResolved` — for future observability, adjacent
to (but not part of) the existing `monitoring/`/`analytics/`
foundations. Genuinely new — no existing event vocabulary for
navigation exists in this repo today. Not wired to any consumer; a
future task would decide whether/how `monitoring/` ever reads these.

| Platform | Status | Reason |
|---|---|---|
| Telegram Bot | PLANNED | No navigation event vocabulary exists today — `keyboard_for_command()`/`record_section()` change state but emit nothing observable. |
| Telegram Mini App | PLANNED | Same — undesigned until a client exists. |
| Android | PLANNED | Same. |
| iOS | PLANNED | Same. |
| Desktop | PLANNED | Same. |

## 12. Screen Lifecycle

**Responsibility**: the states a Screen instance passes through
(e.g. Created → Active → Backgrounded → Destroyed) — a real, OS-backed
concept on native platforms. **Named mismatch, not papered over**: a
Telegram "screen" has no equivalent of Backgrounded/Destroyed — it is
the most recent bot message plus the current Reply Keyboard, always
freshly "Created" on the next interaction, per
`docs/PLATFORM_ARCHITECTURE.md`'s own description of the mechanism
(§2 of this document). A universal Screen Lifecycle model would need
to treat Telegram as a degenerate case (Created → Destroyed only, no
Backgrounded), not force a fictitious Backgrounded state onto a
platform that has none.

| Platform | Status | Reason |
|---|---|---|
| Telegram Bot | NOT_SUPPORTED | No real lifecycle exists — each Telegram interaction is a fresh message, not a persistent view object with OS-driven state transitions. Modeling one would be synthetic, not real. |
| Telegram Mini App | PLANNED | A web view has a real (if simpler) lifecycle (page load/unload); undesigned until a client exists. |
| Android | PLANNED | Android Fragments/Activities have a rich native lifecycle; undesigned until a client exists. |
| iOS | PLANNED | `UIViewController` has a rich native lifecycle; undesigned until a client exists. |
| Desktop | PLANNED | Window lifecycle (minimize/restore/close) exists but is framework-dependent (undecided); undesigned until a client exists. |

## 13. Platform Capability Mapping

**Responsibility**: the concrete application, to Navigation itself, of
`platform_layer/platform_service/capability_model.py`/`capability_registry.py`/
`cross_platform_checker.py` — already built in TASK-001, reused here
rather than duplicated (Article 11). Every component above (§2–§12) is,
in effect, one `ModuleCapabilityRegistry` entry once TASK-002C
(Registry) populates it; `cross_platform_checker.check_module_capabilities()`
already enforces that every platform is addressed and every
non-`SUPPORTED` entry carries a reason — exactly the discipline this
document's own tables above were held to, by hand, in this Architecture
step. TASK-002C's job is making that machine-checked, not re-deriving
the rule.

| Platform | Status | Reason |
|---|---|---|
| Telegram Bot | SUPPORTED | The mapping mechanism itself (`platforms/capability_*`) already exists and is tested (TASK-001, 28 tests). |
| Telegram Mini App | SUPPORTED | Same mechanism — a `NOT_SUPPORTED`/`PLANNED` entry with the right reason is exactly how this platform's rows above were expressed. |
| Android | SUPPORTED | Same. |
| iOS | SUPPORTED | Same. |
| Desktop | SUPPORTED | Same. |

## What this Architecture does not decide

Per Director instruction, no code, API, or folder structure is created
by this document. Where a proposal above (e.g. §5 Back Stack, §7
Permission Layer's new platform-agnostic tier concept) would become a
new public API or contract once implemented, that remains gated by the
No Silent Decisions Policy (`communication/decisions/README.md`) at
TASK-002D (Implementation) — approving this Architecture is not itself
approval to implement any specific API shape.

## Director Decisions (resolved)

The Director answered six questions directly; where an answer
supersedes this document's original §-section proposal, the answer
governs. Full record: `communication/decisions/ADR-001.md` through
`ADR-004.md`.

1. **Back Stack (§5) — RESOLVED: real Navigation Stack, no exception
   for Telegram.** Telegram is never treated as a special case.
   Every platform — Telegram, Android, iOS, Desktop, Mini App — pushes
   the same stack (e.g. `Root → Dashboard → Signals → Signal Details`).
   Telegram's "Back to Main" is `Stack → Root`, not a distinct rule.
   This is stronger than §5's original "depth-1-collapsing special
   case" proposal — there is no special case at all, one model for
   every platform.
2. **Platform Adapter boundary (new, beyond the original 6 questions)
   — RESOLVED.** The Adapter touches UI only, never Business Logic:
   `UI → Platform Adapter → Navigation Core → Application → Business
   Logic`. Refines §8.
3. **Route Registry (§4) — RESOLVED: dynamic, not static.** Required
   for future extensibility (Plugin, AI Module, Education, Marketplace
   modules will each need to register their own screens without a code
   change to the Registry itself). Confirms and strengthens §4's
   design.
4. **Permission Layer (§7) — RESOLVED: runs before Navigation, not
   inside it.** Sequence: `Request → Permission → Navigation → Screen`
   — an unauthorized screen is never navigated to in the first place,
   not hidden after the fact. Refines §7 (the original proposal did
   not specify this ordering explicitly).
5. **Deep Link System (§6) — RESOLVED: in scope, all five platforms.**
   `goldbot://signal/123`, `goldbot://profile`, `goldbot://education`
   resolve identically on Telegram, Mini App, Android, iOS, and
   Desktop. Supersedes §6's "should this move to a later task?"
   framing — it stays in TASK-002's scope.
6. **Navigation State (§9) — RESOLVED: stored in the Platform Layer;
   the Business Layer never knows about it.** Confirms §9's original
   proposal (per-client, not centralized in `database/`) and adds the
   explicit layering rule: Business Logic has zero navigation-state
   awareness, full stop.

**Not explicitly re-answered** (carried forward, still open for
TASK-002D): Screen Lifecycle's Telegram mismatch (§12) and whether
Permission Layer's future platform-agnostic tier concept becomes a
new formal contract or reuses `platform_layer/telegram/permissions.py`'s enum
directly — both deferred to Navigation Implementation (TASK-002D),
not blocking TASK-002C (Registry).

### ADR-002 — Universal Screen Identity

Every screen gets one ID, stable across every platform — e.g.
`dashboard.home`, `signals.list`, `signals.details`, `settings.main`,
`settings.notifications`, `profile.main`. The ID never changes per
platform. See `communication/decisions/ADR-002.md`.

### ADR-003 — Platform never creates a Screen

A platform only ever *calls* Navigation to reach a screen; it never
constructs one itself. Always `Screen Registry → Navigation →
Platform Adapter → Telegram` (or any other client) — never `Telegram →
Create Screen` directly. See `communication/decisions/ADR-003.md`.

### ADR-004 — Navigation Event Bus

Every platform emits the same event vocabulary: `ScreenOpened`,
`ScreenClosed`, `BackPressed`, `PermissionDenied`, `NavigationFailed`,
`DeepLinkOpened`, `SessionExpired` — for a future Analytics/AI consumer.
Interface only in TASK-002C, no dispatch implementation. See
`communication/decisions/ADR-004.md`.

## Future Expansion

Per Director instruction, every Architecture document from this point
states its impact on GoldBot's future direction, not only today's task:

**AI Impact**: The Navigation Event Bus (ADR-004) is the intended
future integration point for AI — an AI Assistant module (foundation
already exists: `assistant/`, `ai/conversation/`) would consume
`ScreenOpened`/`NavigationFailed` events to understand user context,
not call Navigation internals directly. No AI wiring exists today.

**Education Impact**: An Academy/Education module (`ai/learning/`
foundation exists per `docs/PHASE6_FREEZE.md` Stage 6's reservation
table) would register its own screens (e.g. `education.lesson.list`)
into the same dynamic Route Registry (ADR-003's decision), requiring
zero change to Navigation Core itself — this is exactly what "dynamic,
not static" (Director Decision 3 above) is for.

**Marketplace Impact**: Same shape as Education — a future Marketplace
module registers its own screens dynamically; Navigation Core does not
need to know Marketplace exists.

**Enterprise Impact**: Not applicable today — no enterprise/multi-tenant
concept exists anywhere in GoldBot. Flagged honestly as out of scope
rather than speculated on.

**Scalability**: A dynamic Registry (Director Decision 3) means adding
a new module's screens is an additive registration, not a Navigation
Core code change — the mechanism scales by design; whether any given
future module's *screen count* scales well is that module's own
concern, not Navigation's.

**Migration Risk**: Low for TASK-002C specifically (additive fields on
existing `platforms/` dataclasses, no existing behavior changed). The
real migration risk is deferred to a future, separately-approved task:
if `platform_layer/telegram/reply_keyboard_manager.py` is ever adapted to consume this
Registry internally, that adaptation is the actual risk point — not
this Architecture or Registry, which stay unwired.

## Related

- `docs/NAVIGATION_ANALYSIS.md` — the analysis this architecture builds on.
- `communication/decisions/ADR-001.md` through `ADR-004.md` — the
  governing decisions, including this document's own resolutions.
- `docs/constitution/CONSTITUTION.md` Article 13 — the Future First Principle.
- `docs/PLATFORM_WORKFLOW.md` — the Universal UI Abstraction rule and
  Director Questions requirement.
- `docs/PLATFORM_FOUNDATION.md` — `platform_layer/platform_service/navigation_model.py`/
  `menu_registry.py`/`capability_model.py`'s existing foundation this
  architecture extends.
- `communication/task_queue/TASK-002B.md` — this task's own record.
