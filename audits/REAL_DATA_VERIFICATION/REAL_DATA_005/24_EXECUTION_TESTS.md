# 24 — Execution & Monitoring Tests (REAL-DATA-005)

## Test katalogi va klassifikatsiyasi

| Test fayl | Tur | Real order? | Izoh |
|---|---|---|---|
| `tests/execution/simulator/test_simulator_engine.py` | Safe-runtime (real app path) | YO'Q | Real `RiskResult` + real `PaperTrade`, mock YO'Q (`:2-3`); safe simulated fill |
| `tests/lifecycle/test_paper_trade.py` | Unit/Integration (contract) | YO'Q | PaperTrade state machine transitions |
| `tests/lifecycle/test_paper_trade_monitor.py` | Safe-runtime | YO'Q | Real candle arifmetikasi orqali TP/SL/EXPIRED |
| `tests/lifecycle/test_signal_lifecycle_state.py` | Unit | YO'Q | Lifecycle state |
| `tests/phase59/test_phase59_foundation.py` | Integration | YO'Q | Foundation wiring |
| `tests/backtesting/test_backtest_engine.py` | E2E (backtest chain) | YO'Q | paper_trade→monitor backtest zanjiri |
| `tests/analytics/test_signal_performance.py` | Unit | YO'Q | Analytics |

**Production-Probe (real broker) = YO'Q** — ataylab, taqiqlangan.

## Klassifikatsiya izohi

- **Unit=mock, Integration=contract, Safe-runtime=real app path no real
  order, Production-Probe=real broker (yo'q — forbidden), E2E=full
  chain.**
- Mock testlar real execution isboti EMAS. Ammo
  `test_simulator_engine.py` **mock ishlatmaydi** (real RiskResult +
  real PaperTrade), shu bois u Safe-runtime evidence sifatida
  hisoblanadi — real broker order emas, lekin real app kod yo'li.

## Ishga tushirilgan (bu audit)

```
python -m pytest tests/execution/ tests/lifecycle/ -q
→ 76 passed in 5.37s
```

```
python -m pytest tests/ -q
→ 5493 passed in 72.13s
```

Full suite 5493 — o'zgarishsiz (talab qilingan invariant saqlandi).

**Testlar = PASS. Real execution proof = faqat Safe-runtime darajasida
(no real order); live-runtime Execution→Monitoring uchun test YO'Q,
chunki u wired emas.**
</content>
