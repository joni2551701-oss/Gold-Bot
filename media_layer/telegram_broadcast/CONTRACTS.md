# Telegram Broadcast Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat TelegramBroadcast modulining rasmiy Architecture Contract hujjati hisoblanadi.

---

# Module Responsibility

TelegramBroadcast quyidagilar uchun javobgar.

✓ Broadcast Provider'larni (Telegram, YouTube, RTMP, Mini App va h.k.) ro'yxatga oladi

✓ Har bir Provider'ning ENABLED/DISABLED holatini boshqaradi

✓ Broadcast Trigger'larni boshqaradi

✓ Broadcast Request va Asset tayyorlaydi

✓ Broadcast Status'ni kuzatadi

TelegramBroadcast bajarmaydi.

✗ Actual Message Delivery (Platform Layer vazifasi)

✗ Content Generation

✗ Market Analysis

✗ Signal Generation

✗ Trading Decision

---

# Module Boundary

AI_Content_Studio / Content_Manager

↓

Telegram_Broadcast

↓

Platform Layer

---

# Input Contract

• Content Result

• Broadcast Configuration

• Owner Enable/Disable Intent

• Trigger Event

---

# Output Contract

• Broadcast Request

• Broadcast Asset

• Broadcast Status

• Broadcast Metadata

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

# Runtime Contract

1. Har bir Provider sukut bo'yicha DISABLED holatida bo'ladi.

2. Provider faqat Owner ruxsati bilan ENABLED holatiga o'tadi.

3. Telegram_Broadcast xabarni o'zi yubormaydi — yuborish Platform Layer vazifasi.

4. Broadcast faqat tasdiqlangan kontentdan tayyorlanadi.

5. Circular Dependency qat'iyan taqiqlanadi.

---

# Acceptance Criteria

✓ Provider ro'yxatga olinadi.

✓ Trigger boshqariladi.

✓ Broadcast Request yaratiladi.

✓ Broadcast Status kuzatiladi.

✓ Architecture Boundary buzilmaydi.

---

# Summary

TelegramBroadcast Contract Telegram_Broadcast Media Layer ichidagi Canonical Broadcast moduli hisoblanadi. U tarqatish kanallari va shartlarini boshqaradi hamda Broadcast Request tayyorlaydi — xabarni yakuniy yuborish Platform Layer zimmasida qoladi.
