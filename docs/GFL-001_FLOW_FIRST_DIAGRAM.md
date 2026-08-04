# GFL-001 — Flow-First Development Diagram

## Maqsad

Ushbu diagramma GoldBot'ning yagona rasmiy Data Flow (Flow-First) arxitekturasini ko'rsatadi.

Har bir modul o'zidan oldingi modulning Output'ini qabul qiladi va keyingi modul uchun Input yaratadi.

Development har doim ushbu oqim bo'yicha amalga oshiriladi.

---

# FLOW DIAGRAM

══════════════════════════════════════════════════════════════════════════════
                            GOLDBOT DATA FLOW
══════════════════════════════════════════════════════════════════════════════

                               GoldBot Start
                                     │
                                     ▼
                         Configuration Layer
                                     │
                                     ▼
                         Provider Factory Layer
                                     │
                 ┌───────────────────┴───────────────────┐
                 ▼                                       ▼
      Historical Data Layer                  Price Stream Layer
                 │                                       │
                 └───────────────────┬───────────────────┘
                                     ▼
                        Data Validation Layer
                                     │
                                     ▼
                         Market Memory (SSOT)
                                     │
      ┌──────────────┬───────────────┬───────────────┬──────────────┐
      ▼              ▼               ▼               ▼
 Market Engine   Historical DB   Current Price   Event Bus
      │
      ▼
 Context Engine
      │
      ▼
 Analysis Engine
      │
      ▼
 Indicator Engine
      │
      ▼
 Strategy Engine
      │
      ▼
 Confluence Engine
      │
      ▼
 Decision Engine
      │
      ▼
 Risk Engine
      │
      ▼
 Signal Engine
      │
      ▼
 Execution Engine
      │
      ▼
 Trade Monitoring Layer
      │
      ▼
 GoldBot Core API
      │
══════════════════════════════════════════════════════════════════════════════
                         APPLICATION SERVICES
══════════════════════════════════════════════════════════════════════════════
      │
      ▼
 API Gateway
      │
      ├──────────────┬──────────────┬──────────────┬──────────────┐
      ▼              ▼              ▼              ▼
 Telegram       Mini App        Android         iOS
      │              │              │              │
      ├──────────────┼──────────────┼──────────────┤
      ▼              ▼              ▼
 Desktop           Web         Public API
      │
      ▼
 User

══════════════════════════════════════════════════════════════════════════════

Har bir Consumer bir xil Core API orqali ishlaydi.

Telegram
Mini App
Android
iOS
Desktop
Web

hech qachon Provider yoki Core moduliga to'g'ridan-to'g'ri ulanmaydi.

Barcha platformalar faqat GoldBot Core API orqali ma'lumot oladi.

══════════════════════════════════════════════════════════════════════════════

## Development Rule

Development har doim quyidagi tartibda amalga oshiriladi.

Producer
↓
Input
↓
Processing
↓
Output
↓
Consumer
↓
Validation
↓
End-to-End Test
↓
Documentation
↓
WORK_LOG
↓
Next Flow

Har bir Flow to'liq yakunlanmaguncha keyingi Flow boshlanmaydi.

══════════════════════════════════════════════════════════════════════════════

## Flow Completion

Flow Completed hisoblanadi agar:

✓ Producer ishlaydi

✓ Input qabul qilinadi

✓ Processing ishlaydi

✓ Output hosil bo'ladi

✓ Consumer ishlaydi

✓ End-to-End Test PASS

✓ Documentation yangilangan

✓ WORK_LOG yozilgan

══════════════════════════════════════════════════════════════════════════════

## Forbidden

Taqiqlanadi:

• Producer'siz Consumer yaratish

• Input'siz modul yaratish

• Output ishlatilmasligi

• Flow uzilgan holda Development davom ettirish

• Batch Coding

• Layer bo'yicha tasodifiy Development

• End-to-End test o'tmasdan Completed deb belgilash

══════════════════════════════════════════════════════════════════════════════

## Final Principle

GoldBot Layer-first emas.

GoldBot File-first emas.

GoldBot Flow-first arxitektura asosida ishlab chiqiladi.

Har bir Data Flow boshidan oxirigacha ishlaydigan holatga kelgandan keyingina keyingi Flow boshlanadi.
