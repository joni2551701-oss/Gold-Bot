# 04 — Validatsiya va Market Memory tenglik zanjiri

## Oqim (o'zgarmagan arxitektura)

```
TwelveDataPriceSource.read()  -> StreamEvent(price=real current price)
  -> PriceStream._forward_ordered
       -> StreamValidator.validate   (yaroqsiz tick tashlanadi)
       -> _PriceTickSink.on_event
            -> PriceCache.update             (validated price)
            -> EventBus.publish(PRICE_UPDATED, PriceTick)
            -> CandleBuilder.on_event        (yagona yozuvchi -> MarketMemory)
```

## Tenglik zanjiri

Bir tick uchun:

- **provider_price** — manba `read()` bergan narx.
- **validated_price** — `StreamValidator` dan o'tib `PriceCache` ga tushgan
  narx (`PriceStreamService.get_price(...).price`). Tick faqat validatsiyadan
  o'tsa cache'ga tushadi, shu sabab provider va validated bir xil kuzatuv.
- **memory_price** — `MemoryReader.get_forming("XAUUSD","M1").close` — bitta
  tick M1 forming-candle'ga buklanganda close = tick narx.

Probe har yangilanishda `provider_price == validated_price == memory_price`
ni tekshiradi (`equality_chain`). PASS uchun 3/3 zanjir mos kelishi kerak.

Yaroqsiz tick (masalan manfiy narx) validator tomonidan tashlanadi va
cache'ga umuman tushmaydi — mavjud `test_build_default_wires_validator_
that_drops_invalid_ticks` buni tasdiqlaydi.
