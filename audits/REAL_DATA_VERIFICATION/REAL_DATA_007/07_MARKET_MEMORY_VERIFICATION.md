# REAL-DATA-007 — 07. Market Memory Verification

## Tekshirilgan
`price_stream_service.py` → Market Memory yozuv yo'li (single-writer fold).

## Dalillar
- `PriceStreamService.__init__` `memory_registry` qabul qiladi
  (`price_stream_service.py:120-128`); `register_source()` supplied bo'lsa
  per-asset CandleBuilder quradi (docstring :33, :123).
- Yozuv single-writer: CandleBuilder yagona yozuvchi (REAL-DATA-006 05
  topilmasi bilan mos). Memory yozuvi fail-safe — CandleBuilder xatosi
  stream'ga yoki cache'ga yetib bormaydi (service docstring).
- Default (registry berilmagan) holatda — Phase 3 `CurrentPriceProvider`
  yo'li — hech qanday memory obyekti qurilmaydi (docstring: "byte-for-byte
  as before").

## Muhim izoh
Market Memory yozuv yo'li REAL va to'g'ri (single-writer). Ammo upstream
BLOCKED (M1) tufayli production'da real candle memory'ga oqmaydi.

## Xulosa
Market Memory qatlami arxitektura jihatidan to'g'ri (single-writer,
fail-safe), lekin candle-polling upstream nuqsoni tufayli real ma'lumot
bilan to'lmaydi.
