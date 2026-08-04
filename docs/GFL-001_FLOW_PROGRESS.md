# GFL-001 — Flow Progress

## Maqsad

Ushbu hujjat GoldBot Data Flow rivojlanishining rasmiy holatini yuritadi.

Har bir Flow quyidagi statuslardan biriga ega bo'ladi va Development davomida muntazam yangilanadi.

---

# Status

🟦 Blueprint

Flow hali boshlanmagan.

---

🟨 In Progress

Flow ustida Development davom etmoqda.

---

🟪 Review

Flow yakunlandi va Director Review kutilmoqda.

---

🟩 Completed

Flow to'liq yakunlandi.

Barcha testlar muvaffaqiyatli o'tgan.

Documentation yangilangan.

WORK_LOG yozilgan.

---

🟥 Blocked

Flow davom eta olmaydi.

Director Review talab qilinadi.

---

# Flow Progress

| Flow | Nomi | Status | Progress | Owner | Izoh |
|------|------|--------|----------|-------|------|
| FLOW-001 | Current Price | 🟩 | 100% | Worker | Yakunlandi -- 2026-08-04. Audit shuni ko'rsatdi: barcha modullar allaqachon mavjud edi, faqat ulanmagan (Price Stream `tick()`ni hech kim chaqirmasdi, `CurrentPriceProvider` default holatda har safar yangi/alohida instance qurar edi). Tuzatildi: shared singleton + default StreamValidator + default MarketMemoryRegistry + polling.py'da tick driver. 5411 test PASS, E2E test qo'shildi. |
| FLOW-002 | Market Memory | 🟦 | 0% | Worker | Navbatda |
| FLOW-003 | Market Engine | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-004 | Context Engine | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-005 | Analysis Engine | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-006 | Indicator Engine | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-007 | Strategy Engine | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-008 | Confluence Engine | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-009 | Decision Engine | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-010 | Risk Engine | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-011 | Signal Engine | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-012 | Execution Engine | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-013 | Trade Monitoring | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-014 | GoldBot Core API | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-015 | Application Services | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-016 | Telegram | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-017 | Mini App | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-018 | Android | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-019 | iOS | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-020 | Desktop | 🟦 | 0% | Worker | Kutmoqda |
| FLOW-021 | Web | 🟦 | 0% | Worker | Kutmoqda |

---

# Development Rules

Worker faqat bitta Flow ustida ishlaydi.

Oldingi Flow Completed bo'lmaguncha keyingi Flow boshlanmaydi.

Flow statusi ushbu hujjatda darhol yangilanadi.

---

# Status Lifecycle

Blueprint

↓

In Progress

↓

Review

↓

Completed

yoki

Blocked

↓

Director Review

↓

In Progress

↓

Completed

---

# Progress Rules

Progress faqat:

- Audit
- Development
- Testing
- Validation
- Documentation
- WORK_LOG

yakunlangandan keyin o'zgartiriladi.

---

# Blocked Rules

Agar Flow:

- Input ololmasa
- Output ishlamasa
- End-to-End test o'tmasa
- Director Review talab qilsa

Status:

🟥 Blocked

bo'ladi.

---

# Completion Rules

Flow Completed bo'lishi uchun:

✓ Audit yakunlangan

✓ Kod ishlaydi

✓ Input ishlaydi

✓ Output ishlaydi

✓ Consumer ishlaydi

✓ Barcha Consumer'lar PASS (Fan-Out Rule)

✓ End-to-End Test PASS

✓ Producer→Consumer latency o'lchangan va yozilgan (Latency Rule)

✓ Documentation yangilangan

✓ WORK_LOG yozilgan

✓ Director Review yopilgan (agar talab qilingan bo'lsa)

---

# Final Principle

Flow Progress — GoldBot Development holatini aks ettiruvchi yagona rasmiy hujjat hisoblanadi.

Worker har bir Flow holatini ushbu hujjatda doimiy ravishda yangilab borishi shart.
