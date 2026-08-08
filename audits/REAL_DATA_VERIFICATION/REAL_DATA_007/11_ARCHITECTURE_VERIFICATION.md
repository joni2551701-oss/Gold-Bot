# REAL-DATA-007 — 11. Architecture Verification

## Layer/kontrakt yaxlitligi
- `TwelveDataProvider` `data/` dan yuqori qatlamlarni import qilmaydi
  (`twelve_data_provider.py:15` docstring va importlar).
- `CurrentPriceProvider` read-only seam: Telegram → CurrentPriceProvider →
  PriceStreamService.get_price() (`current_price_provider.py:6-13`);
  Telegram cache/service'ni to'g'ridan o'qimaydi (Direktor buyrug'i).
- `BitgetPriceSource`/`TwelveDataProvider` DD-048: har bir vendorni
  biladigan yagona joy PriceProvider adapteri.

## Production driver (tick)
`platform_layer/telegram/polling.py:308`:
```
get_shared_price_stream_service().tick(datetime.now(timezone.utc))
```
`_price_stream_tick_loop()` (:287) jonli Telegram jarayonida tick()'ni
haydaydi — REAL-DATA-006'da tasdiqlangan production driver.

## STALE hujjat topilmasi (kod emas)
`price_stream_service.py` docstring: *"nothing drives tick() in production"*
— bu **STALE (eskirgan)**. Amalda polling.py:308 production'da tick()'ni
haydaydi. (Bu hujjat nuqsoni; audit-only bo'lgani uchun bu passda
tuzatilmadi — Worker Authority bo'yicha keyingi hujjat evolyutsiyasida
tuzatilishi mumkin.)

## Foundation Freeze
Provider path candle MarketDataProvider tanlaydi (`04`); yangi API
arxitekturasi qo'shilmadi. Foundation Freeze saqlangan.

## Xulosa
Arxitektura layer chegaralari to'g'ri va buzilmagan. Yagona ochiq
nomuvofiqlik — stale docstring (hujjat, kod emas). Price Stream candle
polling sifatida arxitektura jihatidan izchil, lekin "real-time stream"
sifatida noto'g'ri nomlangan.
