# Provider Factory

Status: CANONICAL

---

# Purpose

ProviderFactory — Providers bo'limining barcha provider'larni yaratish va boshqarish komponentidir.

Uning asosiy vazifasi Configuration asosida kerakli Historical va Live provider'larni ishga tushirish hamda ularni Historical_Data va Live_Data modullariga taqdim etishdir.

ProviderFactory marketni tahlil qilmaydi va savdo qarorini hisoblamaydi.

---

# Objective

ProviderFactory quyidagi vazifalarni bajaradi:

• Provider Instantiation
• Provider Configuration
• Historical Provider Yaratish
• Live Provider Yaratish
• Provider Registry Boshqaruvi

---

# Layer Position

```text
Configuration

        │
        ▼
ProviderFactory

        │
        ▼
ProviderInterface (TwelveData / Bitget)
```

---

# Responsibilities

ProviderFactory:

✓ Configuration'ni o'qiydi
✓ Kerakli provider'ni yaratadi
✓ Provider Registry'ni yuritadi
✓ Historical va Live provider'larni ajratadi

---

# Not Responsible

ProviderFactory:

✗ Ma'lumot yuklash
✗ Ma'lumotni tekshirish
✗ Ma'lumotni saqlash
✗ Market Analysis

---

# Input

ProviderFactory qabul qiladi:

• Configuration
• Provider turi (Historical / Live)

---

# Output

ProviderFactory yaratadi:

• Provider Instance (ProviderInterface'ga mos)

---

# Golden Rules

1. ProviderFactory yagona provider yaratish nuqtasi hisoblanadi.
2. Har bir provider ProviderInterface'ga mos bo'lishi shart.
3. ProviderFactory marketni tahlil qilmaydi.
4. Yangi provider qo'shish mavjud arxitekturani buzmasligi kerak.

---

# Related Documents

```text
ProviderFactory/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

ProviderFactory Providers bo'limining yagona provider yaratish nuqtasi bo'lib, Configuration asosida kerakli Historical yoki Live provider'ni ishga tushiradi.
