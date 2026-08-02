# Provider Interface

Status: CANONICAL

---

# Purpose

ProviderInterface — Providers bo'limidagi har bir provider bajarishi shart bo'lgan yagona standart interfeys hisoblanadi.

Uning asosiy vazifasi barcha provider'lar (TwelveData, Bitget va kelajakdagi boshqalar) bir xil Contract asosida ishlashini ta'minlashdir.

ProviderInterface o'zi ma'lumot yuklamaydi — u faqat standartni belgilaydi.

---

# Objective

ProviderInterface quyidagi vazifalarni bajaradi:

• Standart Provider Metodlarini belgilash
• Historical va Live Provider uchun umumiy Contract
• Provider almashtirilishini soddalashtirish

---

# Layer Position

```text
ProviderFactory

        │
        ▼
ProviderInterface

        │
        ▼
TwelveData / Bitget
```

---

# Responsibilities

ProviderInterface:

✓ Standart metodlarni belgilaydi (connect, disconnect, fetch, subscribe)
✓ Har bir provider uchun majburiy Contract'ni belgilaydi

---

# Not Responsible

ProviderInterface:

✗ Ma'lumot yuklash
✗ Ulanishni amalga oshirish
✗ Ma'lumotni tekshirish

---

# Input

ProviderInterface'ni provider'lar implement qiladi — o'zi input qabul qilmaydi.

---

# Output

ProviderInterface standart Contract'ni belgilaydi — o'zi output yaratmaydi.

---

# Golden Rules

1. Barcha provider'lar ProviderInterface'ni implement qiladi.
2. Interface o'zgarishi barcha provider'larga bir xil ta'sir qiladi.
3. Interface'siz provider ProviderFactory tomonidan qabul qilinmaydi.

---

# Related Documents

```text
ProviderInterface/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

ProviderInterface Providers bo'limidagi barcha provider'lar uchun yagona standart Contract'ni belgilovchi Canonical modul hisoblanadi.
