# TASK-INFRA-001 — HTTP 403 Branch-Delete Block Diagnosis

**Question answered (with evidence, not guess):** *Which layer returns the
HTTP 403 on `git push origin --delete <branch>`?*

**Answer: the Claude Code (web) git-proxy — the Claude Environment layer.**
It scopes this session's git **writes** to its own designated branch
(`claude/code-analysis-optimization-pwfo3q`) and rejects any ref mutation
(including delete) to other branches. GitHub itself is **not** the blocker:
the GitHub identity is the repo **owner** with full rights.

---

## Layer table — every candidate restriction layer, checked with evidence

| # | Layer | Status | Evidence (verified this session) |
|---|---|---|---|
| 1 | Constitution | **PASS (not the cause)** | `grep -rniE "branch.*delete\|delete.*branch\|force.push" docs/constitution/` → **no matches**. No Article forbids branch deletion. |
| 2 | Repository Policy | **PASS** | `docs/policies/BRANCH_MANAGEMENT_POLICY.md` *mandates* delete-after-merge (Rules 6, 11); never restricts it. No other `docs/policies/*` blocks delete. |
| 3 | Freeze / Lock / Block (governance state) | **PASS** | `grep -rniE "branch.*(freez\|lock\|block\|forbid)\|delete.*forbidden" docs/` → only hits are the policy *mandating* delete and "forbids long-lived branches / forbids branching off each other" — **no freeze or lock forbids the delete operation**. No Phase-Freeze doc restricts VCS branch ops. |
| 4 | GitHub Branch Protection / Ruleset | **PASS (conclusive)** | `mcp__github__list_branches` (81 branches + main): **every branch `"protected": false`, including `main`**. No protection/ruleset exists anywhere in the repo. If protection caused the 403, the target refs would be `protected:true` — they are not. |
| 5 | GitHub Token Permission | **PASS** | `mcp__github__get_me` → `login: joni2551701-oss` = the **repository owner**. Owner holds inherent delete rights on the GitHub API. Read leg `GET info/refs` → **200 OK** confirms the credential authenticates and is authorized to read. |
| 6 | GitHub App / API path | **PASS (API) / N/A** | The MCP GitHub path is owner-authenticated and independent of the git proxy; it is authorized and not the source of the 403. |
| 7 | Sandbox network egress | **PASS** | Proxy `status`: `recentRelayFailures: []`, `selective:false`, `toolScoped:false`. The GitHub host is reachable — the read leg returned **200**. Egress policy is **not** blocking (an egress denial would fail the read too, and would be a 403/407 on the *host*, not on the receive-pack verb). |
| 8 | MCP tooling | **BLOCK (secondary — tool gap)** | GitHub MCP exposes `create_branch`, `create_or_update_file`, `delete_file`, `push_files` — but **no delete-branch / delete-ref / update-ref** tool. The authorized owner-API path therefore has no *exposed* delete-ref action. A tooling gap, not a permission denial. |
| 9 | Session policy (harness directive) | **BEHAVIORAL constraint (not the HTTP 403)** | Base session directive: "Develop on `claude/code-analysis-optimization-pwfo3q`" + "**NEVER push to a different branch without explicit permission**." This constrains *me*, not the wire. It is the human-readable twin of the proxy rule in #10, but it does not itself emit HTTP. |
| 10 | **Claude Environment git-proxy** | **BLOCK ← the source of the HTTP 403** | `git remote -v` → `http://local_proxy@127.0.0.1:41729/git/...`; `insteadOf https://github.com/` routes all git through the local proxy (`gitConfigInjection:true`). Verbose trace: `GET .../info/refs?service=git-receive-pack` → **200** (read allowed); `POST .../git-receive-pack` (delete payload) → **403 Forbidden**, `Server-Timing: x-originResponse;dur=10`. **10 ms** ≪ a real GitHub round-trip (read leg was `dur=235`) → the 403 is emitted at the proxy/infra shim, before reaching GitHub. **Discriminator:** the *same* proxy/session pushed successfully to its own branch (`effed1d..d4b8082`, this session) but 403s a foreign-ref delete → the decision is **per-ref, at the proxy**, scoping writes to the session's own branch. |

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

## Excluded layers (proven NOT the cause — evidence-based)

| Excluded layer | Disproving evidence |
|---|---|
| Constitution | grep: no branch-delete rule |
| Repository Policy | policy *mandates* delete |
| Freeze / Lock / Block | grep: no freeze/lock forbids the delete op |
| GitHub Branch Protection / Ruleset | `list_branches`: **all `protected:false`, incl. main** |
| GitHub Token Permission | `get_me`: identity is repo **owner**; read → 200 |
| Sandbox egress | `recentRelayFailures:[]`; host reachable; read → 200 |
| Session policy (harness) | behavioral directive only — emits no HTTP |

## Confirmed source (single)

**Layer 10 — the Claude Environment git-proxy** returns the HTTP 403,
scoping this session's git **writes** to its own branch and rejecting
foreign-ref mutations (delete included) with a locally-generated
`403` (`dur=10 ms`). Proven by the own-branch-push-succeeds /
foreign-ref-delete-403 discriminator on the *same* proxy and session.

**Secondary (not the 403, but also blocks the API route):** no MCP
delete-branch tool exists, so even the owner-authorized GitHub API path
has no exposed way to delete a ref from here.

Layer 9 (session policy) is the human-readable *intent* behind Layer 10;
they agree, but only Layer 10 emits the HTTP 403.

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
