# TradingView Provider — Design Audit (Phase 59.2, TASK 2)

**No code written in this task, per its own explicit instruction**
("Hozircha kod yozilmaydi. Faqat research."). This document is the
research output and design recommendation only.

## Question: what is TradingView actually usable for?

Two variants were considered:

```
Variant A                          Variant B
Signal/chart source only           Market data source

TradingView                        TradingView API
      |                                  |
      v                                  v
Analysis only                      GoldBot
```

## Research findings

### TradingView's own official position (tradingview.com)

TradingView's own Terms of Service, checked directly
(tradingview.com/policies/), are explicit: **except by separate
agreement, TradingView does not permit commercial usage of any of its
services or APIs**, and its prohibited uses list explicitly names
**automated trading, algorithmic trading, and creating products or
services based on TradingView content or any processing of
TradingView's content**. There is no official, general-purpose REST or
WebSocket market-data API that a third-party product like GoldBot
could legally consume for this purpose.

### What TradingView *does* offer officially: Pine Script alerts + webhooks

The one genuinely official, ToS-sanctioned automation path is
**outbound**, not inbound: a Pine Script strategy/indicator running on
TradingView's own charts can fire an `alert()`, which TradingView then
sends as an HTTP POST webhook (JSON body) to an external URL. This is
how TradingView positions third-party automation today — an alert
firing on a condition you already defined on their platform, not a
queryable historical-candle feed. Webhook alerts additionally require
2FA to be enabled on the account, and TradingView's own guidance warns
against putting credentials in the webhook payload.

This is fundamentally **Variant A** — TradingView is the analysis/
signal source, GoldBot would be a *receiver*, not a data consumer. It
cannot supply `get_candles()`/`get_latest_price()` in the
`MarketDataProvider` sense: there is no endpoint to query "give me the
last 200 M15 candles for XAUUSD" — only "notify me when a condition I
defined already fired."

### What exists but is NOT official: third-party "TradingView Data APIs"

Search results surfaced commercial third-party products (e.g.
"tradingviewapi.com") advertising REST/WebSocket access to
TradingView-sourced market data, with their own paid tiers (Free,
Pro $10/mo, Ultra, Mega — up to 2,500,000 requests/month with
"unlimited real-time streaming" on the top tier) and rate limits. **These
are not operated by TradingView** — they are unofficial resellers/
scrapers of TradingView-sourced data, layered with their own commercial
terms. Building `GoldBot` on top of one of these would mean:
- Depending on a data pipeline TradingView itself has not sanctioned
  for this use, with no guarantee of continued access, accuracy, or
  legality of the underlying scrape.
- Inheriting whatever ToS violation risk TradingView's own policy
  document already names (commercial/algorithmic use of their
  content) one layer removed, not eliminated — the reseller consuming
  TradingView's data commercially does not make GoldBot's own
  downstream use of it compliant.
- A real, un-disclosed commercial and legal risk for the project
  owner, not a technical limitation this codebase can engineer around.

## Recommendation

**Variant A only, and not as a `MarketDataProvider`.** TradingView
should not be built as a `data_layer/providers/tradingview_provider.py`
implementing `MarketDataProvider` (`get_candles()`/`get_latest_price()`)
in this codebase — there is no ToS-compliant way to source raw OHLC
candle history from TradingView for a commercial, automated product
like GoldBot. TwelveData (already live) and, in the future, MT5
(Phase 59.1's stub) remain the only sanctioned candle-data providers.

If TradingView is used at all in a future phase, its role would be
**inbound alert receiver** — an owner-configured Pine Script
alert/webhook landing on a GoldBot endpoint, functioning as an
additional signal/chart-annotation *input*, analogous to a manual
confirmation, never a `MarketDataProvider`. This would need its own,
differently-shaped contract (an alert payload, not a candle list) and
its own explicit approval — out of scope for this phase, and not
designed further here.

## Acceptance criterion status

"TradingView: ✅ design ready" is satisfied by this document's
conclusion — the design decision is **do not build a candle-data
TradingView provider**, backed by sourced research, not silence or an
assumption. No `tradingview_provider.py` exists, and none should be
added under the `MarketDataProvider` contract.

## Sources

- [Terms of Service and Company Policy — TradingView](https://www.tradingview.com/policies/)
- [How to configure webhook alerts — TradingView](https://www.tradingview.com/support/solutions/43000529348-how-to-configure-webhook-alerts/)
- [Alerts — Pine Script docs, TradingView](https://www.tradingview.com/pine-script-docs/faq/alerts/)
- [Stock Market API & Real-Time Financial Data | TradingView Data API (unofficial third-party product)](https://www.tradingviewapi.com/)
- [TradingView API Pricing (unofficial third-party product)](https://www.tradingviewapi.com/pricing/)
