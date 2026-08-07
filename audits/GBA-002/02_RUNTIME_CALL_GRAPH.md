# GBA-002 — TASK-01: Runtime Call Graph (AI -> Media -> Telegram?)

## Metodologiya

Har bir call site'dan boshlab, chaqirilgan funksiya/klassning o'z
tanasi ichiga kirib, u yerdan yana nima chaqirilishini kuzatib
bordik — `platform_layer/telegram/`ga yoki har qanday tarmoq/SDK
qatlamiga chiquvchi yo'l bor-yo'qligini aniqlash uchun.

## Zanjir 1 — `broadcast_asset_from_content_and_media()`

Fayl: `media_layer/telegram_broadcast/broadcast_adapter.py:35`.

Funksiya tanasi faqat `ContentResult` + `MediaAsset`dan
`BroadcastAsset` (dataclass, DRAFT holatida) quradi — hech qanday
tashqi chaqiruv, hech qanday I/O, hech qanday `platform_layer`
importi. Fayl docstring'i (satr 20 atrofida) buni o'zi ham tasdiqlaydi:
`ai_layer.ai_service.content.broadcast_output.BroadcastReadyContent`
bilan ishlaydi, faqat DTO transformatsiyasi.

## Zanjir 2 — `BroadcastManager.prepare_broadcast()`

Fayl: `media_layer/telegram_broadcast/broadcast_manager.py:101-106`.

```python
def prepare_broadcast(self, asset: BroadcastAsset) -> BroadcastAsset:
    new_status = BroadcastStatus.READY if self.validate_broadcast(asset) else BroadcastStatus.FAILED
    updated = replace(asset, status=new_status)
    self._assets[updated.id] = updated
    return updated
```

- `validate_broadcast()` (satr 97-99) — deterministik bool tekshiruv
  (`content_id` va `media_id` bo'sh emasligini tekshiradi), tashqi
  chaqiruv yo'q.
- Natija shunchaki xotiradagi `self._assets: Dict[str, BroadcastAsset]`
  lug'atiga yoziladi (in-memory state, DB yozuvi ham yo'q).
- Klass docstring'i (`broadcast_manager.py:1-23`) o'zi ochiq tan oladi:
  *"None of the five methods send anything anywhere ... No network
  call, no SDK, no streaming library import anywhere in this class
  (Rule 2)"*.

## `media_layer/telegram_broadcast/` butun submodulida `platform_layer` importi bormi?

```
$ grep -rn "platform_layer" media_layer/telegram_broadcast/*.py
(natija: 0 ta)
```

Faqat `IMPLEMENTATION.md:53` (kod emas, hujjat) shu haqida gapiradi:
*"Not wired into `platform_layer/telegram/owner/broadcast_commands.py`
yet"* — ya'ni real Telegram send hali umuman mavjud emas, hujjat
darajasida ham ochiq tan olingan.

## Zanjir 3 — `BroadcastManager.prepare()` (Phase 63.0 asl metodi)

`prepare()` (satr 53-73) faqat `BroadcastRequest` value quradi va
qaytaradi; docstring: *"A future, separately-approved delivery layer
is the only thing that would ever act on this value."* Ya'ni hozircha
hech kim (na `ai_layer`, na `media_layer`ning o'zi) bu value'ni olib
`platform_layer/telegram/`ga yubormaydi — bunday delivery qatlami
kodda hali mavjud emas.

## Yakuniy zanjir xaritasi

```
ai_layer (4 fayl)
   --DTO qurish--> media_layer.telegram_broadcast.broadcast_adapter
                       (BroadcastAsset, faqat data)
   --holat o'tkazish--> media_layer.telegram_broadcast.broadcast_manager
                       .prepare_broadcast() (in-memory Dict yozuvi)
                              |
                              X  <-- ZANJIR SHU YERDA TUGAYDI
                              |
                   platform_layer/telegram/  (HECH QANDAY CHAQIRUV YO'Q)
```

`platform_layer/telegram/`ga yo'l — kodda umuman mavjud emas (na
`ai_layer`dan, na `media_layer.telegram_broadcast`ning o'zidan). Bu
`execution_layer`ning "intentionally inert" holatiga o'xshash: delivery
qatlami CLAUDE.md'ning Trading Safety bo'limida tilga olingan
kelajakdagi, alohida tasdiq talab qiladigan ish.

## Xulosa

Barcha 3 zanjir bir xil natijaga keladi: `ai_layer`dan boshlangan yo'l
`media_layer.telegram_broadcast` ichida DTO/in-memory state darajasida
tugaydi, hech qachon `platform_layer/telegram/`ga yoki tashqi
tarmoq/SDK chaqiruviga yetib bormaydi.

**Verdict: Variant A (Allowed).**
