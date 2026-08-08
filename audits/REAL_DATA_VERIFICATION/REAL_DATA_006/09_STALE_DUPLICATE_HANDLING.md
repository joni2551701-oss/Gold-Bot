# REAL-DATA-006 — 09. Stale / Duplicate / Invalid Handling (mavjud xulq)

Faqat MAVJUD xulq hujjatlashtiriladi — yangi mantiq QO'SHILMADI.

## Uch qatlamli himoya

### 1-qatlam — Provider dedupe (`twelve_data_provider.py:76-79`)
`read()` faqat yangiroq candle close chiqqanda emit qiladi:
```
if self._last_ts is not None and ts <= self._last_ts:
    return []
self._last_ts = ts
```
Bir xil yoki eski timestamp bo'lsa — bo'sh ro'yxat (tick yo'q). Bu
"price unchanged between ticks" holatini normal boshqaradi (xato emas).

### 2-qatlam — Stream ordering (`price_stream.py:230-234`)
`_forward_ordered` event'larni qat'iy timestamp tartibida yetkazadi va
strictly-older'larni tashlaydi:
```
if self._last_ts is not None and e.timestamp < self._last_ts:
    self._stats["dropped_out_of_order"] += 1
    continue
```

### 3-qatlam — StreamValidator (`stream_validator.py:101-110`)
`previous`ga nisbatan:
- `ts == prev_ts` → `duplicate` → DROP (`:107-108`)
- `ts < prev_ts` → `sequence` → DROP (`:109-110`)

Qo'shimcha: invalid price ≤ 0 (`:88-89`), future timestamp (`:94-99`),
non-finite price (`:86-87`) — hammasi DROP.

## "Price unchanged" holati (order talabi)

Bu **xato EMAS**. Provider dedupe (1-qatlam) yangi candle bo'lmaguncha
bo'sh qaytaradi, shuning uchun cache oldingi price'da qoladi va yangi
event chiqmaydi. Probe buni aniq boshqaradi: `unchanged_from_previous`
flag qo'yiladi va log'da *"unchanged from previous tick -- not a
failure; M1 candle not yet advanced"* deb ko'rsatiladi
(`real_price_stream_probe.py`). Timestamp/sequence/source xulqi qayd
etiladi, PASS/BLOCKED holati o'zgarmaydi.

## Status: **PASS (mavjud uch qatlamli duplicate/stale/invalid himoya, real)**
