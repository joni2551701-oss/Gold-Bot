# Post‑Deploy Checklist — Current Price (`/price`) — TASK‑CORE‑004 Phase 1

Run this on the VPS **after** the feature is merged to `main` and
deployed. Executed by the Director / authorized operator (live steps need
egress to `api.telegram.org` + the market API, which CI cannot reach).
Feature commit: `7677b7f` (branch `feature/core-004-current-price-integration`).

**Feature contract being verified:** `/price` and the 💰 Current Price
button show the last known price for **XAU/USD**, read from the existing
production cache via `CurrentPriceProvider` — **never** an API call on
press. Read‑only / informational only.

## 0. Pre‑flight
- [ ] Deployed commit SHA on the VPS matches the merged `main` head.
- [ ] Service started cleanly (no traceback in logs).
- [ ] `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` present (never printed).

## 1. `/start`
- [ ] Send `/start` → bot responds; Main reply keyboard appears.
- [ ] Navigate to the **Signals** section → the **💰 Current Price**
      button is present alongside Live Signals / History / Premium.

## 2. `/price` (happy path)
- [ ] Send `/price` (or tap 💰 Current Price). Expected block:
      ```
      📊 Current Price
      🥇 XAU/USD
      Price:
      <number, 2 dp>
      Updated:
      <HH:MM:SS> UTC
      ```
- [ ] The price is a plausible XAU/USD value; the timestamp is the last
      **closed** candle time (matches what a signal for that candle used).

## 3. Cache WARM (populated)
- [ ] Ensure the pipeline has run at least once (so `.cache_state.json`
      holds candles). Send `/price` → shows the real price (§2).
- [ ] Press `/price` several times → **no** new market‑data fetch (see
      §11 log verification); response is instant.

## 4. Cache COLD (empty)
- [ ] With no cache (fresh env / deleted `.cache_state.json`), send
      `/price` → shows the localized empty state, **no crash**:
      ```
      Price is not available yet.
      Please wait for market data.
      ```

## 5. Restart / persistence (`.cache_state.json`)
- [ ] With a warm cache, note the `/price` value + timestamp.
- [ ] Restart the service.
- [ ] Send `/price` → the **same last value** is shown (loaded from
      `.cache_state.json` on startup) — persistence verified, and still
      **no** fetch on the press.

## 6. Localization (EN / UZ / RU)
- [ ] Set language via `/language` to each of EN, UZ, RU and send `/price`.
- [ ] The header, `Price:`/`Updated:` labels, the button label, and the
      empty‑state string are all localized; the number/timestamp are
      unchanged.

## 7. Empty cache (informational‑only guarantee)
- [ ] Covered by §4 — confirm the empty state never raises and never
      blocks the bot; other commands still work afterward.

## 8. Stale cache (by‑design behavior — confirm, don't "fix")
- [ ] With cache present but past its `expires_at` (e.g. market closed /
      pipeline idle), send `/price`.
- [ ] Expected: shows the **last known** price (possibly stale) with its
      real timestamp — it does **not** fetch to refresh. This is
      intentional (no API call on button press); the timestamp lets the
      user judge freshness. Confirm no fetch occurs (§11).

## 9. Invalid / unsupported symbol
- [ ] `/price` targets XAUUSD (the only tracked asset); there is no
      user‑supplied symbol argument, so a user cannot request an unknown
      one. (Unit‑level: an unknown symbol → empty state, already tested.)
- [ ] Confirm no error is surfaced for any `/price` invocation variant.

## 10. Latency
- [ ] Measure `/price` round‑trip. Expect **fast** (cache/memory read, no
      network). Record a rough figure; flag if it ever blocks on I/O
      (it should not).

## 11. Log verification (NO API call on press)
- [ ] Tail the service logs while pressing `/price` repeatedly.
- [ ] Confirm **no** `SmartDataCache` "Fetching new data…" line and **no**
      increase in the API request counter attributable to the press.
- [ ] Confirm the `CurrentPriceProvider` / `CurrentPriceService` log lines
      contain **no** token / chat_id / API key / internal object.

## 12. Rollback procedure
- [ ] The feature is **additive** (new files + limited Telegram wiring);
      to roll back: `git revert 7677b7f` on `main`, push, redeploy.
- [ ] After revert: `/price` no longer registered, the 💰 button is gone,
      and every other command is unchanged (verify `/start`, `/signal`).
- [ ] The MVP implementation is **untouched** and remains available as the
      reference; no MVP change is involved in this rollback.

## Sign‑off
- [ ] All sections pass → report to Director; Phase 2 may then be
      considered.
- [ ] Any failure → execute §12 rollback and report the failing section
      with logs. **Do not** proceed to Phase 2.
