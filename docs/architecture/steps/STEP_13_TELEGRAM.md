# STEP-13 — `telegram/` Layer Architecture Specification

> **DOCUMENTATION ONLY.** Blueprint for the telegram step. No code here.
> `telegram/` is a mature layer with a hard architecture rule: **handlers →
> service → repository**; handlers never touch the DB. Navigation is the
> Reply Keyboard (Phase 6.3, Director-frozen). STEP-13 **extends** existing
> files — it deletes and duplicates nothing (Director's explicit rule:
> *"Mavjud fayllar bo'lsa: kengaytiriladi, o'chirilmaydi, duplicate qilinmaydi"*).

## 1. Purpose

Two additions, both extensions of existing modules:
1. **Current-price header** — every signal/status/market message is prefixed
   with a small header: **Symbol · Current Price · Session · Regime · Change**.
2. **Reply menu** — the persistent reply keyboard gains: 📈 Price · 📩 Signal ·
   🛰 Status · ℹ️ Market · ⚙️ Settings (📊 Chart reserved for later).

**Does:** read the latest price and render it above existing message bodies;
route the new reply buttons to existing commands. **Does NOT:** fetch a
provider (it reads the existing price store), compute a signal, or make a
trade decision.

## 2. Position in the flow

```
stream/current_price.py  (PricePoint, live single-value store)   ← anchor
        │  read-only
        ▼
market/current_price.py  (MarketPrice façade over stream)        ← reuse, no re-fetch
        │
        ▼
platform_layer/telegram/signal_formatter.py  (+ price header block)  ─┐
platform_layer/telegram/notification_service.py (prepend header)      ├─► outgoing message text
platform_layer/telegram/reply_keyboard_manager.py (📈📩🛰ℹ️⚙️ buttons) ─┘
        │
        ▼
telegram/command_router.route_command()  (reply-button label → existing /command)
```

## 3. Input / Output

- **Input:** a to-be-sent message (signal/status/market) + `symbol`; the
  latest `MarketPrice` (from `market/current_price.py`, which reads
  `stream/current_price.py`); session/regime from the existing context/market
  snapshot already available to the formatter.
- **Output:** the same message with a price-header block prepended; a reply
  keyboard carrying the new buttons; button taps mapped to existing commands.

## 4. File-by-file specification

| File | Role | Input | Output | Reads from | Passes to | New / Extend |
|---|---|---|---|---|---|---|
| `stream/current_price.py` | live single-value price store | provider tick | `PricePoint` | stream | market façade | **reuse** (TASK-CORE-004, unchanged) |
| `market/current_price.py` | market-facing price façade | stream store | `MarketPrice` | stream/current_price | telegram | **reuse** (TASK-CORE-005, unchanged) |
| `telegram/price_header.py` | build the `Symbol · Price · Session · Regime · Change` header string | `MarketPrice` + session/regime | header text | market/current_price | formatter/notify | **new** (only if no existing formatter helper fits — reuse audit first) |
| `platform_layer/telegram/signal_formatter.py` | signal message text | signal + models | `FormattedSignal` | decision/risk models | notify | **extend** (prepend header block; body unchanged) |
| `platform_layer/telegram/notification_service.py` | notification gate + send text | text + prefs | sent/skipped | UserRepository | Telegram | **extend** (prepend header on eligible sends) |
| `platform_layer/telegram/reply_keyboard_manager.py` | which reply keyboard per screen + button→command map | tier/screen | keyboard + mapping | keyboards | command_router | **extend** (add 📈/📩/🛰/ℹ️/⚙️ rows + reverse map) |
| `platform_layer/telegram/menu_commands.py` | native menu-button command list | tier/lang | `set_my_commands` | admin/user repo | Telegram | **extend** (register Price/Market entries if surfaced there too) |
| `platform_layer/telegram/command_router.py` | route a command (typed or button) | command | handler call | routers | handlers/services | **reuse** (new buttons map to existing commands — no new dispatch path) |
| `platform_layer/telegram/keyboards.py` | keyboard button definitions | — | keyboards | — | reply_keyboard_manager | **extend** (button labels only; tier logic unchanged) |
| `telegram/README.md` / `docs/telegram/TELEGRAM_ARCHITECTURE.md` | append STEP-13 section | — | — | — | — | **extend** |

### Existing files to EXTEND (reuse-first, no duplicates)
- `signal_formatter.py`, `notification_service.py`, `reply_keyboard_manager.py`,
  `menu_commands.py`, `keyboards.py` — extended in place.
- Price comes **only** from the existing `stream/current_price.py` via the
  `market/current_price.py` façade — no new fetch, no duplicate price store.
- New reply buttons route through the existing `command_router.route_command()`
  to commands that already exist — **no new dispatch path** (same pattern
  `menu_commands.py` already documents).

### Existing rule honoured
- **Handlers never touch the DB.** The header reads a price value object; any
  user/pref read stays in a service→repository call, as today.
- Navigation stays Reply-Keyboard-only; inline keyboards remain only for real
  choices (language, confirmation) — Phase 6.3 freeze unchanged.

## 5. Reply-menu button → existing command map (spec)

| Button | Routes to (existing) | Screen |
|---|---|---|
| 📈 Price | `/price` (current-price view) | price header + latest value |
| 📩 Signal | `/signals` (signal access) | latest signal(s) |
| 🛰 Status | `/status` (runtime/pipeline status) | status view |
| ℹ️ Market | `/market` (market overview) | session/regime/market |
| ⚙️ Settings | `/settings` (existing settings flow) | settings menu |
| 📊 Chart | *(reserved — later phase)* | — |

## 6. Boundary & safety
- No secret read/logged (bot token stays in `config.py`/`core/secrets.py`).
- No provider fetch, no signal/decision logic in `telegram/`.
- Owner-only sends stay owner-only; the notification-eligibility filter in
  `core/pipeline.py` (REJECT/BLOCKED signals never reach a user) is untouched.

## 7. Detailed flow

```
outgoing signal ──► signal_formatter.format(signal)          [body, unchanged]
   │
   ├─ price_header.build(market_current_price(symbol), session, regime)   [reuse stream price]
   │        │  "XAUUSD · 2412.5 · London · Trending ↑ · +0.4%"
   ▼        ▼
notification_service.send(header + "\n" + body, reply_keyboard_manager.for_screen(...))
                                   │  eligibility gate (unchanged)
                                   ▼
                              Telegram  (message + 📈📩🛰ℹ️⚙️ reply keyboard)
button tap ──► reply_keyboard_manager reverse-map ──► command_router.route_command("/price")  [existing]
```
