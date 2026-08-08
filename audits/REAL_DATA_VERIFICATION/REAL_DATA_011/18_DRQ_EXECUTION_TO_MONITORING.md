# 18 — DRQ — Execution → Monitoring (REAL-DATA-011)

**DRQ turi:** Director Review Question / wiring decision.
**Holat:** NOT WIRED. Bu passda QURILMADI.

## Bir jumlalik so'rov

Director ruxsat beradimi — execution fill hodisasini Monitoring
qatlamiga uzatuvchi (fill → monitor handoff) contract'ni qurishga
(hozir handoff YO'Q, execution inert)?

## Kontekst

- `execution_layer/` inert — real fill ishlab chiqarilmaydi.
- Monitoring qatlami FOUNDATION sifatida mavjud, ammo fill→monitor
  bog'lovchi contract YO'Q (REAL-DATA-010/07_).

## Nega DRQ

Bu Production Execution (17_) DRQ'siga bog'liq — fill bo'lmasa
monitoring handoff'ining ma'nosi yo'q. Execution wiring qaroridan
keyin ko'rib chiqiladi. Yangi wiring = Director qarori.

## Tavsiya

17_ (Production Execution) DRQ tasdiqlangandan keyingina, bitta RFC
ichida "Execution → Monitoring handoff" sifatida rasmiylashtirish.
Bu passda mustaqil qurilmaydi.
