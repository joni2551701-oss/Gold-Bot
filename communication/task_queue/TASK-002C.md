# TASK-002C

**Title**: Navigation Registry
**Status**: ✅ APPROVED. **Freeze: ✅ YES — Frozen from this point.**
No refactoring or new capability added to this task's own content
except for a critical bug, a security issue, a Director-approved ADR,
or a future Migration Task (`communication/decisions/ADR-005.md`).

## Freeze Checklist

```
Freeze Checklist
☑ CI Passed              -- ci.yml run #155, commit 4784a18, success
☑ Tests Passed            -- 15 new (39 total in tests/platforms/), full suite 4648/4648
☑ Documentation Updated   -- docs/PLATFORM_FOUNDATION.md (Documentation Policy)
☑ ADR Updated (if required) -- ADR-002/003/004 already recorded at TASK-002B; none new at 002C itself
☑ Constitution Impact Reviewed -- none; no new Article, Article 13 already covers this work
☑ Public Contracts Reviewed -- additive only (target_bindings/category/content_type fields); no existing field removed or retyped
☑ Backward Compatibility Checked -- is_valid_screen_id() not enforced retroactively on TASK-001's registrations (ADR-005's own precedent)
☑ No Silent Decisions     -- every design choice traces to Director-approved ADR-002/003/004 or the TASK-002C rule list itself
☑ Director Approval       -- this review
☑ Freeze Applied          -- this document
```

## Objective

Build the Screen/Route Registry — dynamic, universal-ID-keyed,
extensible for modules that don't exist yet — plus the Navigation
Event Bus's interface (contract only). Per Director's explicit rule
list for this task:

- No hardcoded screens or dispatch tables.
- No `telegram/` import or Telegram-callback dependency anywhere in
  `platforms/` (unchanged boundary from TASK-001).
- No platform-specific code — the Registry stores platform-agnostic
  data plus per-platform target bindings, never platform-native types.
- Universal Screen ID used (ADR-002's `<category>.<name>` convention).
- Dynamic Registry used (register/get/list — the same mechanism
  `platform_layer/platform_service/menu_registry.py`'s `MenuRegistry` already has from
  TASK-001, extended, not replaced).
- Navigation Event Bus interface prepared — event vocabulary only
  (ADR-004), no dispatch/pub-sub implementation.
- Extensible for future modules (AI, Education, Marketplace, Trading)
  — the Registry mechanism must not assume today's known categories
  are the only ones that will ever exist.

## Depends on

TASK-002B (Navigation Architecture) — Approved.

## Notes

Populates the Registry with GoldBot's real, currently-live Telegram
screens only (Main/Settings/Admin/Owner/Profile/Signals, per
`docs/PLATFORM_ARCHITECTURE.md` §5) under the new Universal Screen ID
convention — no invented AI/Education/Marketplace screens (those
modules don't exist; the Registry mechanism being open to them is not
the same as pre-registering fictitious entries for them, which would
violate this repo's "no fabricated documentation/content" convention).
Zero change to `platform_layer/telegram/reply_keyboard_manager.py`'s live behavior —
this remains a foundation-only mirror, per ADR-003 (a platform never
creates a Screen, it only calls Navigation — today's Telegram code
still creates its own Reply Keyboards directly, unchanged, until a
future, separately-approved task adapts it).
