══════════════════════════════════════════════════════════════════════════════
                    SENIOR TRADING AI
                 DEVELOPMENT STANDARDS
══════════════════════════════════════════════════════════════════════════════

Document ID
05_Development_Standards.md

Status
MASTER STANDARD

Priority
CRITICAL

Authority

This document defines the official development standards
for the Senior Trading AI Ecosystem.

Every implementation, refactor, feature, bug fix,
test and documentation update must follow this document.

If implementation conflicts with this standard,
implementation must stop.

══════════════════════════════════════════════════════════════════════════════
MISSION
══════════════════════════════════════════════════════════════════════════════

Development Standards exist to ensure that:

• Architecture remains stable.
• Code remains maintainable.
• Modules remain independent.
• Repository stays organized.
• Every change is traceable.
• Every feature is testable.
• Every refactor is reversible.

══════════════════════════════════════════════════════════════════════════════
DEVELOPMENT PRINCIPLES
══════════════════════════════════════════════════════════════════════════════

1.
Architecture First

Never write code before understanding
the architecture.

────────────────────────────────────────

2.
Reuse First

Existing modules must be reused whenever possible.

Creating duplicate logic is forbidden.

────────────────────────────────────────

3.
Single Responsibility

One module.

One responsibility.

────────────────────────────────────────

4.
Single Source of Truth

Never duplicate data ownership.

────────────────────────────────────────

5.
Minimal Change

Only modify what the task requires.

Avoid unrelated refactoring.

────────────────────────────────────────

6.
Backward Compatibility

Existing public behaviour must remain stable
unless explicitly approved.

────────────────────────────────────────

7.
Documentation First

If architecture changes,

documentation changes first.

══════════════════════════════════════════════════════════════════════════════
IMPLEMENTATION WORKFLOW
══════════════════════════════════════════════════════════════════════════════

Every implementation follows:

1.
Read Architecture

↓

2.
Read Repository Structure

↓

3.
Read Module Contracts

↓

4.
Read Data Flow Contracts

↓

5.
Audit Existing Code

↓

6.
Architecture Proposal (if required)

↓

7.
Owner Approval

↓

8.
Implementation

↓

9.
Tests

↓

10.
Documentation Update

↓

11.
Final Audit

↓

12.
Handover

══════════════════════════════════════════════════════════════════════════════
CODING RULES
══════════════════════════════════════════════════════════════════════════════

Worker must:

• Reuse existing code.
• Remove duplicate logic.
• Keep modules focused.
• Preserve public APIs.
• Write readable code.
• Keep imports clean.
• Keep naming consistent.

Worker must not:

• Mix responsibilities.
• Create hidden dependencies.
• Bypass architecture.
• Ignore existing modules.
• Introduce circular imports.

══════════════════════════════════════════════════════════════════════════════
REFACTORING RULES
══════════════════════════════════════════════════════════════════════════════

Before refactoring:

• Audit current implementation.
• Compare against architecture.
• Identify duplicates.
• Produce migration plan.
• Preserve existing behaviour.

Refactoring must never:

• Remove features.
• Break public APIs.
• Skip tests.
• Ignore documentation.

══════════════════════════════════════════════════════════════════════════════
TESTING STANDARD
══════════════════════════════════════════════════════════════════════════════

Every completed task must include:

• Unit Tests
• Integration Tests (when applicable)
• Existing test suite passes
• Smoke Test
• Import validation

Regression failures are not acceptable.

══════════════════════════════════════════════════════════════════════════════
DOCUMENTATION STANDARD
══════════════════════════════════════════════════════════════════════════════

When implementation changes:

Architecture

↓

Repository Structure

↓

Module Contract

↓

Data Flow

↓

Developer Documentation

must remain synchronized.

Documentation must never knowingly
contradict implementation.

══════════════════════════════════════════════════════════════════════════════
REPOSITORY RULES
══════════════════════════════════════════════════════════════════════════════

New modules:

• Must have a defined purpose.
• Must belong to one layer.
• Must follow repository structure.
• Must have documented ownership.

Unused modules:

• Audit
• Legacy
• Deprecated
• Delete

Never delete directly.

══════════════════════════════════════════════════════════════════════════════
TASK EXECUTION STANDARD
══════════════════════════════════════════════════════════════════════════════

Every task must define:

• Goal
• Scope
• Inputs
• Outputs
• Constraints
• Deliverables
• Acceptance Criteria

No implementation begins
without a defined task.

══════════════════════════════════════════════════════════════════════════════
REVIEW STANDARD
══════════════════════════════════════════════════════════════════════════════

Every completed task must answer:

• What changed?
• Why?
• Which modules were affected?
• Which tests passed?
• Which risks remain?
• Is architecture still respected?

══════════════════════════════════════════════════════════════════════════════
MIGRATION STANDARD
══════════════════════════════════════════════════════════════════════════════

Migration order:

Audit

↓

Canonical Module

↓

Migration

↓

Compatibility

↓

Legacy

↓

Deprecated

↓

Delete

Delete is always the final step.

══════════════════════════════════════════════════════════════════════════════
QUALITY GATES
══════════════════════════════════════════════════════════════════════════════

Before completion:

✓ Architecture verified

✓ Repository verified

✓ Module contracts respected

✓ Data flow respected

✓ Tests passed

✓ Documentation updated

✓ No duplicate logic

✓ No circular dependency

✓ No feature loss

══════════════════════════════════════════════════════════════════════════════
WORKER RESPONSIBILITIES
══════════════════════════════════════════════════════════════════════════════

Worker must:

• Audit before coding.
• Stop when architecture is unclear.
• Report conflicts.
• Preserve compatibility.
• Leave a complete handover.

Worker must never:

• Guess architecture.
• Ignore standards.
• Hide refactoring.
• Change module responsibilities.
• Skip validation.

══════════════════════════════════════════════════════════════════════════════
OWNER RESPONSIBILITIES
══════════════════════════════════════════════════════════════════════════════

Owner is responsible for:

• Approving architecture.
• Resolving conflicts.
• Approving migration.
• Approving module contracts.
• Approving destructive changes.
• Final acceptance.

══════════════════════════════════════════════════════════════════════════════
FINAL LAW
══════════════════════════════════════════════════════════════════════════════

Every implementation must satisfy:

01_Ecosystem_Architecture.md

↓

02_Repository_Structure.md

↓

03_Module_Contracts.md

↓

04_Data_Flow_Contracts.md

↓

05_Development_Standards.md

Architecture defines the system.

Repository defines location.

Contracts define responsibility.

Data Flow defines movement.

Development Standards define how the system evolves.