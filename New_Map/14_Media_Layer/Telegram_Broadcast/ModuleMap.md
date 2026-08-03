# Telegram Broadcast Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat TelegramBroadcast ichki arxitekturasini tavsiflaydi (ichki submodullar implementatsiya bosqichida to'ldiriladi).

---

# Internal Architecture (Planned)

TelegramBroadcast

├── BroadcastManager

├── ProviderManager

├── TriggerManager

└── BroadcastAdapter

---

# Module Position

AI_Content_Studio / Content_Manager

↓

Telegram_Broadcast

↓

Platform Layer

---

# Processing Pipeline (Planned)

BroadcastManager → ProviderManager → TriggerManager → BroadcastAdapter

---

# Dependency Map

AI_Content_Studio / Content_Manager

↓

Telegram_Broadcast

↓

Platform Layer

---

# Allowed Dependencies

✓ AI_Content_Studio

✓ Content_Manager

---

# Forbidden Dependencies

✗ Signal Layer

✗ Decision Layer

✗ Risk Layer

✗ Execution Layer

✗ Database Layer

---

# Runtime Flow

Receive Input

↓

Process (TelegramBroadcast)

↓

Emit Output

↓

Platform Layer

---

# Summary

TelegramBroadcast Telegram_Broadcast Media Layer ichidagi Canonical Broadcast moduli hisoblanadi. U tarqatish kanallari va shartlarini boshqaradi hamda Broadcast Request tayyorlaydi — xabarni yakuniy yuborish Platform Layer zimmasida qoladi.
