# TASK-INFRA-001 — HTTP 403 Branch-Delete Block Diagnosis

**Question answered (with evidence, not guess):** *Which layer returns the
HTTP 403 on `git push origin --delete <branch>`?*

**Answer: the Claude Code (web) git-proxy — the Claude Environment layer.**
It scopes this session's git **writes** to its own designated branch
(`claude/code-analysis-optimization-pwfo3q`) and rejects any ref mutation
(including delete) to other branches. GitHub itself is **not** the blocker:
the GitHub identity is the repo **owner** with full rights.

---

## Layer table

| Layer | Status | Evidence |
|---|---|---|
| Constitution | **PASS** | `grep -rniE "branch.*delete\|delete.*branch\|force.push" docs/constitution/` → **no matches**. No rule forbids branch deletion. |
| Repository Policy | **PASS** | `docs/policies/BRANCH_MANAGEMENT_POLICY.md` *mandates* delete-after-merge (Rules 6, 11); it never restricts it. No other policy blocks delete. |
| GitHub Branch Protection / Ruleset | **PASS** | Deleted targets are unprotected `feature/*` (not `main`). Read path `GET info/refs` → **200 OK**. The 403 is not a GitHub ruleset message (no `422`, no "protected branch" body); it is a locally-generated git result (see Environment row). |
| GitHub Token Permission | **PASS** | `mcp__github__get_me` → `login: joni2551701-oss` = the **repository owner** (`public_repos:1`, the repo itself). Owner has inherent delete rights on the GitHub API. So permission is not lacking at GitHub. |
| GitHub App / API | **PASS (API) / N/A** | The GitHub API path (MCP, owner-authenticated) is fully authorized and independent of the git proxy. It is not the source of the 403. |
| MCP tooling | **BLOCK (no tool)** | The GitHub MCP toolset exposes `create_branch`, `create_or_update_file`, `delete_file`, `push_files` — but **no delete-branch / delete-ref / update-ref** tool. So even the authorized owner-API path has no *exposed* way to delete a ref from this session. This is a tooling gap, not a permission denial. |
| **Claude Environment (git-proxy)** | **BLOCK ← source of the 403** | `git remote -v` → `http://local_proxy@127.0.0.1:41729/git/joni2551701-oss/Gold-Bot`; `insteadOf https://github.com/` rewrites all git traffic through a local proxy (`gitConfigInjection:true`). Verbose trace: `GET .../info/refs?service=git-receive-pack` → **200** (read allowed); `POST .../git-receive-pack` (the delete payload) → **403 Forbidden**, `Server-Timing: x-originResponse;dur=10`. The **10 ms** response is far below a real GitHub.com round-trip (the read leg took `dur=235`), i.e. the 403 is generated at the proxy/infra shim, before reaching GitHub. Same session **can** push to its own branch — only foreign-ref writes 403. Matches the base rule "NEVER push to a different branch." |

---

## HTTP 403 — precise origin

Full receive-pack exchange (redacted):

```
GET  /git/joni2551701-oss/Gold-Bot/info/refs?service=git-receive-pack
  → 401 Www-Authenticate: Basic realm="Git Proxy"     (proxy auth challenge)
  → (retry with injected creds) → 200 OK               (read/advertise OK)
POST /git/joni2551701-oss/Gold-Bot/git-receive-pack
  → 403 Forbidden
     Content-Type: application/x-git-receive-pack-result
     Server-Timing: x-originResponse;dur=10            (10 ms → local shim)
error: RPC failed; HTTP 403 curl 22 ... returned error: 403
```

**Origin of the 403:** the **local git proxy at `127.0.0.1:41729`**
("Git Proxy" realm) — the Claude Code web sandbox's git egress layer.
It permits reads and writes to the session's own branch, and denies ref
mutations to any other branch. Not GitHub Ruleset, not a GitHub token
permission deficit, not the Constitution, not repo policy.

---

## Excluded layers (proven not the cause)

- **Constitution / Policy** — no rule exists; delete is even mandated.
- **GitHub token / ruleset** — identity is the repo **owner**; read path
  returns 200; owner has delete rights on the API.

## Most probable → confirmed source

**Claude Environment git-proxy write-scoping** (single, confirmed source),
with a **secondary** contributing gap: **no MCP delete-branch tool** exists,
so the authorized owner-API route is also not usable from this session.

---

## What unblocks it (where the real fix belongs)

The fix is at the **infrastructure/permission layer**, not the code, not
the Constitution:

1. **Owner deletes outside the sandbox** — GitHub UI *Branches* page, or
   `git push origin --delete <name>` / `DELETE /repos/.../git/refs/heads/<name>`
   with owner credentials. (Deletion list: `REPOSITORY_AUDIT_TASK_RESET_001.md` §4a.)
2. **Grant this session foreign-ref write scope** — if the Claude Code web
   environment's git proxy is configured to allow this repo's branch
   deletion, `TASK-RESET-001 §7A` re-runs and succeeds.
3. **Expose a delete-branch MCP tool** — would let the owner-authenticated
   API path delete refs directly.

No amount of retrying `git push --delete` from this session will change the
403 — it is a deliberate sandbox egress policy, not a transient fault.
