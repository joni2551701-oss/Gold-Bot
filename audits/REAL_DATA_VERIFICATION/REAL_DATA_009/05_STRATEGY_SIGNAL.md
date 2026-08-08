# 05 — Strategy → Signal — REAL-DATA-009

## Transition

Strategy → Signal (SignalEngine orchestration; Signal contract).

- **INPUT:** strategiyalar ishlab chiqargan `SignalCandidate` obyektlari
  (`signal_layer/signal_builder/models.py`) — `pipeline.py:405`.
- **PROCESSING:** `SignalEngine.generate_signals()` candidate ro'yxatini
  yig'adi. So'ng har candidate `from_signal_candidate(...)` orqali
  portable `SignalSchema`ga aylantiriladi (`pipeline.py:519`,
  `signal_layer/signal_builder/adapter.py`).
- **OUTPUT:** `signal_candidates` (`pipeline.py:405`) va keyinroq
  `signal_history: List[SignalSchema]` (`pipeline.py:519`).
- **NEXT CONSUMER:** DecisionEngine (`pipeline.py:487`).

## Signal contract (SignalSchema — file:line)

`signal_layer/signal_builder/schema.py`:
- `symbol: str` — `schema.py:102`
- `direction: str` (ALLOWED_DIRECTIONS) — `schema.py:104`
- `entry_price: Optional[float]` — `schema.py:109`
- `stop_loss: Optional[float]` — `schema.py:110`
- `take_profit: Optional[float]` — `schema.py:111`
- `confidence_score: Optional[float]` — `schema.py:116`

`validate_signal()` (`schema.py:159+`) majburiy maydonlar, direction
va BUY/SELL uchun narx tartibini tekshiradi (`schema.py:186-187`).

## Ownership

SignalEngine — signal orkestratsiyasi egasi;
`signal_layer/signal_builder/` — Signal contract egasi.

## Real runtime dalil

Run `31240675527`: 1 candidate (FVG_STRATEGY, BUY), grade B, score 40.

## Status: PASS
</content>
