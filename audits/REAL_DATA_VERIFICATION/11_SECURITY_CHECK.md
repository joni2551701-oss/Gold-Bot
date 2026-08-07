# 11 — Security Check (API kalit oqishi)

## Metodologiya

`grep -rn "api_key" data_layer/ --include=*.py` natijalari
`log|print|repr|str\(` bilan filtrlandi — hech qanday moslik topilmadi
(bo'sh natija).

## CONFIRMED: xavfsiz oshkor qilish pattern'i haqiqatan ham qo'llanilgan

1. `config.py:MaskedSecret` (`__repr__`/`__str__`, `config.py:135-163`)
   — har qanday API kalit shu tur orqali saqlanadi (masalan
   `BitgetProvider._api_key`, `bitget_provider.py:60-63`, docstring
   satr 18-19: *"even its repr renders `***`"*). Bu `str()`/`repr()`
   chaqirilganda xom qiymatni hech qachon qaytarmaydi.

2. `TwelveDataClient.api_key` (`twelve_data_client.py:39-46`) —
   `Secrets().TWELVE_DATA_API_KEY`dan olingan xom `str`, `MaskedSecret`
   emas. Grep natijasi shuni tasdiqlaydi: `self.api_key` hech qachon
   `logger.*`/`print`/`repr`/`f"..."`ichida ishlatilmaydi
   (`twelve_data_client.py`da faqat `params["apikey"] = self.api_key`
   sifatida HTTP so'rov parametriga uzatiladi, satr 83 — bu normal,
   chunki bu HTTP so'rovning o'zi, log emas).

3. `TwelveDataProvider.get_market_status()`
   (`data_layer/providers/twelve_data_provider/twelve_data_provider.py:116-124`)
   — `"TWELVE_DATA_API_KEY not configured"` matnini qaytaradi, lekin
   hech qachon kalitning o'zini emas — faqat mavjud/yo'qligini
   (YES/NO ekvivalenti).

4. Xatolik xabarlari (`ValueError`/`ConnectionError`,
   `twelve_data_client.py:76,95,120`) — hech biri `self.api_key`ni
   o'z ichiga olmaydi, faqat statik matn yoki API'ning o'z
   `error_message`sini (bu API tomonidan qaytarilgan xabar, kalitni
   o'z ichiga olmaydi).

## Xulosa

"API configured: YES/NO" xavfsiz-oshkor qilish pattern'i **haqiqatan
ham qo'llanilgan** holat sifatida tasdiqlandi (xom kalit emas). Hech
qanday joyda API kalitining o'zi log/print/repr/xato xabariga
sizib chiqishi aniqlanmadi.
