# 12 — Real Runtime Evidence — REAL-DATA-009

## Manba

REAL-DATA-004 haqiqiy main.py runtime run — **CI run `31240675527`,
commit `ea3d055`** — real TwelveData XAU/USD (200 candle). Ushbu audit
uni qayta ishlatadi (order talabi: CI qayta dispatch qilinmaydi).

## Stage log (real data)

```
stage=market_data     Fetched 200 candles        (0.466s, real API)
stage=data_quality    valid=True score=100.00
stage=htf_bias        NEUTRAL conf=50 quality=0.67 timeframes=['H4','H1']
                      (Daily parse FAILED -- alohida finding, pastda)
stage=context         (ran)
stage=market_phase    MARKUP (TRENDING BULLISH)
stage=signal          Generated 1 signal candidate(s)   [FVG_STRATEGY, BUY]
stage=signal_quality  grade=B score=40 criteria=[STRUCTURE_ALIGNED, FVG_ALIGNED]
stage=features        [('TRENDING','LONDON_NEW_YORK_OVERLAP','B')]
stage=ai              approved=False confidence=0.00 risk_score=1.00 (heuristic stub)
stage=decision        Produced 1 trade decision(s)
stage=risk            Produced 1 risk result(s)          [RiskManager.evaluate() ran]
stage=signal_history  1 record linked to context snapshot b1b6fcee-...
stage=telegram_format Produced 0 telegram message(s)     (AI approved=False -> not eligible)
stage=telegram_delivery Sent 0/0
stage=database        Persisted 1 signal record(s)
```

## Isbot qilingan zanjir

Core → Context → market_phase(MARKUP) → Signal(FVG_STRATEGY) →
signal_quality(B) → features → AI(advisory, rad etdi) → Decision →
Risk(RiskManager.evaluate ishladi) → signal_history → telegram_format →
database — barchasi real XAU/USD data bilan.

## 0-message tushuntirish

`telegram_format` 0 xabar — AI signalni rad etdi (approved=False) →
notification-eligibility filtri (`pipeline.py:550`) candidate'ni
o'tkazmadi. Bu Trading Safety filtri to'g'ri ishlagani, xatolik emas.

## Ma'lum finding (tuzatilmaydi — order talabi)

Daily timeframe parse bug: `TwelveDataClient.fetch_candles()`
(`data_layer/providers/twelve_data_client/twelve_data_client.py:112`)
Daily uchun date-only formatni parse qilolmaydi → HTF Daily yo'qoladi
(H4/H1 ishlatildi, quality 0.67). Context-only, trading qarorini
bloklamaydi. Keyingi Sprint uchun Director qaroriga havola.

## Status: PASS (data→risk real runtime bilan)
</content>
