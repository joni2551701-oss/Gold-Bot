# Navigation Architecture (TASK-002B)

Step 2 of `docs/PLATFORM_WORKFLOW.md`'s "Architecture First" process.
**Architecture only — no implementation, code, or public API exists
after this document.** Every proposal below is a design for Director
review; nothing here is built until TASK-002C (Registry) is
authorized, which does not happen until this document is approved.

Governed by `communication/decisions/ADR-001.md` and Constitution
Article 13 (Future First Principle): every component below states its
compatibility across all five target platforms — Telegram Bot,
Telegram Mini App, Android, iOS, Desktop — using
`platforms/capability_model.py`'s existing `SupportStatus` contract
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
`platforms/navigation_model.py`'s existing `NavigationNode` (id,
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
(`telegram/reply_keyboard_manager.py`) with an *explicit* directed
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
type). Extends `platforms/menu_registry.py`'s existing `MenuRegistry`
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
`telegram/permissions.py`'s `PermissionLevel` (OWNER/ADMIN/USER) values
by convention, the same "by convention, not by import" relationship
`platforms/navigation_model.py`'s `permission` field already has today
(TASK-001). The Navigation Graph itself, not each client individually,
is what checks a Screen's required tier against the resolved value —
centralizing the *check*, not the *resolution*.

| Platform | Status | Reason |
|---|---|---|
| Telegram Bot | SUPPORTED | `telegram/permissions.py`'s existing `PermissionLevel`/`get_permission_level()` already resolves this; nothing to build, only to reference by convention. |
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
to a real client screen. `telegram/reply_keyboard_manager.py` and
`telegram/keyboards.py` are, conceptually, *today's entire Platform
Adapter for Telegram* — already built, already tested
(`tests/telegram/test_keyboards.py`, 38 tests) — but this Architecture
does **not** propose modifying them; a future, separately-approved
task decides whether/how they come to consume the graph described
here internally, without changing their external behavior (Phase 6
Freeze stands).

| Platform | Status | Reason |
|---|---|---|
| Telegram Bot | SUPPORTED | Already exists today (`telegram/reply_keyboard_manager.py`), just not yet connected to a shared graph — connecting it is explicitly out of scope for this Architecture. |
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
| Telegram Bot | SUPPORTED | Already implemented this way (`_LAST_SECTION` in `telegram/reply_keyboard_manager.py`). |
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
`platforms/capability_model.py`/`capability_registry.py`/
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

## Director Questions

1. **Back Stack (§5)** — do you approve modeling Telegram's flat
   Back-to-Main behavior as a depth-1-collapsing special case of a
   real, arbitrary-depth stack, or should Telegram's model be treated
   as fundamentally different (not a special case of the same
   structure)?
2. **Navigation State (§9)** — do you approve keeping navigation
   position per-client/session (never centralized in `database/`), as
   proposed?
3. **Permission Layer (§7)** — this proposes a future platform-agnostic
   tier concept alongside `telegram/permissions.py`'s existing
   `PermissionLevel`. Should that eventually become a real, separate
   contract (a "new public API" under the No Silent Decisions Policy,
   requiring its own `PROPOSED-DECISION-XXXX.md` before TASK-002D), or
   should `telegram/permissions.py`'s enum simply be reused directly
   once cross-platform code needs it?
4. **Deep Link System (§6)** — this component has zero existing
   foundation and no near-term client to serve. Should it stay in
   TASK-002's scope, or move to its own later task so Navigation's
   core (Screen Model/Graph/Route Registry/Back Stack) isn't blocked
   waiting on it?
5. **Screen Lifecycle (§12)** — do you approve treating Telegram as a
   genuine degenerate case (no Backgrounded state) rather than forcing
   a synthetic lifecycle onto it?
6. **TASK-002C scope check** — should Navigation Registry (002C)
   populate the graph with GoldBot's real, current Telegram tree
   (Main/Settings/Admin/Owner/Profile/Signals) as a **read-only
   mirror only** (matching `docs/PLATFORM_FOUNDATION.md`'s own
   "Future Improvements" note), with zero change to
   `telegram/reply_keyboard_manager.py`'s live behavior — confirming
   this is still the intended scope before 002C starts?

## Related

- `docs/NAVIGATION_ANALYSIS.md` — the analysis this architecture builds on.
- `communication/decisions/ADR-001.md` — the governing decision.
- `docs/constitution/CONSTITUTION.md` Article 13 — the Future First Principle.
- `docs/PLATFORM_WORKFLOW.md` — the Universal UI Abstraction rule and
  Director Questions requirement.
- `docs/PLATFORM_FOUNDATION.md` — `platforms/navigation_model.py`/
  `menu_registry.py`/`capability_model.py`'s existing foundation this
  architecture extends.
- `communication/task_queue/TASK-002B.md` — this task's own record.
