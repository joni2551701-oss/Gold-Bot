# 03 — Haqiqiy narx oqimi dalili (CI 3-update log)

**Holat: PLACEHOLDER — orkestrator to'ldiradi.**

Haqiqiy dalil sandboxdan emas, CI `workflow_dispatch` (`real_data_probe`
job) dan keladi. Bu yerga `scripts/verification/real_price_stream_probe.py`
ning CI chiqishi (3 ta yangilanish) joylashtiriladi.

Har bir yangilanish uchun kutiladigan maydonlar:
`provider_price`, `validated_price`, `memory_price`, `timestamp`,
`validated`, `memory`, `equality_chain`, `event_published`.

## PASS sharti (qat'iy)

- 3/3 yangilanishda real `provider_price` keldi, VA
- 3/3 da tenglik zanjiri `provider_price == validated_price ==
  memory_price` (`equality_chain=PASS`).

Aks holda → **BLOCKED + Director Review** (workaround YO'Q). Agar CI da
`/price` endpoint ishlamasa (plan cheklovi, kutilmagan shakl, xato),
to'g'ri natija — BLOCKED, real sabab bilan (`tick_error` klass nomi).

```
(CI PROBE OUTPUT — TO BE INSERTED BY ORCHESTRATOR)
```
