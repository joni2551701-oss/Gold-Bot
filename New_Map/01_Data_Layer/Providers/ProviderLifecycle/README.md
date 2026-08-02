# Provider Lifecycle

Status: CANONICAL

---

# Purpose

ProviderLifecycle — Providers bo'limidagi barcha provider'larning hayotiy siklini (ishga tushirish, qayta ulanish, to'xtatish, sog'liqni tekshirish) boshqaruvchi komponent hisoblanadi.

Uning asosiy vazifasi TwelveData va Bitget kabi provider'larning ishonchli ishlashini ta'minlashdir.

ProviderLifecycle marketni tahlil qilmaydi.

---

# Objective

ProviderLifecycle quyidagi vazifalarni bajaradi:

• Provider Startup
• Provider Reconnect
• Provider Shutdown
• Provider Health Check
• Provider Monitoring

---

# Layer Position

```text
ProviderFactory

        │
        ▼
ProviderLifecycle

        │
        ▼
TwelveData / Bitget
```

---

# Responsibilities

ProviderLifecycle:

✓ Provider'ni ishga tushiradi
✓ Ulanish uzilganda qayta ulaydi
✓ Provider'ni to'xtatadi
✓ Sog'liqni tekshiradi (Health Check)

---

# Not Responsible

ProviderLifecycle:

✗ Ma'lumot yuklash
✗ Ma'lumotni tekshirish
✗ Ma'lumotni saqlash

---

# Input

ProviderLifecycle qabul qiladi:

• Provider Instance
• Lifecycle Event (Start, Stop, Reconnect)

---

# Output

ProviderLifecycle yaratadi:

• Provider Status
• Health Report

---

# Golden Rules

1. Har bir provider ProviderLifecycle orqali boshqariladi.
2. Ulanish uzilishi avtomatik Reconnect'ni ishga tushiradi.
3. Provider nosozligi GoldBot Core ishlashini to'xtatmasligi kerak.

---

# Related Documents

```text
ProviderLifecycle/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

ProviderLifecycle Providers bo'limidagi barcha provider'larning hayotiy siklini boshqaruvchi Canonical modul hisoblanadi.
